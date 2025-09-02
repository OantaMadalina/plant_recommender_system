import React from 'react'

interface DestinationCardProps {
    title: string;
    description: string;
    image: string;
}

function DestinationCard({title, description, image}:DestinationCardProps){
    return (
        <div className="destination-card">
            <h3>{title}</h3>
            <img src={image} alt={title} className="destination-image" />
            <p>{description}</p>
        </div>
    )

}

export default DestinationCard;