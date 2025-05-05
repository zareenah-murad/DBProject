import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { formStyles } from './FormStyles';

const countries = [
  "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
  "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
  "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
  "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
  "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia", "Cameroon",
  "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
  "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus",
  "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti",
  "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
  "Eritrea", "Estonia", "Eswatini (fmr.Swaziland)", "Ethiopia", "Fiji", "Finland", "France",
  "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
  "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary",
  "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
  "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos",
  "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
  "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
  "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
  "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)",
  "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
  "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau",
  "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
  "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
  "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
  "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
  "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
  "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
  "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
  "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
  "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America",
  "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
];


function AddUserForm() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        mediaName: '',
        firstName: '',
        lastName: '',
        birthCountry: '',
        residenceCountry: '',
        age: '',
        gender: '',
        isVerified: false,
    });

    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        let newValue = value;

        // Validation for age
        if (name === 'age' && value !== '') {
            const numValue = parseInt(value);
            if (isNaN(numValue) || numValue < 0) {
                return; // Don't update if invalid
            }
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
        const response = await axios.post('http://localhost:5050/add-user', {
            username: formData.username,
            mediaName: formData.mediaName,
            firstName: formData.firstName,
            lastName: formData.lastName,
            birthCountry: formData.birthCountry,
            residenceCountry: formData.residenceCountry,
            age: formData.age,
            gender: formData.gender,
            isVerified: formData.isVerified,
        });
        const newUserId = response.data.userID;
        setMessage(`Success: User added! Assigned User ID: ${newUserId}`);
        handleClear(); // only clear form on success
    } catch (error) {
        console.log("ERROR:", error.response?.data?.error || error.message);
        if (error.response?.data?.error) {
            setMessage(`Error: ${error.response.data.error}`);
        } else {
            setMessage('Error: Unable to add User.');
        }
    } finally {
        setIsLoading(false);
    }
};

    const handleClear = () => {
        setFormData({
            userID: '',
            username: '',
            mediaName: '',
            firstName: '',
            lastName: '',
            birthCountry: '',
            residenceCountry: '',
            age: '',
            gender: '',
            isVerified: false,
        });

        // Clear the success or error message after 3 seconds
        setTimeout(() => {
            setMessage('');
        }, 3000);
    };

    // Check if all required fields are filled
    const isFormValid = formData.username && formData.mediaName;

    return (
        <div style={formStyles.container}>
            <div style={formStyles.header}>
                <h2>Add User</h2>
                <button 
                    onClick={() => navigate('/')}
                    style={formStyles.backButton}
                >
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
                    placeholder="Media Name * (must exist in SocialMedia table)"
                    value={formData.mediaName}
                    onChange={handleChange}
                    required
                    style={formStyles.input}
                />
                <input
                    name="firstName"
                    placeholder="First Name"
                    value={formData.firstName}
                    onChange={handleChange}
                    style={formStyles.input}
                />
                <input
                    name="lastName"
                    placeholder="Last Name"
                    value={formData.lastName}
                    onChange={handleChange}
                    style={formStyles.input}
                />
                <select
                    name="birthCountry"
                    value={formData.birthCountry}
                    onChange={handleChange}
                    style={formStyles.input}
                >
                    <option value="">Select Birth Country</option>
                    {countries.map((country, idx) => (
                        <option key={idx} value={country}>{country}</option>
                    ))}
                </select>
                <select
                    name="residenceCountry"
                    value={formData.residenceCountry}
                    onChange={handleChange}
                    style={formStyles.input}
                >
                    <option value="">Select Residence Country</option>
                    {countries.map((country, idx) => (
                        <option key={idx} value={country}>{country}</option>
                    ))}
                </select>

                <input
                    name="age"
                    type="number"
                    min="0"
                    placeholder="Age"
                    value={formData.age}
                    onChange={handleChange}
                    style={formStyles.input}
                />
                <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    style={{...formStyles.input, paddingRight: '10px'}}
                >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Non-Binary">Non-Binary</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                    <option value="Other">Other</option>
                </select>

                <label style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '15px'}}>
                    <input
                        type="checkbox"
                        name="isVerified"
                        checked={formData.isVerified}
                        onChange={handleChange}
                    />
                    Verified User
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
                        {isLoading ? 'Adding...' : 'Add User'}
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

export default AddUserForm;
