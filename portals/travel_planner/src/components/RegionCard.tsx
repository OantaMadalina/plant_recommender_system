import React from 'react'
import { useNavigate } from 'react-router-dom';

interface RegionCardProps {
    title: string;
    description: string;
    image: string;
}

function RegionCard({title, description, image}:RegionCardProps){
    const navigate = useNavigate();
    const handleExploreClick = () => {
        navigate(`/region/${title}`);
    };

    return (
        <div className="region-card">
            <img src={image} alt={title} className="region-image" />
            <h3>{title}</h3>
            <p>{description}</p>
            <button className="button" onClick={handleExploreClick}>Explore</button>
        </div>
    )

}

export default RegionCard;