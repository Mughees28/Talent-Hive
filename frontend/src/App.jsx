import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import Signup from "./components/Signup.jsx";
import Login from "./components/Login.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Navbar from "./components/Navbar";
import PostTask from "./components/PostTask";

const ProtectedRoute = ({ children }) => {
  const token = useSelector((state) => state.auth.token) || localStorage.getItem("token");
  return token ? children : <Login />;
};

function App() {
  return (
    <Router>
       <Navbar />
      <Routes>
        
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
             
              <Dashboard />
            </ProtectedRoute>
          }
          
        />
        <Route path="/post-task" element={<ProtectedRoute><PostTask /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
