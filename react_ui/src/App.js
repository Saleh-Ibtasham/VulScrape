import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Detection from './components/Detection';
import Prediction from './components/Prediction';

function App() {
  return (
    <Router>
      <div className="App container-fluid">
        <Navbar/>
        <div className="container-fluid">
          <Switch>
            <Route exact path="/">
              <Detection/>
            </Route>
            <Route path="/prediction">
              <Prediction/>
            </Route>
          </Switch>
        </div>
      </div>
    </Router>

  );
}

export default App;
