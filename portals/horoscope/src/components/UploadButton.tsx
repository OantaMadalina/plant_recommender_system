import React, { useState, ChangeEvent } from 'react';
import styles from "./UploadButton.module.css";
import axios, { AxiosError } from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import environment from '../environment'

interface IUploadButtonProps {
  handleClick?: any;
}

const UploadButton: React.FC<IUploadButtonProps> = () => {

  const fileInput = React.useRef<any>();

  const uploadHoroscopeData = async () => {
    if (fileInput?.current?.files.length === 1) {
      const file = fileInput.current.files[0];
      try {
        await axios.post(`${environment.apiPath}horoscopeUpload/${file.name}`, file, {...environment.params});
        toast.success('File successfully uploaded', 
          {position: "bottom-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "dark",
          });
      } catch (err: AxiosError | any) {
        toast.error('File failed to upload', 
          {position: "bottom-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
          });
      } finally {
        if (fileInput.current) {
          fileInput.current.value = '';
        }
      }
    }
  };

  return (
      <>
        <button onClick={() => fileInput?.current?.click()} className={styles["upload-button"]}>Upload Predictions File</button>
        <input style={{ display: 'none' }} type='file' ref={fileInput} onChange={uploadHoroscopeData}/>
        <ToastContainer/>
      </>
    )
  }

export default UploadButton;
