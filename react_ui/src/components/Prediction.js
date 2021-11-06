import {Box, CircularProgress, Snackbar} from '@material-ui/core';
import Alert from "@material-ui/lab/Alert";
import { useState } from 'react';
import VulPredTable from './VulPredTable';


const Prediction = () => {

    const [rows,setRows] = useState(null);
    const [selectedRows, setSelectedRows] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [snackOpen, setSnackOpen] = useState(false);
    const [snackSeverity, setSnackSeverity] = useState("sucess");
    const [alertMessage, setAlertMessage] = useState("");

    const makeAlertMessage = (message, severity) => {
        setAlertMessage(message);
        setSnackSeverity(severity);
        setSnackOpen(true);
    };


    const uploadCve = (e) =>{
        var search_input = document.getElementById("form1");
        var search_button = document.getElementById("searchButton");
        var cve_id = search_input.value;
        search_button.disabled = true;
        search_input.value = null;
        setUploading(true);
        makeAlertMessage("Generating Exploit Predictions For Valid CVEs......", "info");

        fetch("http://127.0.0.1:8000/fastembed_api/upload-cve/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(cve_id)
        }).then(response => {
            return response.json();
        }).then(data => {
            var obj = JSON.parse(data);

            for ( var i = 0; i <obj.length; i++) {
                obj[i].Exploited = obj[i].Exploited ? "Yes" : "No";
            }
            setUploading(false);
            setRows(obj)
            search_button.disabled = false;
            makeAlertMessage("Fetching Done", "success");

        }).catch(err => {
            if (err.name === 'AbortError') {
                console.log('fetch aborted');
                makeAlertMessage('fetch aborted', "error");
            } else {
                setUploading(false);
                search_button = document.getElementById("searchButton");
                search_button.disabled = false;
                console.log(err.message);
                makeAlertMessage(err.message, "error");

            }            
        });
    };

    const handleSelection = (selectedRows) =>{
        setSelectedRows(selectedRows);
    }


    const handleDownload = () =>{
        var data = selectedRows;
        var arr = rows.filter(item => {
            return data.includes(item.id.toString());
        });
        var fileDownload = require('js-file-download');
        fileDownload(JSON.stringify(arr), 'Predictions.json');
    }

    const handleSnackClose = (event, reason) => {
        if (reason === "clickaway") {
          return;
        }
    
        setSnackOpen(false);
      };

    return ( 
        <div>
            <div className="jumbotron jumbotron-fluid my_text_container">
                <div className="container">
                    <h3 className="display-4 row offset-md-3">Vulnerability Prediction</h3>
                    <p className="lead row offset-md-3">Search for vulnerability exploitation using CVE-ID!!!</p>
                </div>
            </div>
            <div className="input-group col-md-6 offset-md-3">
                <input type="text" id="form1" className="form-control" placeholder="Search CVE-ID..."/>
                <div className="input-group-append">
                    <button type="button" id="searchButton" className="btn btn-outline-secondary" onClick={uploadCve}>
                        <span className="material-icons">search</span>
                    </button>
                </div>
            </div>
            {uploading && <Box m={2}><CircularProgress/></Box>}
            {!uploading && <Box m={2}><VulPredTable rows={rows} handleSelection={handleSelection} /></Box>}
            {rows && !uploading &&
                <div className="m-3 ">
                    <button type="button" id="downloadButton" className="btn btn-primary my_download_text" onClick={handleDownload} 
                    disabled={selectedRows.length === 0}>
                        <span className="material-icons">download</span> Download Selection
                    </button>
                </div>
            }
            <Snackbar
                anchorOrigin={{ vertical: "top", horizontal: "right" }}
                open={snackOpen}
                autoHideDuration={3000}
                onClose={handleSnackClose}
            >
                <Alert onClose={handleSnackClose} severity={snackSeverity} elevation={6} variant="filled">
                    {alertMessage}
                </Alert>
            </Snackbar>
        </div>
    );
}

export default Prediction;