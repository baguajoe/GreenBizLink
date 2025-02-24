import React, { useEffect, useState } from "react";
// import { getPendingRequests, updateConnectionStatus } from "../services/api";  // ✅ Update path


const PendingRequests = () => {
    const [requests, setRequests] = useState([]);

    useEffect(() => {
        fetchRequests();
    }, []);

    const fetchRequests = async () => {
        const response = await getPendingRequests();
        if (response.error) {
            console.error(response.error);
        } else {
            setRequests(response);
        }
    };

    const handleResponse = async (id, status) => {
        const response = await updateConnectionStatus(id, status);
        if (response.error) {
            alert(response.error);
        } else {
            alert(`Request ${status}`);
            setRequests(requests.filter(request => request.id !== id));
        }
    };

    return (
        <div>
            <h2>Pending Connection Requests</h2>
            {requests.length === 0 ? <p>No pending requests.</p> :
                requests.map(request => (
                    <div key={request.id}>
                        <p>{request.user_name} ({request.user_role}) - {request.user_city}, {request.user_state}</p>
                        <button onClick={() => handleResponse(request.id, "connected")}>Accept</button>
                        <button onClick={() => handleResponse(request.id, "rejected")}>Reject</button>
                    </div>
                ))
            }
        </div>
    );
};

export default PendingRequests;
