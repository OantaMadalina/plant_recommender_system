import { SetStateAction, useState } from 'react';
import styles from './UserReview.module.css'

const DEFAULT_COUNT = 5;
const DEFAULT_ICON = "★";
const DEFAULT_UNSELECTED_COLOR = "gray";
const DEFAULT_COLOR = "orange";

interface UserReviewProps{
  setRating: React.Dispatch<React.SetStateAction<number>>; /* Rating */
  rating: number;
  setTemporaryRating: React.Dispatch<React.SetStateAction<number>>; /* Hover */
  temporaryRating: number;
}

const UserReview: React.FC<UserReviewProps> = ({setRating, rating, setTemporaryRating, temporaryRating}) => {
    let stars = Array(DEFAULT_COUNT).fill(DEFAULT_ICON) /* Prop or default count / icon */

    const handleClick = (rating: SetStateAction<number>) => {
        setRating(rating);
    }
    
    return (
      <div className={styles['user-stars-review']}>
        {stars.map((item, index) => {
            /* Index - 0 to 4 rating set to 1 so index 0 lower than 1 color the first star */
            const isActiveColor = (rating || temporaryRating) && (index < rating || index < temporaryRating);
            
            let elementColor = '';

            if (isActiveColor){
                elementColor = DEFAULT_COLOR;
            }else{
                elementColor = DEFAULT_UNSELECTED_COLOR;
            }
            return (<div 
                className={styles['star']} 
                key={index} 
                style={{
                    fontSize: "30px", 
                    color: elementColor, 
                    filter: `${isActiveColor ? "grayscale(0%)" : "grayscale(100%)"}`}} 
                    onMouseEnter={() => setTemporaryRating(index + 1)} 
                    onMouseLeave={() => setTemporaryRating(0)}
                    onClick={() => handleClick(index + 1)}>
                    {DEFAULT_ICON}
                </div>)
        })}
      </div>
    )
  }

export default UserReview;