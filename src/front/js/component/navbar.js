import React from "react";
import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
    const navigate = useNavigate();
    const isAuthenticated = localStorage.getItem("access_token") !== null;

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        navigate("/login");
    };

    const resetAgeVerification = () => {
        localStorage.removeItem("ageVerified");
        localStorage.removeItem("ageVerificationExpires");
        navigate("/");
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container">
                <Link to="/" className="navbar-brand">
                    <span className="navbar-brand mb-0 h1">LeafBridgeConnect</span>
                </Link>

                <div className="ml-auto d-flex align-items-center">
                    <button className="btn btn-secondary me-2" onClick={resetAgeVerification}>
                        Reset Age Check
                    </button>

                    {isAuthenticated ? (
                        <button className="btn btn-danger" onClick={handleLogout}>
                            Logout
                        </button>
                    ) : (
                        <>
                            <Link to="/login">
                                <button className="btn btn-primary me-2">Login</button>
                            </Link>
                            <Link to="/register">
                                <button className="btn btn-success">Register</button>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};
