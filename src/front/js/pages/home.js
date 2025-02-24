import React, { useState } from "react";

import Feed from "../component/Feed";
import JobListings from "../component/JobListings";
import Tabs from "../component/Tabs";
import LeftSidebar from "../component/LeftSidebar";
import RightSidebar from "../component/RightSidebar";

const HomePage = () => {
    const [activeTab, setActiveTab] = useState("home");

    return (
        <div className="container-fluid mt-3">
            <div className="row">
                {/* Left Sidebar */}
                <div className="col-md-3 d-none d-md-block">
                    <LeftSidebar />
                </div>

                {/* Main Content */}
                <div className="col-md-6">
                    <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
                    {activeTab === "home" && <Feed />}
                    {activeTab === "jobs" && <JobListings />}
                </div>

                {/* Right Sidebar */}
                <div className="col-md-3 d-none d-md-block">
                    <RightSidebar />
                </div>
            </div>
        </div>
    );
};

export default HomePage;
