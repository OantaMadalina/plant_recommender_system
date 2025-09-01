import React, { useState } from 'react';
import './UserHomePage.css';
import { Navbar } from '../components/Navbar';
import { ProductList } from '../components/ProductList';
import AddProductModal from '../components/AddProductModal';

const AdminHomePage: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleSubmitProduct = (product: any) => {
    console.log('New Product:', product);
    // Add logic to save the product
  };

  return (
    <div className="AppContainer">
      <Navbar />
      <h1>Products <span>you may also like</span></h1>
      <ProductList />
      {isModalOpen && <AddProductModal onClose={handleCloseModal} onSubmit={handleSubmitProduct} />}
    </div>
  );
};

const Button = () => {

  const handleClick = () => {

    alert('Button clicked!');

  };

 

  return <button onClick={() => handleClick()}>Click Me</button>;

};

export default AdminHomePage;
