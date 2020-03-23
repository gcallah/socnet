import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import Home from './components/Home';
import CreateAlert from './components/CreateAlert';
import ThreadView from './components/ThreadView';
import FilterForm from './components/FilterForm';

function App() {
  return (
    <div className="App">
      <BrowserRouter  basename="/socnet/webapp.html">
        <Switch>
            <Route exact path="/" component={FilterForm} />
            <Route exact path="/alerts" component={Home} />
            <Route exact path="/createAlert" component={CreateAlert} />
            <Route exact path="/thread/:id" component={ThreadView} />  
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
