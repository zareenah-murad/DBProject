import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

function AssociatePostWithProjectForm() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [mediaName, setMediaName] = useState('');
  const [posts, setPosts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selectedPostID, setSelectedPostID] = useState('');
  const [selectedProject, setSelectedProject] = useState('');
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
    } catch (err) {
      setMessage('Error fetching posts.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    console.log("Final values to submit:", {
      postID: selectedPostID,
      parsedID: parseInt(selectedPostID),
      projectName: selectedProject
    });
  
    
    try {      
        await axios.post('http://localhost:5050/add-used-in', {
            postID: parseInt(selectedPostID),
            projectName: selectedProject
          });          
      setMessage(`Success: Post ${selectedPostID} associated with project "${selectedProject}"`);
      setSelectedPostID('');
      setSelectedProject('');
    } catch (err) {
      setMessage('Error: Failed to associate post.');
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = username && mediaName && selectedPostID && selectedProject;

  return (
    <div style={formStyles.container}>
      <div style={formStyles.header}>
        <h2>Associate Post with Project</h2>
        <button onClick={() => navigate('/')} style={formStyles.backButton}>
          Back to Menu
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Username *"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={formStyles.input}
        />
        <input
          placeholder="Media Platform *"
          value={mediaName}
          onChange={(e) => setMediaName(e.target.value)}
          required
          style={formStyles.input}
        />
        <button
          type="button"
          onClick={fetchPosts}
          style={{
            ...formStyles.submitButton,
            marginBottom: '15px',
            backgroundColor: '#1976d2',
            color: '#fff'
          }}
        >
          Fetch Posts
        </button>

        {posts.length > 0 && (
            <select
            value={selectedPostID}
            onChange={(e) => setSelectedPostID(e.target.value)}
            style={formStyles.input}
          >
            <option value="">Select a Post</option>
            console.log("Posts received:", posts);
            {posts.map((p) => (
              <option key={p.postID} value={p.postID}>
              {p.content?.substring(0, 50)}...
            </option>            
            ))}
          </select>
        )}

        <select
          value={selectedProject}
          onChange={(e) => setSelectedProject(e.target.value)}
          style={formStyles.input}
          required
        >
          <option value="">Select a Project</option>
          {projects.map((proj, idx) => (
            <option key={idx} value={proj}>{proj}</option>
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
            {isLoading ? 'Associating...' : 'Associate'}
          </button>
        </div>

        {message && (
          <p style={{
            backgroundColor: message.includes('Error') ? '#ffebee' : '#e8f5e9',
            color: message.includes('Error') ? '#c62828' : '#2e7d32',
            border: '1px solid',
            borderColor: message.includes('Error') ? '#c62828' : '#2e7d32',
            padding: '10px',
            borderRadius: '5px',
            marginTop: '10px',
            fontWeight: '500'
          }}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

export default AssociatePostWithProjectForm;
