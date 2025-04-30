import React, { useState } from 'react';
import axios from 'axios';

function AddAnalysisResultForm() {
    const [formData, setFormData] = useState({
        projectName: '',
        postID: '',
        fieldName: '',
        fieldValue: '',
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await axios.post('http://localhost:5050/add-analysisresult', formData);
            setMessage('Analysis result added successfully!');
            setFormData({
                projectName: '',
                postID: '',
                fieldName: '',
                fieldValue: '',
            });
        } catch (error) {
            setMessage('Error adding analysis result.');
        } finally {
            setIsLoading(false);
        }
    };

    const isFormValid = formData.projectName && formData.postID && formData.fieldName && formData.fieldValue;

    return (
        <div style={{ padding: '20px' }}>
            <h2>Add Analysis Result</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    name="projectName" 
                    placeholder="Project Name *" 
                    value={formData.projectName} 
                    onChange={handleChange} 
                    required 
                    style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                />
                <input 
                    name="postID" 
                    placeholder="Post ID *" 
                    value={formData.postID} 
                    onChange={handleChange} 
                    required 
                    style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                />
                <input 
                    name="fieldName" 
                    placeholder="Field Name *" 
                    value={formData.fieldName} 
                    onChange={handleChange} 
                    required 
                    style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                />
                <textarea 
                    name="fieldValue" 
                    placeholder="Field Value *" 
                    value={formData.fieldValue} 
                    onChange={handleChange} 
                    required 
                    rows={3}
                    style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
                />
                <button 
                    type="submit" 
                    disabled={!isFormValid || isLoading}
                    style={{ 
                        padding: '10px 20px',
                        backgroundColor: isFormValid ? '#4CAF50' : '#cccccc',
                        color: 'white',
                        border: 'none',
                        cursor: isFormValid ? 'pointer' : 'not-allowed'
                    }}
                >
                    {isLoading ? 'Adding...' : 'Add Analysis Result'}
                </button>
                {message && <p style={{ marginTop: '10px', color: message.includes('Error') ? '#dc3545' : '#28a745' }}>{message}</p>}
            </form>
        </div>
    );
}

export default AddAnalysisResultForm;
