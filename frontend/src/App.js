import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import CreateAlert from './components/CreateAlert';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route exact path="/" component={ Home } />
          <Route exact path="/createAlert" component={ CreateAlert } />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
