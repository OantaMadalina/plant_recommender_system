import React from 'react'
import ReactCountryFlag from 'react-country-flag'
import lookup from 'country-code-lookup';

interface CustomCountryFlagProps {
    nationality: string;
    height: string;
    width: string;
}

const CustomCountryFlag: React.FC<CustomCountryFlagProps> = ({ nationality, height, width }) => {
    const ukNationalities = ['England', 'Scotland', 'Wales', 'Northern Ireland'];

    return (
        <ReactCountryFlag
            countryCode={lookup.byCountry(ukNationalities.includes(nationality) ? 'United Kingdom' : nationality)?.iso2 ?? 'NI'}
            svg
            style={{
                width: width,
                height: height,
                border: '1px solid black',
                borderRadius: '3px'
            }}
            title={nationality}>
        </ReactCountryFlag>
    )
}

export default CustomCountryFlag
