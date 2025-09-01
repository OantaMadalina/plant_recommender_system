import React from 'react';
import './Navbar.css';

export const Navbar: React.FC = () => {
  return (
    <div className="NavbarContainer">
      <h1 className="Logo">Plant World</h1>
      <div className="NavLinks">
        <button className="NavLink">Home</button>
        <button className="NavLink">Basket</button>
      </div>
    </div>
  );
};
