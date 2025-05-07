import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function QueryExperimentResultsForm() {
    const navigate = useNavigate();
    const [projectName, setProjectName] = useState('');
    const [results, setResults] = useState(null);
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [projectOptions, setProjectOptions] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5050/query/projects')
            .then((res) => {
                if (Array.isArray(res.data)) {
                    setProjectOptions(res.data);
                }
            })
            .catch(() => setMessage('Error: Failed to load projects.'));
    }, []);
    

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResults(null);
        setMessage('');
    
        try {
            const response = await axios.get('http://localhost:5050/query/experiment-results', {
                params: { projectName }
            });
    
            if (!response.data || response.data.posts.length === 0) {
                setMessage('No results found for this project!');
            } else {
                setResults(response.data); // includes both posts and fieldCoverage
            }
        } catch (error) {
            console.error('Error fetching experiment results:', error);
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
        <select
            value={projectName}
            onChange={(e) => {
                setProjectName(e.target.value);
                setMessage('');
            }}
            required
            style={formStyles.input}
        >
            <option value="">Select Project</option>
            {projectOptions.map((proj, idx) => (
                <option key={idx} value={proj}>{proj}</option>
            ))}
        </select>


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
                        {results.fieldCoverage && Object.entries(results.fieldCoverage).map(([field, percentage]) => (
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

                        {results.posts && results.posts.length > 0 && (
                            <div style={{
                                marginTop: '20px',
                                padding: '15px',
                                backgroundColor: '#f5f5f5',
                                borderRadius: '4px',
                            }}>
                                <h3 style={{ marginBottom: '10px' }}>Results:</h3>
                                <ul style={{ listStyle: 'none', padding: 0 }}>
                                {results.posts.map((post, index) => (
                                        <li key={index} style={{ padding: '10px', marginBottom: '10px', backgroundColor: 'white', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                                            <p><strong>Username:</strong> {post.username}</p>
                                            <p><strong>Name:</strong> {post.firstName} {post.lastName}</p>
                                            <p><strong>Content:</strong> {post.content}</p>
                                            <p><strong>Posted:</strong> {new Date(post.postDateTime).toLocaleString()}</p>
                                            {post.analysis.length > 0 && (
                                                <div>
                                                    <p><strong>Analysis:</strong></p>
                                                    <ul>
                                                        {post.analysis.map((entry, i) => (
                                                            <li key={i}>{entry.field}: {entry.value}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                        </li>
                                    ))}

                                </ul>
                            </div>
                        )}
                    </ul>
                </div>
            )}
        </form>
    </div>
);
};
export default QueryExperimentResultsForm; 
