import { Tooltip } from '@material-ui/core';
import { DataGrid } from '@material-ui/data-grid';

function VulPredTable(props) {

  const showCustomTooltip = (params) => {
    return(
      <div className="my_tooltip_grid" >
        {params.value}
      </div>
    );
  };

  const columns = [
    { field: 'id', hide: true },
    { field: 'ID', headerName: 'CVE-ID', width: 300 },
    { field: 'DESC', headerName: 'Description', width: 500, renderCell: (params) => (
        <Tooltip title={showCustomTooltip(params)} 
        enterDelay={500} 
        leaveDelay={200}
        placement='right-end'>
          <span className="table-cell-trucate">{params.value}</span>
        </Tooltip>
    ),},
    { field: 'VULN_TYPE', headerName: 'Vulnerability Type', width: 300 ,  renderCell: (params) => (
      <Tooltip title={showCustomTooltip(params)} 
      enterDelay={500} 
      leaveDelay={200}
      placement='right-end'>
        <span className="table-cell-trucate">{params.value}</span>
      </Tooltip>
  ),},
    { field: 'Exploited', headerName: 'Exploited', width: 150 },
    { field: 'Exploited_score', headerName: 'Risk Probability (%)', width: 300 },
  ];
  
  const rows = props.rows;
  const handleSelection = props.handleSelection;
  
  return (
    <div>
      {rows && 
        <div style={{ height: 400, width: '100%' }}>
        <DataGrid rows={rows} columns={columns} pageSize={5} checkboxSelection 
          onSelectionModelChange={(newSelection) => {handleSelection(newSelection.selectionModel);}}
        />
        </div>
      }
    </div>
  );
}

export default VulPredTable