import React from 'react';
import './ProductCard.css';

interface Plant {
  idPlant: number;
  namePlant: string;
  pricePlant: string;
  originCountry: string;
}

interface PlantResponse {
  plant: Plant;
  signedPhotoUrl: string;
}

interface ProductCardProps {
  product: PlantResponse;
  onDelete: (idPlant: number) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onDelete }) => {
  return (
    <div className="Card">
      <img className="ProductImage" src={product.signedPhotoUrl} alt={product.plant.namePlant} onError={(e) => (e.currentTarget.src = 'fallback-image-url')} />
      <div className="ProductInfo">
        <h2 className="ProductName">{product.plant.namePlant}</h2>
        <p className="ProductPrice">{product.plant.pricePlant}$</p>
        <p className="ProductLocation">Grown in {product.plant.originCountry}</p>
        <button className="DeleteButton" onClick={() => onDelete(product.plant.idPlant)}>Delete</button>
      </div>
    </div>
  );
};
