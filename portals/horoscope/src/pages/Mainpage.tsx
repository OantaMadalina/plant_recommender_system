import { useState } from 'react';
import Heading from '../components/Heading';
import SignsAsButtons from '../components/SignsAsButtons';
import HoroscopeTypeButtons from '../components/HoroscopeTypeButtons';
import UserReview from '../components/UserRevies';
import SubmitButton from '../components/SubmitButton';
import Horoscope from '../components/Horoscope'

const Mainpage: React.FC = () => {

  const [sign, setSign] = useState<string>('');
  const [type, setType] = useState<string>('');
  const [rating, setRating] = useState<number>(0);
  const [temporaryRating, setTemporaryRating] = useState<number>(0);

  return (
    <div className='app-container'>
      <div className='heading-container'><Heading/></div>
      <div className='horoscope-type-container'><HoroscopeTypeButtons setType={setType} selectedType={type}/></div>
      <div className='signs-container'><SignsAsButtons setSign={setSign} selectedSign={sign}/></div>
      <div className='user-review-container'>
        <UserReview setRating={setRating} rating={rating} setTemporaryRating={setTemporaryRating} temporaryRating={temporaryRating}/>
        <SubmitButton sign={sign} type={type} rating={rating}/>
        </div>
      <div className='horoscope-container'><Horoscope sign={sign} type={type}/></div>
    </div>
  );
}

export default Mainpage;
