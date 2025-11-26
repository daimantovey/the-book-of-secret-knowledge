/**
 * Recipe LLM API Client
 * Connects to your Recipe LLM backend server
 */

import axios from 'axios';

// IMPORTANT: Change this to your server URL
// For local testing: Use your computer's IP address
// For production: Use your deployed server URL (e.g., Render, Railway)
const API_BASE_URL = 'http://192.168.1.5:5000'; // CHANGE THIS!

/**
 * Ask a question to Recipe LLM
 * @param {string} question - The question to ask
 * @param {string} provider - LLM provider (openai, anthropic, ollama)
 * @returns {Promise<string>} - The response from the LLM
 */
export const askRecipeLLM = async (question, provider = 'openai') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/ask`, {
      question,
      provider,
    });

    if (response.data.error) {
      throw new Error(response.data.error);
    }

    return response.data.response;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(
        error.response.data.error || 'Failed to get response from server',
      );
    } else if (error.request) {
      // No response received
      throw new Error(
        'Cannot connect to server. Make sure your Recipe LLM server is running and the API_BASE_URL is correct.',
      );
    } else {
      // Other error
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Clear conversation history
 * @returns {Promise<boolean>} - Success status
 */
export const clearHistory = async () => {
  try {
    await axios.post(`${API_BASE_URL}/clear`);
    return true;
  } catch (error) {
    console.error('Failed to clear history:', error);
    return false;
  }
};

export default {
  askRecipeLLM,
  clearHistory,
};
