// Frontend API service for chat functionality
class ApiService {
  constructor(baseURL) {
    this.baseURL = baseURL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  // Helper method to get auth token from localStorage or elsewhere
  getAuthToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
    }
    return null;
  }

  // Helper method to make API requests
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      ...this.defaultHeaders,
      ...options.headers,
    };

    // Add authorization header if available
    const authToken = this.getAuthToken();
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    const config = {
      method: options.method || 'GET',
      headers,
      ...options,
    };

    if (options.body && typeof options.body !== 'string') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${error.message}`);
      throw error;
    }
  }

  // Chat API methods
  async sendMessage(userId, message, conversationId = null) {
    const body = {
      message,
      conversation_id: conversationId,
    };

    return this.request(`/api/v1/users/${userId}/chat`, {
      method: 'POST',
      body,
    });
  }

  async getUserConversations(userId) {
    return this.request(`/api/v1/users/${userId}/conversations`, {
      method: 'GET',
    });
  }

  async getConversationMessages(userId, conversationId) {
    return this.request(`/api/v1/users/${userId}/conversations/${conversationId}/messages`, {
      method: 'GET',
    });
  }

  // Authentication methods
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    // For login, we need to send form data, not JSON
    const response = await fetch(`${this.baseURL}/api/v1/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async logout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken');
    }
  }
}

export default new ApiService();