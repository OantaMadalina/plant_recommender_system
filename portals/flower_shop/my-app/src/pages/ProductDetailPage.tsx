import React from 'react';
import { useParams } from 'react-router-dom';
import './ProductDetailPage.css';
import { Navbar } from '../components/Navbar';

interface Product {
  id: number;
  name: string;
  price: string;
  location: string;
  imageUrl: string;
}

const products: Product[] = [
  {
    id: 1,
    name: 'Monstera Deliciosa',
    price: '$5.99',
    location: 'San Juan Capistrano, CA',
    imageUrl: 'https://verdena.ro/cdn/shop/products/monster-deliciosa-albo-variegata-50-cm-597492.jpg?v=1707641586&width=675'
  },
  {
    id: 2,
    name: 'String Of Teardrops | String Of Pearls',
    price: '$12.99',
    location: 'Huntington Beach, CA',
    imageUrl: 'https://www.houseplant.co.uk/cdn/shop/products/20200826_163434.jpg?v=1663696559&width=1445'
  },
  {
    id: 3,
    name: 'Boston Fern | Green Moment',
    price: '$12.99',
    location: 'Huntington Beach, CA',
    imageUrl: 'https://leafculture.co.uk/cdn/shop/files/Nephrolepis-Green-Moment-Boston-Fern-Oz-101698595.jpg?v=1704820785'
  }
];

const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  if (!id) {
    return <div>Product not found</div>;
  }

  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div className="ProductDetailContainer">
      <Navbar />
      <div className="ProductDetail">
        <img src={product.imageUrl} alt={product.name} />
        <div className="ProductInfo">
          <h1>{product.name}</h1>
          <p>{product.price}</p>
          <p>{product.location}</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
