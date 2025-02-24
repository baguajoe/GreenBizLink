import axios from "axios";

// Set the API base URL
const API_BASE_URL = "http://127.0.0.1:5000/api"; // Update if needed

// Helper function to set Authorization header
const authHeader = () => {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
};

// Centralized error handler
const handleApiError = (error, defaultMessage) => {
    return { error: error.response?.data?.error || defaultMessage };
};

// ---------------- AUTHENTICATION ---------------- //

// Register a new user
export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/register`, userData);
        return response.data;
    } catch (error) {
        return handleApiError(error, "Registration failed");
    }
};

// Login and get JWT token
export const loginUser = async (credentials) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/login`, credentials);
        return response.data;
    } catch (error) {
        return handleApiError(error, "Login failed");
    }
};

// Logout user (invalidate token)


// Fetch user profile (Protected)
export const getUserProfile = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/profile`, { headers: authHeader() });
        return response.data;
    } catch (error) {
        return handleApiError(error, "Failed to fetch user profile");
    }
};

// Refresh token if expired
export const refreshToken = async () => {
    try {
        const refreshToken = localStorage.getItem("refresh_token");
        const response = await axios.post(`${API_BASE_URL}/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
        });
        localStorage.setItem("access_token", response.data.access_token);
        return response.data;
    } catch (error) {
        return handleApiError(error, "Session expired, please log in again.");
    }
};

// ---------------- ADVERTISEMENTS ---------------- //

// Get active advertisements
export const getAds = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/ads`);
        return response.data;
    } catch (error) {
        return handleApiError(error, "Failed to fetch ads");
    }
};

// Create a new advertisement (Companies only)
export const createAd = async (adData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/ads`, adData, {
            headers: {
                "Content-Type": "application/json",
                ...authHeader()
            }
        });
        return response.data;
    } catch (error) {
        return handleApiError(error, "Failed to submit ad");
    }
};
