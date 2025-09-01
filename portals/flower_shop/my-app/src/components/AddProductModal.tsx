import React, { useState } from 'react';
import './AddProductModal.css';

interface AddProductModalProps {
  onClose: () => void;
  onSubmit: (product: any) => void;
}

const AddProductModal: React.FC<AddProductModalProps> = ({ onClose, onSubmit }) => {
  const [idPlant, setIdPlant] = useState('');
  const [namePlant, setNamePlant] = useState('');
  const [pricePlant, setPricePlant] = useState('');
  const [quantityPlant, setQuantityPlant] = useState('');
  const [descriptionPlant, setDescriptionPlant] = useState('');
  const [image, setImage] = useState<File | null>(null);

  const handleSubmit = () => {
    const product = {
      idPlant,
      namePlant,
      pricePlant,
      quantityPlant,
      descriptionPlant,
      image,
    };
    onSubmit(product);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Add New Product</h2>
        <form>
          <label>ID Plant</label>
          <input type="text" value={idPlant} onChange={(e) => setIdPlant(e.target.value)} />
          <label>Name</label>
          <input type="text" value={namePlant} onChange={(e) => setNamePlant(e.target.value)} />
          <label>Price</label>
          <input type="text" value={pricePlant} onChange={(e) => setPricePlant(e.target.value)} />
          <label>Quantity</label>
          <input type="text" value={quantityPlant} onChange={(e) => setQuantityPlant(e.target.value)} />
          <label>Description</label>
          <textarea value={descriptionPlant} onChange={(e) => setDescriptionPlant(e.target.value)} />
          <label>Upload an image</label>
          <input type="file" onChange={(e) => setImage(e.target.files ? e.target.files[0] : null)} />
          <button type="button" onClick={handleSubmit}>Submit</button>
          <button type="button" onClick={onClose}>Cancel</button>
        </form>
      </div>
    </div>
  );
};

export default AddProductModal;
