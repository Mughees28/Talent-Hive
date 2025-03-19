import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import Signup from "./components/Signup.jsx";
import Login from "./components/Login.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Navbar from "./components/Navbar";
import PostTask from "./components/PostTask";
import TaskDetails from "./components/TaskDetails.jsx";
import TaskDetailsBid from "./components/TaskDetailsBid.jsx";
import Profile from "./components/Profile.jsx";
import ManageAgency from "./components/ManageAgency.jsx";
import TaskBreakdown from "./components/TaskBreakdown.jsx";
import ReviewPayment from "./components/ReviewPayment";
import AgencyPayment from "./components/AgencyPayment";

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
        
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>}/>
        <Route path="/post-task" element={<ProtectedRoute><PostTask /></ProtectedRoute>} />
        <Route path="/task/:taskId" element={<ProtectedRoute><TaskDetails /></ProtectedRoute>} />
        <Route path="/task/:taskId/bid" element={<ProtectedRoute><TaskDetailsBid /></ProtectedRoute>} />
        <Route path="/profile/:userId" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/manage-agency" element={<ProtectedRoute><ManageAgency /></ProtectedRoute>} />
        <Route path="/task/:taskId/taskbreakdown" element={<ProtectedRoute><TaskBreakdown /></ProtectedRoute>} />
        <Route path="/task/:taskId/payment-review" element={<ProtectedRoute><ReviewPayment /></ProtectedRoute>} />
        <Route path="agency-payment/:taskId" element={<ProtectedRoute><AgencyPayment /></ProtectedRoute>} />


      </Routes>
    </Router>
  );
}

export default App;
