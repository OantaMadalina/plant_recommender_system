import React from 'react'
interface CountryCardProps {
    title: string;
    image: string;
}

function CountryCard({title, image}:CountryCardProps){
    return (
        <div className="country-card">
            <img src={image} alt={title} className="country-image" />
            <h3 className="country-title">{title}</h3>
        </div>
    )

}

export default CountryCard;