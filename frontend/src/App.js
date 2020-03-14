import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import Home from './components/Home';
import ThreadView from './components/ThreadView';
import FilterForm from './components/FilterForm';
import CreartAlert from './components/CreateAlerts'

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
            <Route exact path="/" component={FilterForm} />
            <Route exact path="/alerts" component={Home} />
            <Route exact path="/createAlert" component={CreartAlert} />
            <Route exact path="/thread/:id" component={ThreadView} />  
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
