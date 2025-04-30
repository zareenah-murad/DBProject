import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddPostForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        postID: '',
        userID: '',
        text: '',
        postTime: '',
        repostedByUserID: '',
        repostTime: '',
        city: '',
        state: '',
        country: '',
        likes: '',
        dislikes: '',
        hasMultimedia: false,
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        let newValue = value;

        // Validation for likes and dislikes
        if ((name === 'likes' || name === 'dislikes') && value !== '') {
            const numValue = parseInt(value);
            if (isNaN(numValue) || numValue < 0) {
                return; // Don't update if invalid
            }
        }

        // Validation for repostTime
        if (name === 'repostTime' && formData.postTime && value < formData.postTime) {
            setMessage('Repost time cannot be earlier than post time');
            return;
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
            const postData = {
                ...formData,
                repostedByUserID: formData.repostedByUserID || null,
                repostTime: formData.repostTime || null,
                city: formData.city || null,
                state: formData.state || null,
                country: formData.country || null,
                likes: formData.likes ? parseInt(formData.likes) : null,
                dislikes: formData.dislikes ? parseInt(formData.dislikes) : null,
            };

            await axios.post('http://localhost:5050/add-post', postData);
            setMessage('Post added successfully!');
            handleClear();
        } catch (error) {
            setMessage('Error adding post.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = () => {
        setFormData({
            postID: '',
            userID: '',
            text: '',
            postTime: '',
            repostedByUserID: '',
            repostTime: '',
            city: '',
            state: '',
            country: '',
            likes: '',
            dislikes: '',
            hasMultimedia: false,
        });
        setMessage('');
    };

    // Check if all required fields are filled
    const isFormValid = formData.postID && formData.userID && formData.text && formData.postTime;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add Post</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    name="postID" 
                    placeholder="Post ID *" 
                    value={formData.postID} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <input 
                    name="userID" 
                    placeholder="User ID * (must exist in Users table)" 
                    value={formData.userID} 
                    onChange={handleChange} 
                    required 
                    style={formStyles.input}
                />
                <textarea 
                    name="text" 
                    placeholder="Text content *" 
                    value={formData.text} 
                    onChange={handleChange} 
                    required 
                    style={{...formStyles.input, minHeight: '100px'}}
                />
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>Post Time * (When was this originally posted?)</div>
                    <input 
                        name="postTime" 
                        type="datetime-local" 
                        value={formData.postTime} 
                        onChange={handleChange} 
                        required 
                        style={formStyles.input}
                    />
                </div>
                <input 
                    name="repostedByUserID" 
                    placeholder="Reposted By User ID" 
                    value={formData.repostedByUserID} 
                    onChange={handleChange} 
                    style={formStyles.input}
                />
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>Repost Time (When was this reposted?)</div>
                    <input 
                        name="repostTime" 
                        type="datetime-local" 
                        value={formData.repostTime} 
                        onChange={handleChange} 
                        style={formStyles.input}
                    />
                </div>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                    <input 
                        name="city" 
                        placeholder="City" 
                        value={formData.city} 
                        onChange={handleChange} 
                        style={{ flex: 1, padding: '8px' }} 
                    />
                    <input 
                        name="state" 
                        placeholder="State" 
                        value={formData.state} 
                        onChange={handleChange} 
                        style={{ flex: 1, padding: '8px' }} 
                    />
                    <input 
                        name="country" 
                        placeholder="Country" 
                        value={formData.country} 
                        onChange={handleChange} 
                        style={{ flex: 1, padding: '8px' }} 
                    />
                </div>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                    <input 
                        name="likes" 
                        type="number" 
                        min="0"
                        placeholder="Likes" 
                        value={formData.likes} 
                        onChange={handleChange} 
                        style={{ flex: 1, padding: '8px' }} 
                    />
                    <input 
                        name="dislikes" 
                        type="number" 
                        min="0"
                        placeholder="Dislikes" 
                        value={formData.dislikes} 
                        onChange={handleChange} 
                        style={{ flex: 1, padding: '8px' }} 
                    />
                </div>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '15px' }}>
                    <input 
                        type="checkbox" 
                        name="hasMultimedia" 
                        checked={formData.hasMultimedia} 
                        onChange={handleChange} 
                    />
                    Has Multimedia
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
                        {isLoading ? 'Adding...' : 'Add Post'}
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

export default AddPostForm;
