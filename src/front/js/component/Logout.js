import React, { useEffect } from "react";
// import { logoutUser } from "../services/api";
import { useNavigate } from "react-router-dom";

const Logout = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const logout = async () => {
            await logoutUser();
            navigate("/login");
        };
        logout();
    }, [navigate]);

    return <p>Logging out...</p>;
};

export default Logout;
