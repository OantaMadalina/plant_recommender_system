import { useState } from 'react';
import { useEffect } from 'react';
import SignsAsButtons from './SignsAsButtons'
import HoroscopeTypeButtons from './HoroscopeTypeButtons'
import environment from '../environment'
import styles from "./Horoscope.module.css";
import axios from 'axios';

interface HoroscopeProps {
    sign: string;
    type: string;
}

const Horoscope: React.FC<HoroscopeProps> = ({sign, type}) => {
    const [horoscope, setHoroscope] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true)
    useEffect(() => {
        const fetchHoroscope = async () => {
            setLoading(true);
            try{
                const encodedSign = encodeURIComponent(sign);
                const encodedType = encodeURIComponent(type);
                const response = await axios.get(`${environment.apiPath}horoscope?sign=${sign.toLowerCase()}&type=${type.toLowerCase()}`, {...environment.params});
                setHoroscope(response.data)
            }catch (error){
                console.error("Error fetching response: ", error)
            }finally{
                setLoading(false);
            }
        };
        fetchHoroscope();
    }, [sign, type]);

    if (loading){
        return <h1 className={styles["horoscope"]}>Loading...</h1>
    }

    return (
        <div className={styles["horoscope"]}>
            <h1>{horoscope}</h1>
        </div>
    )
}

export default Horoscope;