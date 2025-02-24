import React, { useState } from "react";
// import { registerUser } from "../services/api";

const Register = () => {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        city: "",
        state: "",
        role: "Customer"
    });
    const [message, setMessage] = useState("");

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await registerUser(formData);
        if (response.error) {
            setMessage(response.error);
        } else {
            setMessage("Registration successful! Please check your email to verify your account.");
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" placeholder="Full Name" onChange={handleChange} required />
                <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
                <input type="text" name="city" placeholder="City" onChange={handleChange} required />
                <input type="text" name="state" placeholder="State" onChange={handleChange} required />
                <select name="role" onChange={handleChange}>
                    <option value="Customer">Customer</option>
                    <option value="Dispensary Owner">Dispensary Owner</option>
                    <option value="Manager">Manager</option>
                    <option value="Employee">Employee</option>
                </select>
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Register;
