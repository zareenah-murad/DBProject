import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';
import countriesData from '../data/Countries.json';

function AddPostForm() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [stateOptions, setStateOptions] = useState([]);
  const [cityOptions, setCityOptions] = useState([]);
  const [futureWarning, setFutureWarning] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const [formData, setFormData] = useState({
    username: '',
    mediaName: '',
    text: '',
    postTime: '',
    repostUsername: '',
    repostMediaName: '',
    repostTime: '',
    city: '',
    state: '',
    country: '',
    likes: '',
    dislikes: '',
    hasMultimedia: false,
    projectName: ''
  });

  useEffect(() => {
    // Fetch project names
    axios.get("http://localhost:5050/query/projects")
      .then(res => {
        if (Array.isArray(res.data)) {
          setProjects(res.data);
        }
      })
      .catch(err => console.error("Error fetching projects", err));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if ((name === 'likes' || name === 'dislikes') && value !== '') {
      const numValue = parseInt(value);
      if (isNaN(numValue) || numValue < 0) return;
    }

    if (name === 'postTime' || name === 'repostTime') {
      const inputTime = new Date(value);
      const now = new Date();
      setFutureWarning(inputTime > now ? `Warning: ${name === 'postTime' ? 'Post' : 'Repost'} time is in the future.` : '');
    }

    if (name === 'repostTime' && formData.postTime && value < formData.postTime) {
      setMessage('Repost time cannot be earlier than post time.');
      return;
    }

    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    setMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
  
    try {
      const { username, mediaName, repostUsername, repostMediaName } = formData;
  
      // Resolve main user ID
      const userRes = await axios.get(`http://localhost:5050/query/user-id?username=${username}&mediaName=${mediaName}`);
      const userID = userRes.data.userID;
  
      // Resolve repost user ID if provided
      let repostedByUserID = null;
      if (repostUsername && repostMediaName) {
        try {
          const repostRes = await axios.get(
            `http://localhost:5050/query/user-id?username=${repostUsername}&mediaName=${repostMediaName}`
          );
          repostedByUserID = repostRes.data.userID;
        } catch (err) {
          setMessage("Error: Could not resolve reposting user.");
          setIsLoading(false);
          return;
        }
      }
  
      const postData = {
        UserID: userID,
        PostText: formData.text,
        PostDateTime: formData.postTime,
        RepostedByUserID: repostedByUserID,
        RepostDateTime: formData.repostTime || null,
        City: formData.city || null,
        State: formData.state || null,
        Country: formData.country || null,
        Likes: formData.likes ? parseInt(formData.likes) : null,
        Dislikes: formData.dislikes ? parseInt(formData.dislikes) : null,
        HasMultimedia: formData.hasMultimedia
      };
  
      const response = await axios.post('http://localhost:5050/add-post', postData);
      const newPostID = response.data.postID;
      setMessage(`Success: Post added with ID ${newPostID}`);
  
      // If a projectName was selected, associate the post
      if (formData.projectName) {
        await axios.post("http://localhost:5050/add-used-in", {
          projectName: formData.projectName,
          postID: newPostID
        });
        setMessage(prev => prev + ` and associated with project "${formData.projectName}".`);
      }
  
      handleClear();
    } catch (err) {
      const msg = err.response?.data?.error || 'Unable to add post.';
      setMessage(`Error: ${msg}`);
    } finally {
      setIsLoading(false);
    }
  };  

  const handleClear = () => {
    setFormData({
      username: '',
      mediaName: '',
      text: '',
      postTime: '',
      repostUsername: '',
    repostMediaName: '',
      repostTime: '',
      city: '',
      state: '',
      country: '',
      likes: '',
      dislikes: '',
      hasMultimedia: false,
      projectName: ''
    });
    setTimeout(() => setMessage(''), 3000);
  };

  const isFormValid = formData.username && formData.mediaName && formData.text && formData.postTime;

  return (
    <div style={formStyles.container}>
      <div style={formStyles.header}>
        <h2>Add Post</h2>
        <button onClick={() => navigate('/')} style={formStyles.backButton}>
          Back to Menu
        </button>
      </div>
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Username *"
          value={formData.username}
          onChange={handleChange}
          required
          style={formStyles.input}
        />
        <input
          name="mediaName"
          placeholder="Media Platform *"
          value={formData.mediaName}
          onChange={handleChange}
          required
          style={formStyles.input}
        />
        <textarea
          name="text"
          placeholder="Post Text *"
          value={formData.text}
          onChange={handleChange}
          required
          style={{ ...formStyles.input, minHeight: '100px' }}
        />
        <input
          name="postTime"
          type="datetime-local"
          value={formData.postTime}
          onChange={handleChange}
          required
          style={formStyles.input}
        />
        {futureWarning && <p style={{ color: '#c62828' }}>{futureWarning}</p>}

        <input
        name="repostUsername"
        placeholder="Reposted By Username"
        value={formData.repostUsername}
        onChange={handleChange}
        style={formStyles.input}
        />
        <input
        name="repostMediaName"
        placeholder="Reposted By Media Platform"
        value={formData.repostMediaName}
        onChange={handleChange}
        style={formStyles.input}
        />

        <input
          name="repostTime"
          type="datetime-local"
          value={formData.repostTime}
          onChange={handleChange}
          style={formStyles.input}
        />

        {/* Country, State, City dropdowns go here as in your existing version */}

        <input
          name="likes"
          type="number"
          min="0"
          placeholder="Likes"
          value={formData.likes}
          onChange={handleChange}
          style={formStyles.input}
        />
        <input
          name="dislikes"
          type="number"
          min="0"
          placeholder="Dislikes"
          value={formData.dislikes}
          onChange={handleChange}
          style={formStyles.input}
        />

        <label>
          <input
            type="checkbox"
            name="hasMultimedia"
            checked={formData.hasMultimedia}
            onChange={handleChange}
          />
          Has Multimedia
        </label>

        {/* Project Dropdown */}
        <select
          name="projectName"
          value={formData.projectName}
          onChange={handleChange}
          style={formStyles.input}
        >
          <option value="">Associate with Project</option>
          {projects.map((p, idx) => (
            <option key={idx} value={p}>{p}</option>
          ))}
        </select>

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
            border: message.includes('Error') || message.includes('Success') ? '1px solid' : 'none',
            borderColor: message.includes('Error')
            ? '#c62828'
            : message.includes('Success')
                ? '#2e7d32'
                : 'transparent',
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

export default AddPostForm;
