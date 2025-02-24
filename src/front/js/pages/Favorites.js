import React, { useEffect, useState } from "react";
// import { getFavoriteUsers } from "../services/api";  // ✅ Update path


const Favorites = () => {
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        fetchFavorites();
    }, []);

    const fetchFavorites = async () => {
        const response = await getFavoriteUsers();
        if (response.error) {
            console.error(response.error);
        } else {
            setFavorites(response);
        }
    };

    return (
        <div>
            <h2>Favorite Connections</h2>
            {favorites.length === 0 ? <p>No favorite connections.</p> :
                favorites.map(user => (
                    <div key={user.id}>
                        <p>{user.name} ({user.role}) - {user.city}, {user.state}</p>
                    </div>
                ))
            }
        </div>
    );
};

export default Favorites;
