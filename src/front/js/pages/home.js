import React, { useState } from "react";
import LeftSidebar from "../component/LeftSidebar";
import Feed from "../component/Feed";
import RightSidebar from "../component/RightSidebar";
import Messaging from "../component/Messaging";
import JobListings from "../component/JobListings";
import Tabs from "../component/Tabs";

const HomePage = () => {
    const [activeTab, setActiveTab] = useState("home");
    const [showMessaging, setShowMessaging] = useState(false);

    return (
        <>
        
            <div className="container-fluid mt-3">
                <div className="row">
                    {/* Left Sidebar (Profile + Quick Links) */}
                    <div className="col-md-3 d-none d-md-block">
                        <LeftSidebar />
                    </div>

                    {/* Main Content */}
                    <div className="col-md-6">
                        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
                        {activeTab === "home" && <Feed />}
                        {activeTab === "jobs" && <JobListings />}
                    </div>

                    {/* Right Sidebar (Suggestions + Ads) */}
                    <div className="col-md-3 d-none d-md-block">
                        <RightSidebar />
                    </div>
                </div>
            </div>

            {/* Floating Chat Panel */}
            {showMessaging && <Messaging closeChat={() => setShowMessaging(false)} />}
        </>
    );
};

export default HomePage;
