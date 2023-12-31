import React from 'react';
import './App.css';
import DefaultDashboardView from './features/DefaultDashboard/DefaultDashboardView';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <div className="App" style={{backgroundColor: "#000000"}}>
          <Route path='/' component={DefaultDashboardView}/>
          <Route path='/democrats' component={DefaultDashboardView}/> 
          <Route path='/republicans' component={DefaultDashboardView}/>
        </div>
      </Switch>
    </Router>
  );
}

export default App;
