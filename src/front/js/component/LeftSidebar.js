import React from "react";

const LeftSidebar = () => {
    return (
        <div className="card p-3">
            <h5>John Doe</h5>
            <p>Dispensary Owner</p>
            <hr />
            <ul className="list-unstyled">
                <li><a href="#">My Profile</a></li>
                <li><a href="#">My Connections</a></li>
                <li><a href="#">Saved Jobs</a></li>
            </ul>
        </div>
    );
};

export default LeftSidebar;
