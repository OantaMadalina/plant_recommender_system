import Heading from '../components/Heading';
import UploadButton from '../components/UploadButton';
import DownloadButton from '../components/DownloadButton';
import HoroscopeStatistics from '../components//HoroscopeStatistics';


const Admin = () => {
  
  return (
    <div className='app-container'>
      <div className='heading-container'>
        <Heading/>
      </div>
      <div className='upload-button-container'>
        <UploadButton/>
      </div>
      <div className='download-button-container'>
        <DownloadButton/></div>
      <div className='statistics-container'>
        <HoroscopeStatistics/></div>
      </div>
  );
}

export default Admin;
