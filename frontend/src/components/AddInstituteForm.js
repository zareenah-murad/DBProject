import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddInstituteForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        instituteName: ''
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
            await axios.post('http://localhost:5050/add-institute', formData);
            setMessage('Institute added successfully!');
            handleClear();
        } catch (error) {
            setMessage('Error adding institute.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = () => {
        setFormData({
            instituteName: ''
        });
        setMessage('');
    };

    const isFormValid = formData.instituteName;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add Institute</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    name="instituteName" 
                    placeholder="Institute Name *" 
                    value={formData.instituteName} 
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
                        {isLoading ? 'Adding...' : 'Add Institute'}
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
                        backgroundColor: message.includes('Error') ? '#ffebee' : '#e8f5e9',
                        color: message.includes('Error') ? '#c62828' : '#2e7d32'
                    }}>
                        {message}
                    </p>
                )}
            </form>
        </div>
    );
}

export default AddInstituteForm;
