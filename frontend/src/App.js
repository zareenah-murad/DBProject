import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainMenu from './components/MainMenu';
import AddUserForm from './components/AddUserForm';
import AddPostForm from './components/AddPostForm';
import RepostForm from './components/RepostForm';
import AddInstituteForm from './components/AddInstituteForm';
import AddProjectForm from './components/AddProjectForm';
import AddFieldForm from './components/AddFieldForm';
import AddSocialMediaForm from './components/AddSocialMediaForm';
import AddAnalysisResultForm from './components/AddAnalysisResultForm';
import AssociatePostWithProjectForm from './components/AssociatePostWithProjectForm';
import QuerySocialMediaPostsForm from './components/QuerySocialMediaPostsForm';
import QueryTimePeriodPostsForm from './components/QueryTimePeriodPostsForm';
import QueryUsernamePostsForm from './components/QueryUsernamePostsForm';
import QueryNamePostsForm from './components/QueryNamePostsForm';
import QueryExperimentResultsForm from './components/QueryExperimentResultsForm';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainMenu />} />
        <Route path="/add-user" element={<AddUserForm />} />
        <Route path="/add-post" element={<AddPostForm />} />
        <Route path="/repost-post" element={<RepostForm />} />
        <Route path="/add-institute" element={<AddInstituteForm />} />
        <Route path="/add-project" element={<AddProjectForm />} />
        <Route path="/add-field" element={<AddFieldForm />} />
        <Route path="/add-socialmedia" element={<AddSocialMediaForm />} />
        <Route path="/add-analysisresult" element={<AddAnalysisResultForm />} />
        <Route path="/associate-post-project" element={<AssociatePostWithProjectForm />} />
        <Route path="/query/socialmedia" element={<QuerySocialMediaPostsForm />} />
        <Route path="/query/timeperiod" element={<QueryTimePeriodPostsForm />} />
        <Route path="/query/username" element={<QueryUsernamePostsForm />} />
        <Route path="/query/name" element={<QueryNamePostsForm />} />
        <Route path="/query/experiment" element={<QueryExperimentResultsForm />} />
      </Routes>
    </Router>
  );
}

export default App;
