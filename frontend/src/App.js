import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";

import Login from './pages/Login'
import Profile from './pages/Profile';
import Register from './pages/Register';
import Posting from './pages/Posting';
import axios from 'axios';


// axios.defaults.baseURL = "http://172.26.17.196:12060/api"
axios.defaults.baseURL = "http://127.0.0.1:8000/api"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/profile/:id" element={<Profile />} />
        <Route path="/register" element={<Register />} />
        <Route path="/posting/:id" element={<Posting />} />
      </Routes>
    </Router>
  );
}

export default App;
