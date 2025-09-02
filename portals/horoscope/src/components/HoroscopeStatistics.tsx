import { useState } from 'react';
import { useEffect } from 'react';
import SignsAsButtons from './SignsAsButtons'
import HoroscopeTypeButtons from './HoroscopeTypeButtons'
import environment from '../environment'
import styles from "./Horoscope.module.css";
import axios from 'axios';


const HoroscopeStatistics: React.FC = () => {
    const [horoscopeStats, setHoroscopeStats] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true)
    useEffect(() => {
        const fetchHoroscopeStatistics = async () => {
            try{
                const response = await axios.get<string[]>(`${environment.apiPath}horoscopeStats`, {...environment.params});
                setHoroscopeStats(response.data)
            }catch (error){
                console.error("Error fetching response: ", error)
            }finally{
                setLoading(false);
            }
        };
        fetchHoroscopeStatistics();
    }, []);

    if (loading){
        return <div className={styles["horoscope"]}>Loading...</div>
    }

    return (
        <div className={styles["horoscope"]}>
            {horoscopeStats.map((stats) => (<p key={stats}>{stats}</p>))}
        </div>
    )
}

export default HoroscopeStatistics;