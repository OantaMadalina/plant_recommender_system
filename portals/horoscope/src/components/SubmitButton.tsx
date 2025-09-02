import styles from "./SubmitButton.module.css";
import environment from '../environment'
import axios, { AxiosError } from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface SubmitReviewProps{
  sign: string;
  type: string;
  rating: number;
}

const SubmitButton: React.FC<SubmitReviewProps> = ({sign, type, rating}) => {
  const encodedSign = encodeURIComponent(sign);
  const encodedType = encodeURIComponent(type);
  const encodedReview = encodeURIComponent(rating);
  const uploadReview = async () => {
    try{
        await axios.post(`${environment.apiPath}horoscopeUploadRating?sign=${sign.toLowerCase()}&type=${type.toLowerCase()}&rating=${rating}`, '', {...environment.params});
        toast.success('Rating successfully uploaded', 
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
        toast.error('Rating failed to upload', 
          {position: "bottom-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
          });
    }
};
    return (
      <>
        <ToastContainer/>
        <button className={styles["submit-button"]} onClick={() => uploadReview()}>Submit</button>
      </>
    )
  }

export default SubmitButton;
