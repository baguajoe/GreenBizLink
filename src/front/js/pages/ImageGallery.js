import React, { useState, useEffect } from 'react';

const ImageGallery = ({ userId }) => {
    const [images, setImages] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:5000/api/user/${userId}/images`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('jwt_token')}`
            }
        })
        .then(response => response.json())
        .then(data => setImages(data))
        .catch(error => console.error('Error fetching images:', error));
    }, [userId]);

    return (
        <div>
            <h2>Image Gallery</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {images.map(image => (
                    <div key={image.id} style={{ margin: '10px' }}>
                        <img
                            src={`http://localhost:5000/api/images/${image.file_name}`}
                            alt={image.file_name}
                            width="200"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ImageGallery;
