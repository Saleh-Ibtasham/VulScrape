import { DataGrid } from '@material-ui/data-grid';
import { Tooltip } from '@material-ui/core';

// const rows = [
//   { id: "CVE-2004-2252", lastName: 'Obtain Information', firstName: 'The Windows Forms (aka WinForms) component in Microsoft .NET Framework 1.0 SP3, 1.1 SP1, 2.0 SP2, 3.0 SP2, 4, and 4.5 does not properly initialize memory arrays, which allows remote attackers to obtain sensitive information via (1) a crafted XAML browser application (XBAP)', exploited: "Yes"},
//   { id: "CVE-2013-0001", lastName: 'Execute CodeOverflow ', firstName: 'Microsoft XML Core Services (aka MSXML) 3.0, 5.0, and 6.0 does not properly parse XML content', exploited: "No"},
//   { id: "CVE-2013-0002", lastName: 'Execute CodeOverflow ', firstName: 'win32k.sys in the kernel-mode drivers in Microsoft Windows Vista SP2, Windows Server 2008 SP2, R2, and R2 SP1, Windows 7 Gold and SP1, Windows 8, Windows Server 2012,', exploited: "No"},
//   { id: "CVE-2004-0005", lastName: 'Execute Code ', firstName: 'The Print Spooler in Microsoft Windows Server 2008 R2 and R2 SP1 and Windows 7 Gold and SP1 allows remote attackers to execute arbitrary code or cause a denial of service (memory corruption) via a crafted print job', exploited: "Yes"},
//   { id: "CVE-2013-0010", lastName: 'Denial Of Service ', firstName: 'The SSL provider component in Microsoft Windows Vista SP2, Windows Server 2008 SP2, R2, and R2 SP1, Windows 7 Gold and SP1, Windows 8, Windows Server 2012,', exploited: "No"},
//   { id: "CVE-2013-3500", lastName: 'Gain privileges ', firstName: 'Use-after-free vulnerability in Microsoft Internet Explorer 8 allows remote attackers to execute arbitrary code via a crafted web site that triggers access to a deleted object', exploited: "No"},
//   { id: "CVE-2004-1181", lastName: 'Cross Site Scripting ', firstName: 'Use-after-free vulnerability in Microsoft Internet Explorer 8 allows remote attackers to execute arbitrary code via a crafted web site that triggers access to a deleted object', exploited: "No"},
// ];

function VulTable(props) {

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
    { field: 'VULNERABILITY_KIND', headerName: 'Vulnerability Type', width: 300 ,  renderCell: (params) => (
      <Tooltip title={showCustomTooltip(params)} 
      enterDelay={500} 
      leaveDelay={200}
      placement='right-end'>
        <span className="table-cell-trucate">{params.value}</span>
      </Tooltip>
  ),},
    { field: 'Source_code', headerName: 'Vulnerable FileName', width: 300 },
    { field: 'VULNERABILITY_RISK', headerName: 'Risk Probability (%)', width: 300 },
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

export default VulTable