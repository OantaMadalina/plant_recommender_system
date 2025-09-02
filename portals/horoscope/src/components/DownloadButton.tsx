import { useState } from 'react';
import styles from "./DownloadButton.module.css";
import axios from 'axios';
import environment from '../environment'

const DownloadButton: React.FC = () => {
  const downloadFile = async (type: 'weekly' | 'monthly') => {
    try{
      const response = await axios.post(`${environment.apiPath}downloadHoroscopeReports/${type}`, {type}, {...environment.params});
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a'); /* Temporary link */
      link.href = url;
      link.setAttribute('download', `latest-${type}-file.csv`)
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    }catch (error){
      console.error('Error downloading the file: ', error)
    }
    };
    return (
      <>
        <button className={styles["download-button"]} onClick={() => downloadFile('weekly')}>Download Weekly Report</button>
        <button className={styles["download-button"]} onClick={() => downloadFile('monthly')}>Download Monthly Report</button>
      </>
    )
  }

export default DownloadButton;
