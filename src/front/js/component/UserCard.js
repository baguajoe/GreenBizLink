import React from "react";
import { useNavigate } from "react-router-dom";

const UserCard = ({ user, onConnect }) => {
    const navigate = useNavigate();

    return (
        <div className="user-card">
            <img src={user.profile_image || "default-avatar.png"} alt={user.name} className="user-avatar" />
            <div className="user-info">
                <h3>{user.name}</h3>
                <p>{user.role}</p>
                <p>{user.city}, {user.state}</p>
                <div className="user-actions">
                    <button onClick={() => navigate(`/profile/${user.id}`)}>View Profile</button>
                    <button onClick={() => onConnect(user.id)}>Connect</button>
                </div>
            </div>
        </div>
    );
};

export default UserCard;
