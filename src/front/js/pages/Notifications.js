import React, { useEffect, useState } from "react";
// import { getNotifications } from "../services/api";  // ✅ Update path


const Notifications = () => {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        fetchNotifications();
    }, []);

    const fetchNotifications = async () => {
        const response = await getNotifications();
        if (response.error) {
            console.error(response.error);
        } else {
            setNotifications(response);
        }
    };

    return (
        <div>
            <h2>Notifications</h2>
            {notifications.length === 0 ? <p>No new notifications.</p> :
                notifications.map((notification, index) => (
                    <div key={index}>
                        <p>{notification.message}</p>
                        <small>{new Date(notification.timestamp).toLocaleString()}</small>
                    </div>
                ))
            }
        </div>
    );
};

export default Notifications;
