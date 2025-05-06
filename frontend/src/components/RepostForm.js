import React, { useState } from 'react';
import axios from 'axios';
import { formStyles } from './FormStyles';
import { useNavigate } from 'react-router-dom';

function RepostForm() {
    const navigate = useNavigate();
    const [postID, setPostID] = useState('');
    const [repostedByUserID, setRepostedByUserID] = useState('');
    const [repostTime, setRepostTime] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage('');

        try {
            const response = await axios.post('http://localhost:5050/update/repost', {
                postID,
                repostedByUserID,
                repostTime
            });

            setMessage(response.data.message || 'Repost info updated!');
        } catch (error) {
            console.error(error);
            setMessage(error.response?.data?.error || 'An error occurred.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Mark a Post as Reposted</h2>
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
                    placeholder="Post ID *"
                    value={postID}
                    onChange={(e) => setPostID(e.target.value)}
                    required
                    style={formStyles.input}
                />
                <input
                    type="text"
                    placeholder="Reposted By User ID *"
                    value={repostedByUserID}
                    onChange={(e) => setRepostedByUserID(e.target.value)}
                    required
                    style={formStyles.input}
                />
                <input
                    type="datetime-local"
                    value={repostTime}
                    onChange={(e) => setRepostTime(e.target.value)}
                    required
                    style={formStyles.input}
                />

                <div style={formStyles.buttonContainer}>
                <button
                    type="submit"
                    disabled={isLoading || !postID || !repostedByUserID || !repostTime}
                    style={{
                        ...formStyles.submitButton,
                        backgroundColor: (!postID || !repostedByUserID || !repostTime) ? '#cccccc' : '#4CAF50',
                        cursor: (!postID || !repostedByUserID || !repostTime) ? 'not-allowed' : 'pointer'
                    }}
                >
                    {isLoading ? 'Submitting...' : 'Mark as Repost'}
                </button>

                </div>

                {message && (
                    <p style={{
                        ...formStyles.message,
                        backgroundColor: message.includes('error') ? '#ffebee' : '#e8f5e9',
                        color: message.includes('error') ? '#c62828' : '#2e7d32'
                    }}>
                        {message}
                    </p>
                )}
            </form>
        </div>
    );
}

export default RepostForm;
