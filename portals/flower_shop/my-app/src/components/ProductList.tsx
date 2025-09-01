import React, { useEffect, useState } from 'react';
import './ProductList.css';
import { ProductCard } from './ProductCard';
import { Link } from 'react-router-dom';
import axios from 'axios';
import environment from "../environment";

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

export const ProductList: React.FC = () => {
  const [products, setProducts] = useState<PlantResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        console.log('Fetching products from API...');
        const response = await axios.get(
          `${environment.apiPath}plantData`,
          {
            ...environment.params,
          }
        );
        console.log('API response:', response.data);
        response.data.forEach((product: PlantResponse) => {
          console.log('Signed Photo URL:', product.signedPhotoUrl);
        });
        setProducts(response.data);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Failed to fetch products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleDelete = async (idPlant: number) => {
    try {
      const response = await axios.delete(
        `${environment.apiPath}plant/${idPlant}`,
        {
          ...environment.params,
        }
      );
      setProducts(products.filter(product => product.plant.idPlant !== idPlant));
    } catch (err) {
      console.error('Error deleting product:', err);
      setError('Failed to delete product');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="ProductListContainer">
      {products.map(product => (
        <div key={product.plant.idPlant} className="ProductLink">
          <ProductCard product={product} onDelete={handleDelete} />
        </div>
      ))}
    </div>
  );
};
