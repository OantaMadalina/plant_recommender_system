import React, { FC } from 'react';
import styles from './CreateRecipe.module.css';

const CreateRecipe: FC = () => {
  return (
    <div className={styles.createRecipe}>
      <h2>Create a New Recipe</h2>
      <p>Use the form below to add a new recipe.</p>
    </div>
  );
};

export default CreateRecipe;
