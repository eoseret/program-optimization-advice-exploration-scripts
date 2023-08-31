import React, { useState, useEffect } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import Table from "./table";
function ApplicationSubTable({ data, setSelectedRows, selectedRows }) {
    const navigate = useNavigate();

    const handleButtonClick = async (timestamp) => {
        // Call your backend API here and fetch data
        console.log(timestamp)
        const newWindow = window.open(`/generated?loading=true`, "_blank");

        try {
            const result = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/get_html_by_timestamp`, { 'timestamp': timestamp })
            //send user to new page
            // navigate('/generated');
            newWindow.location.href = "/generated?loading=false";

        } catch (error) {
            console.error('Error fetching data:', error);
        }

    };

    const handleRowSelection = (event, rowInfo) => {
        if (rowInfo) {
            const selected = event.target.checked;

            if (selected) {
                setSelectedRows(prevSelectedRows => [...prevSelectedRows, rowInfo._original]);
            } else {
                setSelectedRows(prevSelectedRows => prevSelectedRows.filter(row => row !== rowInfo._original));
            }
        }
    };
    const columns = [
        {
            Header: 'Select',
            id: 'selection',
            Cell: ({ row }) => (
                <div className="table-action">
                    <input
                        type="checkbox"
                        checked={selectedRows.some(selectedRow => selectedRow === row._original)}
                        onChange={(e) => handleRowSelection(e, row)}
                    />
                </div>
            ),
            width: 50,

        },
        {
            Header: 'Action',
            id: 'button',
            Cell: ({ row }) => (
                <div className="table-action">
                    <button className="table-action-button" onClick={() => handleButtonClick(row._original.timestamp)}>View Details</button>
                </div>

            ),
            width: 100,
        },
        {
            Header: 'Timestamp',
            accessor: 'timestamp'
        },
        {
            Header: 'Machine',
            accessor: 'machine'
        },
        {
            Header: 'Data',
            accessor: 'data'
        },
    ];

    return (
        <Table
            data={data}
            columns={columns}
            defaultPageSize={5}
        />
    );
}

export default ApplicationSubTable;