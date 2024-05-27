import React, { useState } from 'react';
import axios from 'axios';

const ChatComponent = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/chat', { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse('An error occurred. Please try again later.');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
        />
        <button type="submit">Submit</button>
      </form>
      {response && <div>{response}</div>}
    </div>
  );
};

export default ChatComponent;