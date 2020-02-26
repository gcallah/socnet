import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { HashRouter, Route, Switch, BrowserRouter} from 'react-router-dom';
import Home from './components/Home';
import CreateAlert from './components/CreateAlert';
import ThreadView from './components/ThreadView';
import FilterForm from './components/FilterForm';
import ThreadAlerts from './components/ThreadAlerts';

function App() {
  return (
    <div className="App">
      <HashRouter>
        <Switch>
            <Route exact path="/main" component={Home} />
            <Route exact path="/createAlert" component={CreateAlert} />
            <Route exact path="/thread/:id" component={ThreadView} />
            <Route exact path="/(|filterAlert)" component={FilterForm} />  
        </Switch>
      </HashRouter>
    </div>
  );
}

export default App;
