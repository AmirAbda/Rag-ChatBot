// node --version # Should be >= 18
// npm install axios

import axios from 'axios';

const API_URL = 'http://localhost:8000/chat'; // Replace with your backend API endpoint

async function runChat(prompt) {
  try {
    const response = await axios.post(API_URL, { query: prompt });
    return response.data.response;
  } catch (error) {
    console.error('Error during chat:', error);
    throw error;
  }
}

export default runChat;