import React, { useState } from 'react';

const VideoPlayer = ({ filename, instructional = false }) => {
    const [videoUrl, setVideoUrl] = useState(
        `http://localhost:5000/api/stream/video/${filename}`
    );

    // If it's an instructional video, set the appropriate endpoint
    if (instructional) {
        setVideoUrl(`http://localhost:5000/api/stream/instructional/${filename}`);
    }

    return (
        <div>
            <h2>{instructional ? 'Instructional Video' : 'User Video'}</h2>
            <video width="800" controls>
                <source src={videoUrl} type="video/mp4" />
                Your browser does not support the video tag.
            </video>
        </div>
    );
};

export default VideoPlayer;
