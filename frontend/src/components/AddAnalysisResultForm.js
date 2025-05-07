import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AddAnalysisResultForm() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [mediaName, setMediaName] = useState('');
  const [posts, setPosts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [availableFields, setAvailableFields] = useState([]);
  const [formData, setFormData] = useState({
    projectName: '',
    postID: '',
    fieldName: '',
    fieldValue: '',
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    axios.get("http://localhost:5050/query/projects")
      .then(res => {
        if (Array.isArray(res.data)) {
          setProjects(res.data);
        }
      })
      .catch(() => setMessage('Error fetching projects.'));
  }, []);

  const fetchPosts = async () => {
    try {
      const res = await axios.get(`http://localhost:5050/query/posts-by-username?username=${username}&mediaName=${mediaName}`);
      setPosts(res.data);
      setMessage(res.data.length === 0 ? 'No posts found for that user.' : '');
    } catch (err) {
      setMessage('Error fetching posts.');
    }
  };

  const handleChange = async (e) => {
    const { name, value } = e.target;

    setFormData(prev => ({
        ...prev,
        [name]: value,
    }));

    // Fetch fields if project changes
    if (name === 'projectName') {
        try {
            const res = await axios.get(`http://localhost:5050/query/fields-by-project?projectName=${value}`);
            if (Array.isArray(res.data)) {
                setAvailableFields(res.data);
            } else {
                setAvailableFields([]);
            }
        } catch (err) {
            console.error("Failed to load fields:", err);
            setAvailableFields([]);
        }
    }
};

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    try {
      await axios.post('http://localhost:5050/add-analysisresult', {
        ProjectName: formData.projectName,
        PostID: formData.postID,
        FieldName: formData.fieldName,
        FieldValue: formData.fieldValue,
      });
      setMessage('Success: Analysis Result Added!');
      handleClear();
    } catch (error) {
      const errMsg = error.response?.data?.error || 'Unable to add Analysis Result.';
      setMessage(`Error: ${errMsg}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setUsername('');
    setMediaName('');
    setPosts([]);
    setFormData({
      projectName: '',
      postID: '',
      fieldName: '',
      fieldValue: '',
    });
    setTimeout(() => setMessage(''), 3000);
  };

  const isFormValid = formData.projectName && formData.postID && formData.fieldName && formData.fieldValue;

  return (
    <div style={formStyles.container}>
      <div style={formStyles.header}>
        <h2>Add Analysis Result</h2>
        <button onClick={() => navigate('/')} style={formStyles.backButton}>Back to Menu</button>
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
        <button
          type="button"
          onClick={fetchPosts}
          disabled={!username || !mediaName}
          style={{
            ...formStyles.submitButton,
            backgroundColor: (!username || !mediaName) ? '#ccc' : '#4CAF50',
            cursor: (!username || !mediaName) ? 'not-allowed' : 'pointer',
            marginBottom: '10px'
          }}
        >
          Fetch Posts
        </button>

        {posts.length > 0 && (
          <select
            name="postID"
            value={formData.postID}
            onChange={handleChange}
            style={formStyles.input}
          >
            <option value="">Select a Post</option>
            {posts.map(p => (
              <option key={p.postID} value={p.postID}>
                {p.postID}: {p.content?.slice(0, 50)}...
              </option>
            ))}
          </select>
        )}

        <select
          name="projectName"
          value={formData.projectName}
          onChange={handleChange}
          required
          style={formStyles.input}
        >
          <option value="">Select a Project</option>
          {projects.map((proj, idx) => (
            <option key={idx} value={proj}>{proj}</option>
          ))}
        </select>

        <select
            name="fieldName"
            value={formData.fieldName}
            onChange={handleChange}
            required
            style={formStyles.input}
        >
            <option value="">Select Field Name</option>
            {availableFields.map((field, idx) => (
                <option key={idx} value={field}>{field}</option>
            ))}
        </select>
        <textarea
          name="fieldValue"
          placeholder="Field Value *"
          value={formData.fieldValue}
          onChange={handleChange}
          required
          style={formStyles.input}
        />

        <button
          type="submit"
          disabled={!isFormValid || isLoading}
          style={{
            ...formStyles.submitButton,
            backgroundColor: isFormValid ? '#4CAF50' : '#ccc',
            cursor: isFormValid ? 'pointer' : 'not-allowed'
          }}
        >
          {isLoading ? 'Adding...' : 'Add Analysis Result'}
        </button>

        {message && (
          <p style={{
            ...formStyles.message,
            backgroundColor: message.includes('Error') ? '#ffebee' : '#e8f5e9',
            color: message.includes('Error') ? '#c62828' : '#2e7d32'
          }}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

export default AddAnalysisResultForm;
