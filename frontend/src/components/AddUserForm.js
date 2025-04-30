import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddUserForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        userID: '',
        username: '',
        mediaName: '',
        firstName: '',
        lastName: '',
        birthCountry: '',
        residenceCountry: '',
        age: '',
        gender: '',
        isVerified: false,
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        let newValue = value;

        // Validation for age
        if (name === 'age' && value !== '') {
            const numValue = parseInt(value);
            if (isNaN(numValue) || numValue < 0) {
                return; // Don't update if invalid
            }
        }

        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : newValue,
        });
        setMessage('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const userData = {
                ...formData,
                firstName: formData.firstName || null,
                lastName: formData.lastName || null,
                birthCountry: formData.birthCountry || null,
                residenceCountry: formData.residenceCountry || null,
                age: formData.age ? parseInt(formData.age) : null,
                gender: formData.gender || null,
            };

            await axios.post('http://localhost:5050/add-user', userData);
            setMessage('User added successfully!');
            handleClear();
        } catch (error) {
            setMessage('Error adding user.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = () => {
        setFormData({
            userID: '',
            username: '',
            mediaName: '',
            firstName: '',
            lastName: '',
            birthCountry: '',
            residenceCountry: '',
            age: '',
            gender: '',
            isVerified: false,
        });
        setMessage('');
    };

    // Check if all required fields are filled
    const isFormValid = formData.userID && formData.username && formData.mediaName;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add User</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    name="userID" 
                    placeholder="User ID *" 
                    value={formData.userID} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="username" 
                    placeholder="Username *" 
                    value={formData.username} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="mediaName" 
                    placeholder="Media Name * (must exist in SocialMedia table)" 
                    value={formData.mediaName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="firstName" 
                    placeholder="First Name" 
                    value={formData.firstName} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <input 
                    name="lastName" 
                    placeholder="Last Name" 
                    value={formData.lastName} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <input 
                    name="birthCountry" 
                    placeholder="Birth Country" 
                    value={formData.birthCountry} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <input 
                    name="residenceCountry" 
                    placeholder="Residence Country" 
                    value={formData.residenceCountry} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <input 
                    name="age" 
                    type="number" 
                    min="0"
                    placeholder="Age" 
                    value={formData.age} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <input 
                    name="gender" 
                    placeholder="Gender" 
                    value={formData.gender} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '15px' }}>
                    <input 
                        type="checkbox" 
                        name="isVerified" 
                        checked={formData.isVerified} 
                        onChange={handleChange} 
                    />
                    Verified User
                </label>

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
                        {isLoading ? 'Adding...' : 'Add User'}
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

export default AddUserForm;
