import {Box, CircularProgress, Snackbar} from '@material-ui/core';
import Alert from "@material-ui/lab/Alert";
import VulTable from './VulTable';
import { useState } from 'react';

// const getCookie= (name) => {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// };

const Detection = () => {

    const [rows,setRows] = useState(null);
    const [uploadText, setUploadText] = useState("Upload Source Code");
    const [uploaded, setUploaded] = useState(false);
    const [current_working_directory, setcurrent_working_directory] = useState(null);
    const [selectedRows, setSelectedRows] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [tableLoading, setTableLoading] = useState(false);
    const [snackOpen, setSnackOpen] = useState(false);
    const [snackSeverity, setSnackSeverity] = useState("sucess");
    const [alertMessage, setAlertMessage] = useState("");

    var upload_button = null;
    var file_upload = null;
    var temp_files = null;

    const makeAlertMessage = (message, severity) => {
        setAlertMessage(message);
        setSnackSeverity(severity);
        setSnackOpen(true);
    };

    const handleFileUpload = (e) => {
        upload_button = document.getElementById("uploadButton");
        upload_button.disabled = true;
        temp_files = e.target.files;
        if(temp_files.length <= 0) {
            upload_button.disabled = false;
            return;
        } 
        var form_data = new FormData();
        // for( var i = 0; i < temp_files.length;i++){
        //     form_data.append(temp_files[i].webkitRelativePath,temp_files[i]);
        // }
        form_data.append("files", temp_files[0].webkitRelativePath);
        // var fr = new  FileReader();
        // fr.onload = () => {
        //     console.log(fr.result);
        // };
        // fr.readAsText(temp_files[0]);
        setUploadText("Uploading....");
        setUploading(true);
        makeAlertMessage("Uploading Source Code......", "info");
        // var csrftoken = getCookie('csrftoken')
        // console.log(csrftoken);
        fetch('http://127.0.0.1:8000/detection_api/upload-code/',{
            method: 'POST',
            headers: { 
                "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryyrV7KO0BoCBuDbTL",
            },
            body: form_data
          }).then((response) => {
            file_upload = document.getElementById("fileUpload");
            file_upload.value = null;
            return response.json();
          }).then((data) => {
            setcurrent_working_directory(data);
            setUploading(false);
            setUploadText("Source Code Loaded");
            setUploaded(true);
            makeAlertMessage("Source Code Uploaded", "success");
          }).catch(err => {
            if (err.name === 'AbortError') {
              console.log('fetch aborted')
              makeAlertMessage('fetch aborted', "error");
            } else {
            setUploading(false);
            setUploadText("Upload Source Code");
            upload_button = document.getElementById("uploadButton");
            upload_button.disabled = false;
            console.log(err.message);
            makeAlertMessage(err.message, "error");
            }
          });
    };

    const uploadCode = (e) =>{
        file_upload = document.getElementById("fileUpload");
        file_upload.click();
    };

    const undoUpload = (e) =>{
        upload_button = document.getElementById("uploadButton");
        upload_button.disabled = false;
        setcurrent_working_directory(null);
        setUploadText("Upload Source Code");
        setUploaded(false);
        setRows(null);
    };

    const fetchCveList = (url) =>{
        setTableLoading(true);
        makeAlertMessage("Please wait while model is evaluating source code", "info");
        fetch(url,{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(current_working_directory)
        })
        .then(response => {
            // history.go(-1);
            setTableLoading(false);
            return response.json();
          }).then(data => {
            var obj = JSON.parse(data);
            setUploading(false);
            setRows(obj);
            setUploadText("Source Code Loaded");
            setUploaded(true);
            makeAlertMessage("Model Evaluation Successful", "success");
          }).catch(err => {
            if (err.name === 'AbortError') {
              console.log('fetch aborted');           
              makeAlertMessage('fetch aborted', "error");
            } else {
              // auto catches network / connection error
                setUploading(false);
                setRows(null);
                // setUploadText("Upload source code");
                // upload_button = document.getElementById("uploadButton");
                // upload_button.disabled = false;
                console.log(err.message);
                makeAlertMessage(err.message, "error");
            }
          });
    };

    const handleModel = (e) =>{
        if(e.target.control.id === "sysevr"){
            fetchCveList("http://127.0.0.1:8000/detection_api/cve-list/sysevr/");
        }else{
            fetchCveList("http://127.0.0.1:8000/detection_api/cve-list/vuldeepecker/");
        }
    };

    const handleSelection = (selectedRows) =>{
        setSelectedRows(selectedRows);
    }; 


    const handleDownload = () =>{
        var data = selectedRows;
        var arr = rows.filter(item => {
            return data.includes(item.id.toString());
        });
        var fileDownload = require('js-file-download');
        fileDownload(JSON.stringify(arr), 'Detections.json');
    };

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
                    <h3 className="display-4 row offset-md-3">Vulnerability Detection</h3>
                    <p className="lead row offset-md-3">Select a C/C++ code from your pc and detect vulnerability!!!</p>
                </div>
            </div>
            <input type="file" id="fileUpload" name="codes" style={{display:"none"}} webkitdirectory="../../" mozdirectory="../../" onChange={handleFileUpload}/>
            <button className="btn btn-lg my_upload_button" id="uploadButton" onClick={uploadCode}> <span className="material-icons">cloud_upload</span> {uploadText}</button>
            {uploading && <Box m={2}><CircularProgress/></Box>}
            {uploaded && 
            <div className="container row ">
                <div className="input-group m-3">
                    <div className="input-group-prepend">
                        <span className="input-group-text my_delete_button" id="basic-addon1">Remove Source Code</span>
                    </div>  
                    <div className="input-group-append">
                        <button type="button" id="searchButton" className="btn btn-outline-secondary my_delete_button border-0" onClick={undoUpload}>
                            <span className="material-icons">close</span>
                        </button>
                    </div>
                </div>
                <div className="btn-group btn-group-toggle col-md-3 float-left" data-toggle="buttons" >
                    <div className="input-group-append">
                        <div className="input-group-text" id="btnGroupAddon">Select a Detection Model</div>
                    </div>
                    <label className="btn btn-secondary" onClick={(e) => handleModel(e)}>
                        <input type="radio" name="options1" id="sysevr" />SySeVR Model
                    </label>
                    <label className="btn btn-secondary" onClick={(e) => handleModel(e)}>
                        <input type="radio" name="options2" id="vuldeep" />VulDeePecker Model
                    </label>
                </div>
            </div>
            }

            {tableLoading && <Box m={2}><CircularProgress/></Box>}            
            {!tableLoading && <Box m={2}><VulTable rows={rows}  handleSelection={handleSelection}/></Box>}
            {rows && !tableLoading &&
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

export default Detection;