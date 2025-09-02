import React from 'react';
import logo from './logo.svg';
import './App.css';
import Header from './components/Header';
import Region from './components/Region';
import RecommendedDestinations from './components/RecommendedDestinations';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegionDetail from './components/RegionDetail';
import { regions } from './data'; 


function App() {
  return (
    <Router>
      <div>
        <Header />
      <main>
        <Routes>
          {/*Main Route */}
          <Route path="/" element={<Home />} />
          {/*Detail Route */}
          <Route path="region/:regionTitle" element={<RegionDetail />} />
        </Routes>
      </main>
      </div>
    </Router>
  );
};

const Home: React.FC = () => {
  return(
    <>
    <Region />
    <RecommendedDestinations />
  </>
  );
};


export default App;
