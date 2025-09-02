import './App.css';
import { useState } from 'react';
import { useEffect } from 'react';
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Mainpage from './pages/Mainpage'
import Admin from './pages/Admin'


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/admin"
          element={<Admin />} />
        <Route path="/"
          element={<Mainpage />} />
      </Routes>
    </Router>
);
}

export default App;
