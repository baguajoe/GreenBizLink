import React from "react";

const Tabs = ({ activeTab, setActiveTab }) => {
    return (
        <ul className="nav nav-tabs mb-3">
            {["home", "connects", "my-connects", "jobs", "messaging"].map((tab) => (
                <li className="nav-item" key={tab}>
                    <button 
                        className={`nav-link ${activeTab === tab ? "active" : ""}`}
                        onClick={() => setActiveTab(tab)}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                </li>
            ))}
        </ul>
    );
};

export default Tabs;
