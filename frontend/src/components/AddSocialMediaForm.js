import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddSocialMediaForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        mediaName: '',
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
        setMessage('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await axios.post('http://localhost:5050/add-socialmedia', {
                mediaName: formData.mediaName
            });
            setMessage('Success: Social media platform added!');
            handleClear();
        } catch (error) {
            if (error.response?.data?.error) {
                setMessage(`Error: ${error.response.data.error}`);
                handleClear();
            } else {
                setMessage('Error: Unable to add social media platform.');
                handleClear();
            }
        } finally {
            setIsLoading(false);
        }
    };


    const handleClear = () => {
      setFormData({ mediaName: '' });

      // Clear the success or error message after 3 seconds
      setTimeout(() => {
        setMessage('');
      }, 3000);
    };


    const isFormValid = formData.mediaName;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add Social Media Platform</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    name="mediaName" 
                    placeholder="Media Name * (e.g., Twitter, Facebook)" 
                    value={formData.mediaName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <div style={formStyles.buttonContainer}>
                    <button 
                        type="submit" 
                        disabled={!isFormValid || isLoading}
                        style={{ 
                            ...formStyles.submitButton,
                            backgroundColor: isFormValid ? '#4CAF50' : '#cccccc',
                            cursor: isFormValid ? 'pointer' : 'not-allowed'
                        }}
                    >
                        {isLoading ? 'Adding...' : 'Add Social Media'}
                    </button>
                    <button 
                        type="button"
                        onClick={handleClear}
                        style={formStyles.clearButton}
                    >
                        Clear Form
                    </button>
                </div>
                {message && (
                  <p style={{
                    ...formStyles.message,
                    backgroundColor: message.includes('Error')
                      ? '#ffebee'
                      : message.includes('Success')
                        ? '#e8f5e9'
                        : 'transparent',
                    color: message.includes('Error')
                      ? '#c62828'
                      : message.includes('Success')
                        ? '#2e7d32'
                        : '#000',
                    border: '1px solid',
                    padding: '10px',
                    borderRadius: '5px',
                    marginTop: '10px'
                  }}>
                    {message}
                  </p>
                )}
            </form>
        </div>
    );
}

export default AddSocialMediaForm;
