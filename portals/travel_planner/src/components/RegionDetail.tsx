import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import CountryCard from './CountryCard'
import {regionsData} from '../data'

const RegionDetail: React.FC = () => {
    const { regionTitle } = useParams<{ regionTitle: string }>();
    const region = regionsData.find(r => r.regionName === regionTitle);
    if (!region) {
        return <div>Region not found</div>
    }

    const descriptionParts = region.regionDescription.split('<br>');

    return (
        <div className="region-detail">
            <h1>{region.regionName}</h1>
            <img src={region.regionImage} alt={region.regionName} className="region-image" />
            {descriptionParts.map((part, index) => (
                <p key={index} className="region-description">
                    {part}
                </p>
            ))}
            <h2>Countries to visit in {region.regionName}</h2>
            <div className="country-list">
                {region.regionCountries.map((country) => (
                    <CountryCard key={country.countryName} title={country.countryName} image={country.countryImage} />
                ))}
            </div>
        </div>
    );
};

export default RegionDetail;