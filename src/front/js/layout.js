import React, { useState } from "react";
import { Link, BrowserRouter as Router, Routes, Route, Outlet, Navigate } from "react-router-dom";
import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import HomePage from "./pages/home";
import LeftSidebar from "./component/LeftSidebar";
import RightSidebar from "./component/RightSidebar";
import Messaging from "./component/Messaging";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Logout from "./component/Logout";
import PendingRequests from "./pages/PendingRequests";
import Notifications from "./pages/Notifications";
import Favorites from "./pages/Favorites";
import AgeVerification from "./pages/AgeVerification";

// Middleware to enforce age verification before accessing the site
const RequireAgeVerification = ({ children }) => {
    const ageVerified = localStorage.getItem("ageVerified") === "true";
    return ageVerified ? children : <Navigate to="/" />;
};

// Page layout with sidebar
const PageLayout = () => {
    return (
        <div className="container-fluid mt-3">
            <div className="row">
                {/* Left Sidebar */}
                <div className="col-md-3 d-none d-md-block">
                    <LeftSidebar />
                </div>

                {/* Main Content */}
                <div className="col-md-6">
                    <Outlet /> {/* This is where route components will render */}
                </div>

                {/* Right Sidebar */}
                <div className="col-md-3 d-none d-md-block">
                    <RightSidebar />
                </div>
            </div>
        </div>
    );
};

const Layout = () => {
    const [showMessaging, setShowMessaging] = useState(false);

    return (
        <Router>
            <Navbar />
            <Routes>
                {/* Age Verification Page */}
                <Route path="/" element={<AgeVerification />} />

                {/* Protected Routes (Require Age Verification) */}
                <Route path="/home" element={<RequireAgeVerification><HomePage /></RequireAgeVerification>} />

                <Route element={<RequireAgeVerification><PageLayout /></RequireAgeVerification>}>
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/logout" element={<Logout />} />
                    <Route path="/pending-requests" element={<PendingRequests />} />
                    <Route path="/notifications" element={<Notifications />} />
                    <Route path="/favorites" element={<Favorites />} />

                    {/* 404 - Not Found */}
                    <Route
                        path="*"
                        element={
                            <div className="notFoundDiv" style={{ textAlign: 'center' }}>
                                <h1 className="mt-5">404 Not Found</h1>
                                <Link to="/">
                                    <button className="btn btn-secondary my-4">Back home</button>
                                </Link>
                            </div>
                        }
                    />
                </Route>
            </Routes>

            {/* Floating Chat Panel */}
            {showMessaging && <Messaging closeChat={() => setShowMessaging(false)} />}
            <Footer />
        </Router>
    );
};

export default Layout;
