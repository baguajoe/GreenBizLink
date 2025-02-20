import React from "react";

const Messaging = ({ closeChat }) => {
    return (
        <div className="chat-panel">
            <div className="chat-header">
                <h5>Messages</h5>
                <button onClick={closeChat}>X</button>
            </div>
            <div className="chat-body">
                <p>Start a new conversation...</p>
            </div>
        </div>
    );
};

export default Messaging;
