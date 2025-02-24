import React, { useState } from "react";
import { createAd } from "../services/api";

const SubmitAd = () => {
    const [adData, setAdData] = useState({
        title: "",
        description: "",
        image_url: "",
        link: ""
    });
    const [message, setMessage] = useState("");

    const handleChange = (e) => {
        setAdData({ ...adData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await createAd(adData);
        if (response.error) {
            setMessage(response.error);
        } else {
            setMessage("Ad submitted successfully!");
            setAdData({ title: "", description: "", image_url: "", link: "" });
        }
    };

    return (
        <div>
            <h2>Submit Advertisement</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Ad Title" onChange={handleChange} required />
                <textarea name="description" placeholder="Ad Description" onChange={handleChange} required />
                <input type="text" name="image_url" placeholder="Image URL (optional)" onChange={handleChange} />
                <input type="text" name="link" placeholder="Ad Link" onChange={handleChange} required />
                <button type="submit">Submit Ad</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default SubmitAd;
