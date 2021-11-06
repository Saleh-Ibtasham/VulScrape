import { useState } from "react";
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { useHistory } from "react-router-dom";

const Navbar = () => {
    var inital_value = 0;
    const history = useHistory();
    if (window.performance) {
        if(performance.navigation.type === performance.navigation.TYPE_RELOAD){
            if(history.location.pathname.includes("prediction")){
                inital_value = 1;
            }
        }  
    }
    const [value, setValue] = useState(inital_value);


    const a11yProps = (index) => {
        return {
            id: `simple-tab-${index}`,
            'aria-controls': `simple-tabpanel-${index}`,
        };
    };

    const handleChange = (event, newValue) => {
        if(newValue === 0){
            history.push('/')
        }else{
            history.push('/prediction')
        }
        setValue(newValue);
    };
    return ( 
        <AppBar position="static">
            <Toolbar className="my_toolbar">
                <Typography variant="h6">
                VulScrape
                </Typography>
                <Tabs value={value} onChange={handleChange} aria-label="simple tabs example" className="links">
                    <Tab label="Detection" {...a11yProps(0)} className="link btn"></Tab>
                    <Tab label="Prediction" {...a11yProps(1)} className="link btn"></Tab>
                </Tabs>
            </Toolbar>
        </AppBar>
    );
}
export default Navbar;