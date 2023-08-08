import React, { useState, useEffect } from "react";
import Histogram from "./Histogram";
import { Modal } from 'antd';
import axios from 'axios';
import { RANGES } from "../Constants";
export default function AllSpeedupRangeGraph() {
    const [data, setData] = useState(null);
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const colors = ['#4D4D4D', '#5DA5DA', '#FAA43A', '#60BD68', '#F17CB0', '#B2912F', '#B276B2', '#DECF3F', '#F15854'];

    const fetchData = () => {
        setLoading(true);

        axios.get(`${process.env.REACT_APP_API_BASE_URL}/ov_get_all_speedup_range`)
            .then(response => {
                setData(response.data);
                setOpen(true);
                setLoading(false)

            })
            .catch(error => {
                console.error('Error fetching performance data:', error);
                setLoading(false)
            });
    }



    // Prepare histogram for speedup r for different compilers
    const generateDataForCompiler = (compilersData, compilerName) => {
        let speedupData = [];
        for (let d of compilersData[compilerName]) {
            speedupData.push(d.speedup_r);
        }

        // Generate histogram data
        return RANGES.map(range => {
            if (range.includes('>')) {
                const min = parseFloat(range.split('>')[1]);
                return speedupData.filter(speed => speed > min).length;
            } else {
                const [min, max] = range.split('-').map(Number);
                return speedupData.filter(speed => speed >= min && speed < max).length;
            }
        });
    };



    if (loading) {
        return <div>Loading...</div>;
    }

    const chartData = data ? {
        labels: RANGES,
        datasets: Object.keys(data).map((compilerName, index) => ({
            label: `${compilerName}`,
            data: generateDataForCompiler(data, compilerName),
            fill: false,
            backgroundColor: colors[index % colors.length]
        })),
        xAxis: 'Range',
        yAxis: 'Count Speedup R',
    } : null;

    console.log(chartData)
    return (

        <div >

            <button onClick={fetchData}>
                Show All Speedup Range Count Graph
            </button>
            <Modal
                title="All speedup range count"
                open={open}
                onCancel={() => setOpen(false)}
                onOk={() => setOpen(false)}
            >
                <Histogram data={chartData} />
            </Modal>

        </div>
    )
}
