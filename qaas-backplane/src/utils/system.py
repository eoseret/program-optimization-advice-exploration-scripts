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
# Created April 2023
# Contributors: Hafid/David

import os
import sys
import subprocess
import cpuinfo

def get_vendor_name():
    vendor = cpuinfo.get_cpu_info()['vendor_id_raw']
    if vendor == 'GenuineIntel':
        return 'intel'
    elif vendor == 'AuthenticAMD':
        return 'amd'
    else:
        return 'unknown'

def get_family():
    '''Get the CPU family ID'''
    return cpuinfo.get_cpu_info()['family']

def get_model():
    '''Get the CPU model ID'''
    return cpuinfo.get_cpu_info()['model']

def get_intel_processor_name():
    # Get the CPU family ID
    family = get_family ()
    # Get the CPU model ID
    model = get_model()

    if family == 6:
        if model == 143:
            CPU = 'SPR'
        elif model == 106:
            CPU = 'ICL'
        elif model == 85:
            CPU = 'SKL'
        elif model == 63 or model == 79:
            CPU = 'HSW'
        else:
            CPU = 'OTHER'

    elif family == 25:
        if model == 17:
            CPU = 'ZEN_V4'
        else:
            CPU = 'OTHER'

    return CPU

def get_number_of_cpus():
    '''Retrieve the number of logical CPUs from lscpu command'''
    count = int(subprocess.check_output('lscpu --extended=CPU | tail -n +2 | sort -u | wc -l', shell=True))
    return count

def get_number_of_cores():
    '''Retrieve the number of physical cores from lscpu command'''
    count = int(subprocess.check_output('lscpu --extended=CORE | tail -n +2 | sort -u | wc -l', shell=True))
    return count

def get_number_of_sockets():
    '''Retrieve the number of sockets from lscpu command'''
    count = int(subprocess.check_output('lscpu --extended=SOCKET | tail -n +2 | sort -u | wc -l', shell=True))
    return count

def get_number_of_nodes():
    '''Retrieve the number of sockets from lscpu command'''
    count = int(subprocess.check_output('lscpu --extended=NODE | tail -n +2 | sort -u | wc -l', shell=True))
    return count
