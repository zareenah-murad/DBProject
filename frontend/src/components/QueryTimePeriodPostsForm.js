import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function QueryTimePeriodPostsForm() {
    const navigate = useNavigate();
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [results, setResults] = useState([]);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults([]);
        setMessage('');

        try {
            const response = await axios.get('http://localhost:5050/query/posts-by-time', {
                params: {
                    start: new Date(startDate).toISOString(),
                    end: new Date(endDate).toISOString()
                }
            });

            if (response.data.length === 0) {
                setMessage('No posts found in this time period!');
            } else {
                console.log('Response data:', response.data);
                setResults(response.data);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            setMessage('Error fetching posts.');
        } finally {
            setIsLoading(false);
        }
    };

    const isFormValid = startDate && endDate && startDate <= endDate;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Find Posts by Time Period</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>Start Date and Time *</div>
                    <input 
                        type="datetime-local"
                        value={startDate}
                        onChange={(e) => {
                            setStartDate(e.target.value);
                            setMessage('');
                        }}
                        required
                        style={formStyles.input}
                    />
                </div>

                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '5px', color: '#666' }}>End Date and Time *</div>
                    <input 
                        type="datetime-local"
                        value={endDate}
                        onChange={(e) => {
                            setEndDate(e.target.value);
                            setMessage('');
                        }}
                        required
                        style={formStyles.input}
                    />
                </div>

                {startDate && endDate && startDate > endDate && (
                    <p style={{
                        ...formStyles.message,
                        backgroundColor: '#ffebee',
                        color: '#c62828'
                    }}>
                        End date must be after start date
                    </p>
                )}

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
                                    <p><strong>Posted:</strong> {new Date(post.postDateTime).toLocaleString()}</p>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </form>
        </div>
    );
}

export default QueryTimePeriodPostsForm; 