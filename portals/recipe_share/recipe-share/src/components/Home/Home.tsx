import React, { FC } from 'react';
import styles from './Home.module.css';
import foodImage from '../../images/food.jpg';

const Home: FC = () => {
    return (
        <div className={styles.home}>
          <h2>Welcome to PlatePal</h2>
          <p>Your personal recipe manager.</p>
          <img src={foodImage} alt="Delicious food" className={styles.image} />
        </div>
    );
};

export default Home;
