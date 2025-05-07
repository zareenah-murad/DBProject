import React, { useState } from 'react';
import axios from 'axios';
import { formStyles } from './FormStyles';
import { useNavigate } from 'react-router-dom';

function RepostForm() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [mediaName, setMediaName] = useState('');
    const [repostUsername, setRepostUsername] = useState('');
    const [repostMediaName, setRepostMediaName] = useState('');
    const [repostTime, setRepostTime] = useState('');
    const [posts, setPosts] = useState([]);
    const [selectedPostID, setSelectedPostID] = useState('');
    const [selectedPost, setSelectedPost] = useState(null);

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showFutureWarning, setShowFutureWarning] = useState(false);
    const [invalidTimeWarning, setInvalidTimeWarning] = useState('');

    const handleRepostTimeChange = (e) => {
        const inputTime = e.target.value;
        setRepostTime(inputTime);

        const selected = new Date(inputTime);
        const now = new Date();
        setShowFutureWarning(selected > now);

        if (selectedPost?.postDateTime) {
            const selectedUTC = new Date(inputTime);
            const originalUTC = new Date(selectedPost.postDateTime);
        
            console.log("== HANDLE TIME CHANGE ==");
            console.log("Original post datetime (raw):", selectedPost.postDateTime);
            console.log("Repost datetime (raw):", inputTime);
            console.log("Original (Date object):", new Date(selectedPost.postDateTime));
            console.log("Repost (Date object):", new Date(inputTime));
            console.log("Original timestamp:", new Date(selectedPost.postDateTime).getTime());
            console.log("Repost timestamp:", new Date(inputTime).getTime());

            // Compare timestamps directly
            if (selectedUTC.getTime() < originalUTC.getTime()) {
                setInvalidTimeWarning("Repost time cannot be before the original post time.");
            } else {
                setInvalidTimeWarning('');
            }
        }        
    };

    const fetchPosts = async () => {
        try {
            const res = await axios.get(`http://localhost:5050/query/posts-by-username?username=${username}&mediaName=${mediaName}`);
            setPosts(res.data);
            setMessage('');
            setSelectedPostID('');
            setSelectedPost(null);
        } catch (err) {
            console.error(err);
            setPosts([]);
            setMessage('Error fetching posts for user.');
        }
    };

    const handlePostSelect = (postID) => {
        setSelectedPostID(postID);
        const found = posts.find(p => String(p.postID) === String(postID)); // force both to string
        setSelectedPost(found || null);
        setInvalidTimeWarning('');
    };    

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage('');

        console.log("== HANDLE SUBMIT ==");
        console.log("Selected Post:", selectedPost);
        console.log("Selected Post DateTime (raw):", selectedPost.postDateTime);
        console.log("Selected Post DateTime (Date object):", new Date(selectedPost.postDateTime));
        console.log("Repost Time (raw):", repostTime);
        console.log("Repost Time (Date object):", new Date(repostTime));
        console.log("Post timestamp:", new Date(selectedPost.postDateTime).getTime());
        console.log("Repost timestamp:", new Date(repostTime).getTime());


        if (!selectedPost || new Date(repostTime).getTime() < new Date(selectedPost.postDateTime).getTime()) {
            setMessage('Error: Repost time must be after the original post time.');
            setIsLoading(false);
            return;
        }        

        try {
            const res = await axios.get(`http://localhost:5050/query/user-id?username=${repostUsername}&mediaName=${repostMediaName}`);
            const repostedByUserID = res.data.userID;

            console.log(repostTime);
            await axios.post('http://localhost:5050/update/repost', {
                postID: selectedPostID,
                repostedByUserID,
                repostTime
            });

            setMessage(`Success: Post ${selectedPostID} marked as reposted.`);
        } catch (err) {
            console.error(err);
            setMessage(err.response?.data?.error || 'An error occurred.');
        } finally {
            setIsLoading(false);
        }
    };

    const isFormValid = selectedPostID && repostUsername && repostMediaName && repostTime;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Mark a Post as Reposted</h2>
                <button onClick={() => navigate('/')} style={formStyles.backButton}>
                    Back to Menu
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    placeholder="Original Post Username *"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={formStyles.input}
                />
                <input
                    placeholder="Original Post Media Platform *"
                    value={mediaName}
                    onChange={(e) => setMediaName(e.target.value)}
                    style={formStyles.input}
                />
            <div style={{ marginBottom: '16px' }}>
                <button
                    type="button"
                    onClick={fetchPosts}
                    disabled={!username || !mediaName}
                    style={{
                        ...formStyles.submitButton,
                        backgroundColor: (!username || !mediaName) ? '#ccc' : '#4CAF50',
                        cursor: (!username || !mediaName) ? 'not-allowed' : 'pointer'
                    }}
                >
                    Fetch Posts
                </button>
                    </div>

                {posts.length > 0 && (
                    <select
                        value={selectedPostID}
                        onChange={(e) => handlePostSelect(e.target.value)}
                        style={formStyles.input}
                    >
                        <option value="">Select a Post</option>
                        {posts.map(p => (
                            <option key={p.postID} value={p.postID}>
                                {p.postID}: {p.content?.slice(0, 60)}...
                            </option>
                        ))}
                    </select>
                )}

                <input
                    placeholder="Reposted By Username"
                    value={repostUsername}
                    onChange={(e) => setRepostUsername(e.target.value)}
                    style={formStyles.input}
                />
                <input
                    placeholder="Reposted By Media Platform"
                    value={repostMediaName}
                    onChange={(e) => setRepostMediaName(e.target.value)}
                    style={formStyles.input}
                />
                <input
                    type="datetime-local"
                    value={repostTime}
                    onChange={handleRepostTimeChange}
                    style={formStyles.input}
                />
                {showFutureWarning && (
                    <p style={{ fontSize: '0.9em', color: '#c62828' }}>
                        Warning: Repost time is in the future.
                    </p>
                )}
                {invalidTimeWarning && (
                    <p style={{ fontSize: '0.9em', color: '#c62828' }}>
                        {invalidTimeWarning}
                    </p>
                )}

                <div style={formStyles.buttonContainer}>
                    <button
                        type="submit"
                        disabled={!isFormValid || isLoading}
                        style={{
                            ...formStyles.submitButton,
                            backgroundColor: isFormValid ? '#4CAF50' : '#ccc',
                            cursor: isFormValid ? 'pointer' : 'not-allowed'
                        }}
                    >
                        {isLoading ? 'Submitting...' : 'Mark as Repost'}
                    </button>
                </div>

                {message && (
                    <p style={{
                        backgroundColor: message.toLowerCase().includes('error') ? '#ffebee' : '#e8f5e9',
                        color: message.toLowerCase().includes('error') ? '#c62828' : '#2e7d32',
                        border: '1px solid',
                        borderColor: message.toLowerCase().includes('error') ? '#c62828' : '#2e7d32',
                        padding: '10px',
                        borderRadius: '5px',
                        marginTop: '10px',
                        fontWeight: '500',
                        fontSize: '0.95em'
                    }}>
                        {message}
                    </p>
                    )}

            </form>
        </div>
    );
}

export default RepostForm;
