import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";

import Login from './pages/Login'
import Profile from './pages/Profile';
import Register from './pages/Register';
import axios from 'axios';


axios.defaults.baseURL = "http://172.26.17.196:12060/api"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;
