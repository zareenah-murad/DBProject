import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddProjectForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        projectName: '',
        managerFirstName: '',
        managerLastName: '',
        instituteName: '',
        startDate: '',
        endDate: '',
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;

        // Validation for endDate
        if (name === 'endDate' && formData.startDate && value < formData.startDate) {
            setMessage('End date cannot be earlier than start date');
            return;
        }

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
            await axios.post('http://localhost:5050/add-project', formData);
            setMessage('Project added successfully!');
            handleClear();
        } catch (error) {
            setMessage('Error adding project.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = () => {
        setFormData({
            projectName: '',
            managerFirstName: '',
            managerLastName: '',
            instituteName: '',
            startDate: '',
            endDate: '',
        });
        setMessage('');
    };

    // Check if all required fields are filled
    const isFormValid = formData.projectName && 
                       formData.managerFirstName && 
                       formData.managerLastName && 
                       formData.instituteName && 
                       formData.startDate && 
                       formData.endDate;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add Project</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    name="projectName" 
                    placeholder="Project Name *" 
                    value={formData.projectName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="managerFirstName" 
                    placeholder="Manager First Name *" 
                    value={formData.managerFirstName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="managerLastName" 
                    placeholder="Manager Last Name *" 
                    value={formData.managerLastName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="instituteName" 
                    placeholder="Institute Name * (must exist in Institute table)" 
                    value={formData.instituteName} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>Start Date *</div>
                    <input 
                        name="startDate" 
                        type="date" 
                        value={formData.startDate} 
                        onChange={handleChange} 
                        required 
                        style={formStyles.input}
                    />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>End Date * (must be after start date)</div>
                    <input 
                        name="endDate" 
                        type="date" 
                        value={formData.endDate} 
                        onChange={handleChange} 
                        required 
                        style={formStyles.input}
                    />
                </div>

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
                        {isLoading ? 'Adding...' : 'Add Project'}
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

export default AddProjectForm;
