#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# MIT License

# Copyright (c) 2023 Intel-Sandbox
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
# HISTORY
# Created October 2022
# Contributors: Yue/David

import pandas as pd

from flask import Flask
from flask_cors import CORS
from flask import jsonify
import numpy as np
import configparser
import os

script_dir=os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, "../../config/qaas-web.conf")

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

config.read(config_path)
def calculate_speedup(time_comp, baseline_compiler):
    baseline_time = time_comp.get(baseline_compiler, 0)
    if baseline_time == 0:
        return []

    win_lose_list = []
    for compiler, time in time_comp.items():
        speedup = baseline_time / time
        if speedup < 1:
            converted_speedup = 1 / speedup
            win_lose_list.append({'winner': baseline_compiler, 'loser': compiler, 'speedup': converted_speedup})
    return win_lose_list

def create_app(config):
    app = Flask(__name__)
    CORS(app)

    @app.route('/get_qaas_unicore_perf_gflops_data', methods=['GET'])
    def get_qaas_unicore_perf_gflops_data():
        df = pd.read_csv('/host/home/yjiao/ArchComp.Unicore.csv')

        #sort by x axis
        df['Mean'] = df.drop(columns=['Apps']).mean(axis=1)
        df.sort_values('Mean', inplace=True)
        df.drop('Mean', axis=1, inplace=True)


        data_dict = df.to_dict(orient='list')
        # replace NaN with None (null in JSON)
        for key in data_dict.keys():
            data_dict[key] = [None if pd.isna(x) else x for x in data_dict[key]]

     
        return jsonify(data_dict)

    @app.route('/get_arccomp_data', methods=['GET'])
    def get_arccomp_data():
        df = pd.read_csv('/host/home/yjiao/ArchComp.Multicore.csv')

        df['ICL per-core GFlops'] = df['ICL.Gf'] / df['ICL.cores']
        df['SPR per-core GFlops'] = df['SPR.Gf'] / df['SPR.cores']

        df['coreICL/coreSPR'] = df['ICL per-core GFlops'] / df['SPR per-core GFlops']
        df['coreSPR/coreICL'] = df['SPR per-core GFlops'] / df['ICL per-core GFlops']
        df['winner'] = np.where(df['coreICL/coreSPR'] > 1, 'ICL', 'SPR')
        df['winner ratio'] = df[['coreICL/coreSPR', 'coreSPR/coreICL']].max(axis=1)
        result_df = df[['Apps', 'winner', 'winner ratio']]
        #sort the result df
        result_df = result_df.sort_values(by='winner ratio', ascending=True)


        data_dict = result_df.to_dict(orient='list')
        # replace NaN with None (null in JSON)
        for key in data_dict.keys():
            data_dict[key] = [None if pd.isna(x) else x for x in data_dict[key]]

        return jsonify(data_dict)
    
    @app.route('/get_appgain_data', methods=['GET'])
    def get_appgain_data():
        df = pd.read_excel('/host/home/yjiao/QaaS_Min_Max_Unicore_Perf_Default.xlsx', header=3).dropna()
        df['largest_gain'] = df[['ICX: -O3 -march=native', 'ICC: -O3 -march=native', 'GCC: -O3 -march=native']].max(axis=1)
        df['app'] = df['Unnamed: 0']
        result_df = df[['app', 'largest_gain']]
        result_df = result_df.sort_values(by='largest_gain', ascending=True)

        data_dict = result_df.to_dict(orient='list')
        # replace NaN with None (null in JSON)
        for key in data_dict.keys():
            data_dict[key] = [None if pd.isna(x) else x for x in data_dict[key]]
        return jsonify(data_dict)
    
    @app.route('/get_qaas_multicore_perf_gflops_data', methods=['GET'])
    def get_qaas_multicore_perf_gflops_data():
        df = pd.read_csv('/host/home/yjiao/ArchComp.Multicore.csv')

        #sort by x axis
        df['Mean'] = df.drop(columns=['Apps']).mean(axis=1)
        df.sort_values('Mean', inplace=True)
        df.drop('Mean', axis=1, inplace=True)
        df['ICL Gf/core'] = df['ICL.Gf'] / df['ICL.cores']
        df['SPR Gf/core'] = df['SPR.Gf'] / df['SPR.cores']
        df.drop('ICL.cores', axis=1, inplace=True)
        df.drop('SPR.cores', axis=1, inplace=True)
        df.rename({'ICL.Gf':'ICL total Gf', 'SPR.Gf':'SPR total Gf'}, axis=1, inplace=True)

        data_dict = df.to_dict(orient='list')
        # replace NaN with None (null in JSON)
        for key in data_dict.keys():
            data_dict[key] = [None if pd.isna(x) else x for x in data_dict[key]]

        return jsonify(data_dict)
    
    @app.route('/get_qaas_compiler_comparison_historgram_data', methods=['GET'])
    def get_qaas_compiler_comparison_historgram_data():
        df = pd.read_excel('/host/home/yjiao/QaaS_Min_Max_Unicore_Perf_Default.xlsx', header=3)

        # convert columns to numeric, replacing errors with NaN
        df['Best (option) perf. (s)'] = pd.to_numeric(df['Best (option) perf. (s)'], errors='coerce')
        df['ICX: -O3 -march=native'] = pd.to_numeric(df['ICX: -O3 -march=native'], errors='coerce')

  
        
        # List to store unique compilers
        compilers = ['ICX', 'ICC', 'GCC']

        applications = []
        delta = 0.03  # 3% threshold

        #get the execution time back
        df['ICX'] = df['Best (option) perf. (s)'] * df['ICX: -O3 -march=native']
        df['ICC'] = df['Best (option) perf. (s)'] * df['ICC: -O3 -march=native']
        df['GCC'] = df['Best (option) perf. (s)'] * df['GCC: -O3 -march=native']


      
        #one row is one application
        for index, row in df.iterrows():
            app_name = row['Unnamed: 0']
            if pd.isna(app_name):
                break
            icx_speedup = row['ICX: -O3 -march=native']
            icc_speedup = row['ICC: -O3 -march=native']
            gcc_speedup = row['GCC: -O3 -march=native']

            #if there is empty value just continue
            if pd.isna(icx_speedup) or pd.isna(icc_speedup) or pd.isna(gcc_speedup):
                continue
            
      
            speedups = {'ICX': icx_speedup, 'ICC': icc_speedup, 'GCC': gcc_speedup}

            best_compiler_set = sorted(set(row['Best compiler'].split("/")))
            is_n_way_tie = len(best_compiler_set) == 3

            #if it is a tie just look at next application
            if is_n_way_tie:
                applications.append({
                'application': app_name,
                'is_n_way_tie': is_n_way_tie,
                'n_way' : len(best_compiler_set),
                'win_lose': [],
                })
                continue

            best_compiler = best_compiler_set[0].upper()


            best_time_key = f'{best_compiler}qaas'
            time_comp = {'ICX': row['ICX'],'ICC': row['ICC'], 'GCC': row['GCC'], best_time_key: row['Best (option) perf. (s)']}
            all_win_lose = []

            for baseline_compiler in ['ICX', 'ICC', 'GCC', best_time_key]:
                win_lose = calculate_speedup(time_comp, baseline_compiler)
                all_win_lose.extend(win_lose)

          
            applications.append({
                'application': app_name,
                'win_lose': all_win_lose,
                'is_n_way_tie': is_n_way_tie
            })

        return jsonify({
            'compilers': compilers,
            'applications': applications
        })

    
    return app
if __name__ == '__main__':
    app = create_app(config)
    app.run(debug=True,port=5002)