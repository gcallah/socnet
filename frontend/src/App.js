import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import ViewAlerts from './components/ViewAlerts';
import CreateAlert from './components/CreateAlert';
import AlertDetail from './components/AlertDetail';
import SearchAlerts from './components/SearchAlerts';

/*
 * 2) FilterForm --> SearchAlerts
 * 3) Home --> ViewAlerts
 * 4) ThreadAlerts --> AlertsTable
 */

function App() {
  return (
    <div className="App">
      <BrowserRouter  basename="/socnet/webapp.html#">
        <Switch>
            <Route exact path="/" component={SearchAlerts} />
            <Route exact path="/alerts" component={ViewAlerts} />
            <Route exact path="/createAlert" component={CreateAlert} />
            <Route exact path="/thread/:id" component={AlertDetail} />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
