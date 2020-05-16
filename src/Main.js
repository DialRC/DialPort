import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Upload from './Upload';
import App from './App';


export default function Main() {
  return (
    <Router>
      <div>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/">
            <App />
          </Route>
          <Route path="/submit">
            <Upload />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}
