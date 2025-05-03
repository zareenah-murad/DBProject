import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function QueryNamePostsForm() {
    const navigate = useNavigate();
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [results, setResults] = useState([]);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);


    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults([]);
        setMessage('');

        try {
            const response = await axios.get(`http://localhost:5050/query/posts-by-name`, {
                params: {
                    firstName: firstName || undefined,
                    lastName: lastName || undefined
                }
            });
            if (response.data.length === 0) {
                setMessage('No posts found for this name!');
            } else {
                setResults(response.data);
            }
        } catch (error) {
            console.error(error);
            if (error.response?.data?.error) {
                setMessage(error.response.data.error);
            } else {
                setMessage('Error fetching posts.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const isFormValid = firstName || lastName; // At least one name must be provided

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Find Posts by Name</h2>
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
                    placeholder="First Name"
                    value={firstName}
                    onChange={(e) => {
                        setFirstName(e.target.value);
                        setMessage('');
                    }}
                    style={formStyles.input}
                />

                <input 
                    type="text"
                    placeholder="Last Name"
                    value={lastName}
                    onChange={(e) => {
                        setLastName(e.target.value);
                        setMessage('');
                    }}
                    style={formStyles.input}
                />

                {!isFormValid && (
                    <p style={{
                        ...formStyles.message,
                        backgroundColor: '#ffebee',
                        color: '#c62828'
                    }}>
                        Please enter at least first name or last name
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
                                    <p><strong>Name:</strong> {post.firstName} {post.lastName}</p>
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

export default QueryNamePostsForm; 