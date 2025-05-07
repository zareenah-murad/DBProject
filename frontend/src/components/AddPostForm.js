import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';
import countriesData from '../data/Countries.json';




function AddPostForm() {
    const navigate = useNavigate();
    console.log("countriesData", countriesData);

    const [selectedCountry, setSelectedCountry] = useState('');
    const [selectedState, setSelectedState] = useState('');
    const [stateOptions, setStateOptions] = useState([]);
    const [cityOptions, setCityOptions] = useState([]);

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
    const [futureWarning, setFutureWarning] = useState('');



    const handleCountryChange = (e) => {
      const country = e.target.value;
      setSelectedCountry(country);
      setSelectedState('');
      setFormData({ ...formData, country, state: '', city: '' });
    };

    const handleStateChange = (e) => {
      const state = e.target.value;
      setSelectedState(state);
      setFormData({ ...formData, state, city: '' });
    };

    const handleCityChange = (e) => {
      setFormData({ ...formData, city: e.target.value });
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        const now = new Date().toISOString();
        let newValue = value;
    
        // Handle likes/dislikes
        if ((name === 'likes' || name === 'dislikes') && value !== '') {
            const numValue = parseInt(value);
            if (isNaN(numValue) || numValue < 0) return;
        }
    
        // Future time warning
        if (name === 'postTime' || name === 'repostTime') {
            const inputTime = new Date(value);
            const now = new Date();
        
            if (inputTime > now) {
                setFutureWarning(`Warning: ${name === 'postTime' ? 'Post' : 'Repost'} time is in the future.`);
            } else {
                setFutureWarning('');
            }
        }        
    
        // Repost before post validation
        if (name === 'repostTime' && formData.postTime && value < formData.postTime) {
            setMessage('Repost time cannot be earlier than post time.');
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
        PostID: formData.postID,
        UserID: formData.userID,
        PostText: formData.text,
        PostDateTime: formData.postTime,
        RepostedByUserID: formData.repostedByUserID || null,
        RepostDateTime: formData.repostTime || null,
        City: formData.city || null,
        State: formData.state || null,
        Country: formData.country || null,
        Likes: formData.likes ? parseInt(formData.likes) : null,
        Dislikes: formData.dislikes ? parseInt(formData.dislikes) : null,
        HasMultimedia: formData.hasMultimedia
        };

        const response = await axios.post('http://localhost:5050/add-post', postData);
        setMessage('Success: Post added!');
        handleClear();
    } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
            setMessage(`Error: ${error.response.data.error}`);
        } else {
            setMessage('Error: Unable to add post.');
        }
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
        setTimeout(() => {
            setMessage('');
        }, 3000);

    };

    // Check if all required fields are filled
    const isFormValid = formData.postID && formData.userID && formData.text && formData.postTime;
    console.log("Rendering formData", formData);

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
                <div style={{marginBottom: '10px'}}>
                    <div style={{marginBottom: '5px', color: '#666'}}>Post Time * (When was this originally posted?)
                    </div>
                    <input
                        name="postTime"
                        type="datetime-local"
                        value={formData.postTime}
                        onChange={handleChange}
                        required
                        style={formStyles.input}
                    />
                </div>
                {futureWarning && formData.postTime && futureWarning.includes('Post') && (
                    <p style={{ color: '#c62828', fontSize: '0.9em', marginTop: '5px' }}>{futureWarning}</p>
                )}
                <input
                    name="repostedByUserID"
                    placeholder="Reposted By User ID"
                    value={formData.repostedByUserID}
                    onChange={handleChange}
                    style={formStyles.input}
                />
                <div style={{marginBottom: '10px'}}>
                    <div style={{marginBottom: '5px', color: '#666'}}>Repost Time (When was this reposted?)</div>
                    <input
                        name="repostTime"
                        type="datetime-local"
                        value={formData.repostTime}
                        onChange={handleChange}
                        style={formStyles.input}
                    />
                </div>
                {futureWarning && formData.repostTime && futureWarning.includes('Repost') && (
                    <p style={{ color: '#c62828', fontSize: '0.9em', marginTop: '5px' }}>{futureWarning}</p>
                )}
                <div style={{display: 'flex', gap: '10px', marginBottom: '10px'}}>
                    {/* Country dropdown */}
                    <select
                        value={selectedCountry}
                        onChange={(e) => {
                            const country = e.target.value;
                            const found = countriesData.find(c => c.name === country);
                            setSelectedCountry(country);
                            setSelectedState('');
                            setFormData({...formData, country, state: '', city: ''});
                            setStateOptions(found ? found.states : []);
                            setCityOptions([]);
                        }}
                        style={formStyles.input}
                    >
                        <option value="">Select Country</option>
                        {countriesData.map((c) => (
                            <option key={c.id} value={c.name}>{c.name}</option>
                        ))}
                    </select>

                    {/* State dropdown */}
                    {stateOptions.length > 0 && (
                        <select
                            value={selectedState}
                            onChange={(e) => {
                                const state = e.target.value;
                                const found = stateOptions.find(s => s.name === state);
                                setSelectedState(state);
                                setFormData({...formData, state, city: ''});
                                setCityOptions(found ? found.cities : []);
                            }}
                            style={formStyles.input}
                        >
                            <option value="">Select State</option>
                            {stateOptions.map((s) => (
                                <option key={s.id} value={s.name}>{s.name}</option>
                            ))}
                        </select>
                    )}

                    {/* City dropdown */}
                    {cityOptions.length > 0 && (
                        <select
                            value={formData.city}
                            onChange={(e) => setFormData({...formData, city: e.target.value})}
                            style={formStyles.input}
                        >
                            <option value="">Select City</option>
                            {cityOptions.map((c) => (
                                <option key={c.id} value={c.name}>{c.name}</option>
                            ))}
                        </select>
                    )}
                </div>
                <div style={{display: 'flex', gap: '10px', marginBottom: '10px'}}>
                    <input
                        name="likes"
                        type="number"
                        min="0"
                        placeholder="Likes"
                        value={formData.likes}
                        onChange={handleChange}
                        style={{flex: 1, padding: '8px'}}
                    />
                    <input
                        name="dislikes"
                        type="number"
                        min="0"
                        placeholder="Dislikes"
                        value={formData.dislikes}
                        onChange={handleChange}
                        style={{flex: 1, padding: '8px'}}
                    />
                </div>
                <label style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '15px'}}>
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
                    backgroundColor: message.includes('Error')
                      ? '#ffebee'
                      : message.includes('Success')
                        ? '#e8f5e9'
                        : 'transparent',
                    color: message.includes('Error')
                      ? '#c62828'
                      : message.includes('Success')
                        ? '#2e7d32'
                        : '#000',
                    border: '1px solid',
                    padding: '10px',
                    borderRadius: '5px',
                    marginTop: '10px'
                  }}>
                    {message}
                  </p>
                )}
            </form>
        </div>
    );
}

export default AddPostForm;
