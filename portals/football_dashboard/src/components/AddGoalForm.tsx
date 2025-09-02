import React, { useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
import { Scorer } from '../models/interfaces';

interface AddGoalFormProps {
  onAddGoal: (minute: number, setFunction: React.Dispatch<React.SetStateAction<Scorer[]>>) => void;
  setFunction: React.Dispatch<React.SetStateAction<Scorer[]>>
}

const AddGoalForm: React.FC<AddGoalFormProps> = ({ onAddGoal, setFunction }) => {
  const [minute, setMinute] = useState<number | ''>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [placeholder, setPlaceholder] = useState<string>("Minute");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;

    if (/^\d*$/.test(value) && (value === '' || (Number(value) >= 1 && Number(value) <= 90))) {
      setMinute(Number(value));
      setErrorMessage(null);
    }
  };

  const handleInputFocus = () => {
    setPlaceholder("");
  };

  const handleInputBlur = () => {
    if (minute === "") {
      setPlaceholder("Minute");
    }
  }

  const handleAddGoal = () => {
    if (minute !== '' && minute >= 1 && minute <= 90) {
      onAddGoal(minute, setFunction);
      setMinute('');
      console.log(`Goal added for minute: ${minute}`);
    } else {
      setErrorMessage('Enter a minute BETWEEN 1 and 90.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
      {errorMessage && (
        <span style={{ color: '#ff0000', fontSize: 'small', fontWeight: 'bold' }}>
          {errorMessage}
        </span>
      )}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <input
          type="number"
          value={minute}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onBlur={handleInputBlur}
          placeholder={placeholder}
          style={{
            backgroundColor: 'white',
            borderRadius: '10px',
            border: '1px solid #ccc',
            padding: '5px 10px',
            width: '100px',
            height: '30px',
            textAlign: 'center',
            fontSize: 'large'
          }}
        />
        <button
          onClick={handleAddGoal}
          style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: 'green',
            color: 'white',
            border: '1px solid green',
            padding: '5px 5px 5px 10px',
            textAlign: 'center',
            borderRadius: '10px',
            height: '30px',
            cursor: 'pointer',
        }}
        >
          <span style={{ fontWeight: 'bolder',  }}>Add Goal</span>
          <AddIcon style={{marginLeft: '5px'}}/>
        </button>
      </div>
    </div>
  );
};

export default AddGoalForm;
