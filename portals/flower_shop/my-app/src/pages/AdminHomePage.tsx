// src/components/AdminHomePage.tsx
import React, { useState } from 'react';
import './AdminHomePage.css';
import { Navbar } from '../components/Navbar';
import { ProductList } from '../components/ProductList';
import AddProductModal from '../components/AddProductModal';
import plantsImage from '../components/plants-hanging-home.png'; // Adjust the path as necessary

const AdminHomePage: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleAddProductClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleSubmitProduct = (product: any) => {
    console.log('New Product:', product);
    // Add logic to save the product
  };

  return (
    <div className="AppContainer">
      <img src={plantsImage} alt="Plants" className="HeaderImage" />
      <Navbar />
      <h1>Products <span>you may also like</span></h1>
      <button className="AddProductButton" onClick={handleAddProductClick}>Add new product</button>
      <ProductList />
      {isModalOpen && <AddProductModal onClose={handleCloseModal} onSubmit={handleSubmitProduct} />}
    </div>
  );
};

export default AdminHomePage;
