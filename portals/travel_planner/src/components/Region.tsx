import React from 'react';
import RegionCard from './RegionCard'
import {regions} from '../data'


  export interface Region {
    regionName: string;
    regionImage: string;
    regionSummary: string;
  }


function Region(){
    return (
        <div className="regions">
            <h2 className="header">Regions</h2>
            <div className="regions-list">
                {regions.map((region, index) => (
                <RegionCard 
                key={index} 
                title={region.regionName} 
                description={region.regionSummary}
                image={region.regionImage}
                />
            ))} 
            </div>
        </div>
    )
};

export default Region;