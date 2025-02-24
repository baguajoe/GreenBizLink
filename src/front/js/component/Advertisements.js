import React, { useEffect, useState } from "react";
import { getAds } from "../services/api";

const Advertisements = () => {
    const [ads, setAds] = useState([]);

    useEffect(() => {
        fetchAds();
    }, []);

    const fetchAds = async () => {
        const response = await getAds();
        if (response.error) {
            console.error(response.error);
        } else {
            setAds(response);
        }
    };

    return (
        <div className="ads-container">
            <h3>Sponsored Ads</h3>
            {ads.length === 0 ? <p>No ads available.</p> :
                ads.map(ad => (
                    <div key={ad.id} className="ad-card">
                        {ad.image_url && <img src={ad.image_url} alt={ad.title} />}
                        <h4>{ad.title}</h4>
                        <p>{ad.description}</p>
                        <a href={ad.link} target="_blank" rel="noopener noreferrer">Learn More</a>
                    </div>
                ))
            }
        </div>
    );
};

export default Advertisements;
