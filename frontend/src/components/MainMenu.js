import React from 'react';
import { useNavigate } from 'react-router-dom';

function MainMenu() {
    const navigate = useNavigate();

    return (
        <div style={{ padding: '20px' }}>
            <p style={{ color: '#666', fontStyle: 'italic', marginBottom: '20px' }}>
                NOTE: This is a placeholder UI! The form fields are not connected to the backend yet.
            </p>
            <h2>Enter Data</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '300px', marginBottom: '30px' }}>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-user')}
                >
                    Add User
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-post')}
                >
                    Add Post
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-project')}
                >
                    Add Project
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-institute')}
                >
                    Add Institute
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-field')}
                >
                    Add Field
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-socialmedia')}
                >
                    Add Social Media
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/add-analysisresult')}
                >
                    Add Analysis Result
                </button>
            </div>

            <h2>Query</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '300px' }}>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/query/socialmedia')}
                >
                    Find posts of a certain social media
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/query/timeperiod')}
                >
                    Find posts between a certain period of time
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/query/username')}
                >
                    Find posts by username of a certain media
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/query/name')}
                >
                    Find posts by first/last name
                </button>
                <button 
                    style={{ padding: '10px', cursor: 'pointer' }}
                    onClick={() => navigate('/query/experiment')}
                >
                    View experiment results by project
                </button>
            </div>
        </div>
    );
}

export default MainMenu; 