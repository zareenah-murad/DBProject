import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function QueryExperimentResultsForm() {
    const navigate = useNavigate();
    const [projectName, setProjectName] = useState('');
    const [results, setResults] = useState(null);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults(null);
        setMessage('');

        try {
            const response = await axios.post('http://localhost:5050/query/experiment', {
                projectName: projectName
            });
            if (!response.data || (response.data.posts && response.data.posts.length === 0)) {
                setMessage('No results found for this project!');
            } else {
                setResults(response.data);
            }
        } catch (error) {
            setMessage('Error fetching experiment results.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Query Experiment Results</h2>
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
                    placeholder="Project Name *"
                    value={projectName}
                    onChange={(e) => {
                        setProjectName(e.target.value);
                        setMessage('');
                    }}
                    required
                    style={formStyles.input}
                />

                <div style={formStyles.buttonContainer}>
                    <button 
                        type="submit"
                        disabled={!projectName || isLoading}
                        style={{
                            ...formStyles.submitButton,
                            backgroundColor: projectName ? '#4CAF50' : '#cccccc',
                            cursor: projectName ? 'pointer' : 'not-allowed'
                        }}
                    >
                        {isLoading ? 'Loading...' : 'Get Results'}
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

                {results && (
                    <div style={{
                        marginTop: '20px',
                        padding: '15px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '4px',
                    }}>
                        <h3 style={{ marginBottom: '15px' }}>Project Results</h3>
                        
                        {/* Field Coverage Statistics */}
                        <div style={{
                            marginBottom: '20px',
                            padding: '15px',
                            backgroundColor: 'white',
                            borderRadius: '4px',
                            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                        }}>
                            <h4 style={{ marginBottom: '10px' }}>Field Coverage</h4>
                            {Object.entries(results.fieldCoverage || {}).map(([field, percentage]) => (
                                <div key={field} style={{ 
                                    display: 'flex', 
                                    justifyContent: 'space-between',
                                    marginBottom: '5px'
                                }}>
                                    <span>{field}:</span>
                                    <span>{(percentage * 100).toFixed(1)}%</span>
                                </div>
                            ))}
                        </div>

                        {/* Posts and Their Analysis Results */}
                        <h4 style={{ marginBottom: '10px' }}>Posts and Analysis Results</h4>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {results.posts && results.posts.map((post, index) => (
                                <li key={index} style={{
                                    padding: '15px',
                                    marginBottom: '15px',
                                    backgroundColor: 'white',
                                    borderRadius: '4px',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                                }}>
                                    <p style={{ 
                                        marginBottom: '10px',
                                        fontSize: '16px'
                                    }}>
                                        <strong>Post Text:</strong> {post.content}
                                    </p>
                                    
                                    {post.analysisResults && post.analysisResults.length > 0 ? (
                                        <div>
                                            <strong>Analysis Results:</strong>
                                            <ul style={{ 
                                                listStyle: 'none',
                                                padding: '10px',
                                                marginTop: '5px',
                                                backgroundColor: '#f8f9fa',
                                                borderRadius: '4px'
                                            }}>
                                                {post.analysisResults.map((result, rIndex) => (
                                                    <li key={rIndex} style={{ marginBottom: '5px' }}>
                                                        <strong>{result.fieldName}:</strong> {result.value}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    ) : (
                                        <p style={{ color: '#666', fontStyle: 'italic' }}>
                                            No analysis results for this post
                                        </p>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </form>
        </div>
    );
}

export default QueryExperimentResultsForm; 