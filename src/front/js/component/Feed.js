import React, { useState } from "react";

const Feed = () => {
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
        <div>
            {/* Post Form */}
            <div className="card p-3 mb-3">
                <textarea
                    className="form-control"
                    placeholder="What's on your mind?"
                    value={postContent}
                    onChange={(e) => setPostContent(e.target.value)}
                />
                <button className="btn btn-primary mt-2" onClick={handlePostSubmit}>
                    Post
                </button>
            </div>

            {/* Recent Updates */}
            <h4>Recent Updates</h4>
            <div className="card p-3 mb-2">
                <strong>Karl Headen</strong> completed 10 years at Primerica
            </div>
        </div>
    );
};

export default Feed;
