import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {formStyles} from "./FormStyles";

function AddAnalysisResultForm() {
    const navigate = useNavigate();
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
        const response = await axios.post('http://localhost:5050/add-analysisresult', {
            ProjectName: formData.projectName,
            PostID: formData.postID,
            FieldName: formData.fieldName,
            FieldValue: formData.fieldValue,
        });
        setMessage('Success: Analysis Result Added!');
        handleClear(); // only clear form on success
    } catch (error) {
        console.log("ERROR:", error.response?.data?.error || error.message);
        if (error.response?.data?.error) {
            setMessage(`Error: ${error.response.data.error}`);
        } else {
            setMessage('Error: Unable to add Analysis Result.');
        }
    } finally {
        setIsLoading(false);
    }
};

    const handleClear = () => {
        setFormData({
            projectName: '',
            postID: '',
            fieldName: '',
            fieldValue: '',
        });

        // Clear the success or error message after 3 seconds
        setTimeout(() => {
            setMessage('');
        }, 3000);
    };

    const isFormValid = formData.projectName && formData.postID && formData.fieldName && formData.fieldValue;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add Analysis Result</h2>
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
                    placeholder="Project Name * (must exist in Project Table)"
                    value={formData.projectName}
                    onChange={handleChange}
                    required
                    style={formStyles.input}
                />
                <input
                    name="postID"
                    placeholder="Post ID *"
                    value={formData.postID}
                    onChange={handleChange}
                    required
                    style={formStyles.input}
                />
                <input
                    name="fieldName"
                    placeholder="Field Name *"
                    value={formData.fieldName}
                    onChange={handleChange}
                    required
                    style={formStyles.input}
                />
                <textarea
                    name="fieldValue"
                    placeholder="Field Value *"
                    value={formData.fieldValue}
                    onChange={handleChange}
                    required
                    style={formStyles.input}
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

export default AddAnalysisResultForm;
