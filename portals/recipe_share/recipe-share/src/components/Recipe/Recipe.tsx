import React, { FC } from 'react';
import { useParams } from 'react-router-dom';
import styles from './Recipe.module.css';

const Recipe: FC = () => {
    const { recipeId } = useParams<{ recipeId: string }>();

    return (
        <div className={styles.recipe}>
          <h2>Recipe Details</h2>
          <p>Details for recipe ID: {recipeId}</p>
        </div>
    );
};

export default Recipe;
