import React from 'react';
import { useNavigate } from 'react-router-dom';

function MainMenu() {
    const navigate = useNavigate();

    return (
        <div style={{
            padding: '30px',
            maxWidth: '1000px',
            margin: '0 auto',
            backgroundColor: '#fff'
        }}>
            <h1 style={{
                fontSize: '32px',
                fontWeight: 'bold',
                marginBottom: '16px',
                color: '#222'
            }}>
                Social Media Analysis Database System
            </h1>

            <p style={{
                color: '#666',
                fontStyle: 'bold',
                marginBottom: '30px',
                padding: '8px',
                borderLeft: '3px solid #ddd',
                backgroundColor: '#f9f9f9'
            }}>
                Welcome to the Social Media Analysis Database System.
This tool allows users to store, organize, and query social media text posts and their associated analysis results. Use the menu to enter project data, upload posts, record analytical findings, and explore data through detailed search and reporting features.
            </p>

            <div style={{ marginBottom: '40px' }}>
                <h2 style={{
                    fontSize: '24px',
                    fontWeight: 'bold',
                    marginBottom: '16px',
                    borderBottom: '1px solid #eee',
                    paddingBottom: '8px',
                    color: '#333'
                }}>
                    Enter Data
                </h2>

                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(2, 1fr)',
                    gap: '15px',
                    marginBottom: '30px'
                }}>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-user')}
                    >
                        Add User
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-field')}
                    >
                        Add Field
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-post')}
                    >
                        Add Post
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-socialmedia')}
                    >
                        Add Social Media
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-project')}
                    >
                        Add Project
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-analysisresult')}
                    >
                        Add Analysis Result
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/add-institute')}
                    >
                        Add Institute
                    </button>

                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/repost-post')}
                    >
                        Mark Post as Reposted
                    </button>

                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/associate-post-project')}
                    >
                        Associate Post with Project
                    </button>

                    <div></div>
                </div>
            </div>

            <div>
                <h2 style={{
                    fontSize: '24px',
                    fontWeight: 'bold',
                    marginBottom: '16px',
                    borderBottom: '1px solid #eee',
                    paddingBottom: '8px',
                    color: '#333'
                }}>
                    Query
                </h2>

                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '10px'
                }}>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/query/socialmedia')}
                    >
                        Find Posts of a Certain Social Media
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/query/timeperiod')}
                    >
                        Find Posts within a Certain Period of Time
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/query/username')}
                    >
                        Find Posts by Username of a Certain Media
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/query/name')}
                    >
                        Find Posts by First/Last Name
                    </button>
                    <button
                        style={{
                            padding: '10px 15px',
                            cursor: 'pointer',
                            backgroundColor: '#f8f8f8',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'left',
                            transition: 'all 0.2s'
                        }}
                        onClick={() => navigate('/query/experiment')}
                    >
                        View Experiment Results by Project
                    </button>
                </div>
            </div>
        </div>
    );
}

export default MainMenu;