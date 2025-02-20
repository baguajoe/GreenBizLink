import React, { useState } from "react";

import Feed from "../component/Feed";
import JobListings from "../component/JobListings";
import Tabs from "../component/Tabs";

const HomePage = () => {
    const [activeTab, setActiveTab] = useState("home");

    return (
        <>
        
            <div className="container-fluid mt-3">
                <div className="row">

                    {/* Main Content */}
                    <div className="col">
                        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
                        {activeTab === "home" && <Feed />}
                        {activeTab === "jobs" && <JobListings />}
                    </div>

                   
                </div>
            </div>

          
        </>
    );
};

export default HomePage;
