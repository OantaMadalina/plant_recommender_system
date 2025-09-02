import React, { FC } from 'react';
import styles from './MyRecipes.module.css';

const MyRecipes: FC = () => {
  return (
    <div className={styles.myRecipes}>
      <h2>My Recipes</h2>
      <p>Here are your saved recipes.</p>
    </div>
  );
};

export default MyRecipes;
