import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function QuerySocialMediaPostsForm() {
    const navigate = useNavigate();
    const [mediaName, setMediaName] = useState('');
    const [results, setResults] = useState([]);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults([]);
        setMessage('');

        try {
            const response = await axios.get(`http://localhost:5050/query/posts-by-media?mediaName=${encodeURIComponent(mediaName)}`);
            console.log('Response data:', response.data);
            setResults(response.data);  // Keep this


            if (response.data.length === 0) {
                setMessage('No posts found!');
            } else {
                setResults(response.data);
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data.error) {
                setMessage(`Error: ${error.response.data.error}`);
            } else {
                setMessage('Error: Unable to fetch posts.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Find Posts by Social Media Platform</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text"
                    placeholder="Media Name *"
                    value={mediaName}
                    onChange={(e) => setMediaName(e.target.value)}
                    required
                    style={formStyles.input}
                />

                <div style={formStyles.buttonContainer}>
                    <button 
                        type="submit"
                        disabled={!mediaName || isLoading}
                        style={{
                            ...formStyles.submitButton,
                            backgroundColor: mediaName ? '#4CAF50' : '#cccccc',
                            cursor: mediaName ? 'pointer' : 'not-allowed'
                        }}
                    >
                        {isLoading ? 'Searching...' : 'Find Posts'}
                    </button>
                </div>

                {isLoading && (
                    <p style={formStyles.message}>Loading...</p>
                )}

                {message && (
                    <p style={{
                        ...formStyles.message,
                        backgroundColor: message.includes('Error') ? '#ffebee' : '#e8f5e9',
                        color: message.includes('Error') ? '#c62828' : '#2e7d32'
                    }}>
                        {message}
                    </p>
                )}

                {results.length > 0 && (
                    <div style={{
                        marginTop: '20px',
                        padding: '15px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '4px',
                    }}>
                        <h3 style={{ marginBottom: '10px' }}>Results:</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {results.map((post, index) => (
                                <li key={index} style={{
                                    padding: '10px',
                                    marginBottom: '10px',
                                    backgroundColor: 'white',
                                    borderRadius: '4px',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                                }}>
                                    <p><strong>Username:</strong> {post.username}</p>
                                    <p><strong>Content:</strong> {post.content}</p>
                                    <p><strong>Posted:</strong> {new Date(post.postDateTime).toLocaleString(undefined, {
                                        dateStyle: 'medium',
                                        timeStyle: 'short'
                                    })}</p>

                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </form>
        </div>
    );
}

export default QuerySocialMediaPostsForm; 