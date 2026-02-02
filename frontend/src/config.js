const API_BASE_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? 'http://127.0.0.1:5000'
    : window.location.origin;

export default API_BASE_URL;
