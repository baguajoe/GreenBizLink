import React, { useState } from "react";

const HomePage = () => {
    const [activeTab, setActiveTab] = useState("home");
    const [showMessaging, setShowMessaging] = useState(false);
    const [postContent, setPostContent] = useState("");

    const handlePostSubmit = () => {
        if (postContent) {
            alert(`Post submitted: ${postContent}`);
            setPostContent("");
        } else {
            alert("Post cannot be empty!");
        }
    };

    return (
        <div className="home-page container mt-3">
            <h1>Welcome to GreenLinkBiz</h1>
            
            <ul className="nav nav-tabs mb-3">
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === "home" ? "active" : ""}`}
                        onClick={() => setActiveTab("home")}
                    >
                        Home
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === "connects" ? "active" : ""}`}
                        onClick={() => setActiveTab("connects")}
                    >
                        Connects
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === "my-connects" ? "active" : ""}`}
                        onClick={() => setActiveTab("my-connects")}
                    >
                        My Connects
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === "jobs" ? "active" : ""}`}
                        onClick={() => setActiveTab("jobs")}
                    >
                        Jobs
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === "messaging" ? "active" : ""}`}
                        onClick={() => setActiveTab("messaging")}
                    >
                        Messaging
                    </button>
                </li>
            </ul>

            <div className="tab-content">
                {activeTab === "home" && (
                    <div className="tab-pane active">
                        <div className="post-form mb-3">
                            <form>
                                <div className="mb-3">
                                    <label htmlFor="postContent" className="form-label">Start a Post</label>
                                    <textarea
                                        className="form-control"
                                        id="postContent"
                                        rows="3"
                                        value={postContent}
                                        onChange={(e) => setPostContent(e.target.value)}
                                        placeholder="What's on your mind?"
                                    />
                                </div>
                                <button
                                    type="button"
                                    className="btn btn-primary mt-2"
                                    onClick={handlePostSubmit}
                                >
                                    Post
                                </button>
                            </form>
                        </div>
                        <div className="feed">
                            <h4>Recent Updates</h4>
                            <div className="feed-item">
                                <strong>Karl Headen</strong> completed 10 years at Primerica
                                <div className="actions mt-2">
                                    <button className="btn btn-link">Like</button>
                                    <button className="btn btn-link">Comment</button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                
                {activeTab === "connects" && (
                    <div className="tab-pane active">
                        <h4>Explore New Connects</h4>
                        <p>Discover new connections here...</p>
                    </div>
                )}

                {activeTab === "my-connects" && (
                    <div className="tab-pane active">
                        <h4>Your Connections</h4>
                        <p>Your active connections will be displayed here...</p>
                    </div>
                )}

                {activeTab === "jobs" && (
                    <div className="tab-pane active">
                        <h4>Job Listings</h4>
                        <p>View and apply to jobs here...</p>
                    </div>
                )}

                {activeTab === "messaging" && (
                    <div className="tab-pane active">
                        <h4>Messaging</h4>
                        <button 
                            className="btn btn-primary" 
                            onClick={() => setShowMessaging(true)}
                        >
                            Open Messaging
                        </button>
                    </div>
                )}
            </div>

            {/* Modal */}
            {showMessaging && (
                <div className="modal show d-block" tabIndex="-1">
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Messaging</h5>
                                <button 
                                    type="button" 
                                    className="btn-close" 
                                    onClick={() => setShowMessaging(false)}
                                ></button>
                            </div>
                            <div className="modal-body">
                                <p>Your messaging content goes here...</p>
                            </div>
                            <div className="modal-footer">
                                <button 
                                    type="button" 
                                    className="btn btn-secondary" 
                                    onClick={() => setShowMessaging(false)}
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
            {showMessaging && (
                <div className="modal-backdrop show"></div>
            )}
        </div>
    );
};

export default HomePage;