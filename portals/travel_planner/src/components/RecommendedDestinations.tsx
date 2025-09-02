import React from 'react';
import DestinationCard from './DestinationCard'
import santorini from './assets/santorini.jpg'
import kyoto from './assets/kyoto.jpg'
import maui from './assets/maui.jpg'

const recommendedDestinations = [
    { 
        title: 'Santorini', 
        description: 'Beautiful island in the Aegean Sea with stunning sunsets.', 
        image: santorini
    },
    { 
        title: 'Kyoto', 
        description: 'Ancient city in Japan known for its temples and gardens.',
        image: kyoto
    },
    { 
        title: 'Maui', 
        description: 'Popular Hawaiian island known for its beaches and waterfalls.',
        image: maui
    },
];

function RecommendedDestinations(){
    return (
        <div className="recommended-destinations">
            <h2 className="header">Recommended Destinations</h2>
            <div className="destinations-list">
                {recommendedDestinations.map((destination, index) => (
                <DestinationCard 
                key={index} 
                title={destination.title} 
                description={destination.description}
                image={destination.image}
                />
            ))} 
            </div>
        </div>
    )
};

export default RecommendedDestinations;