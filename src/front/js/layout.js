import React from "react";
import { Link, BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import HomePage from "./pages/home";
// import Login from "./pages/Login";
// import Signup from "./pages/Signup";
// import ForgotPassword from "./pages/ForgotPassword";
// import ResetPassword from "./pages/ResetPassword";
// import Favorites from "./pages/FavoriteConnects";
// import Profile2 from "./pages/Connects";
// import UserProfile from "./pages/UserProfile";
// import SpotterProfiles from "./pages/ConnectedProfiles";
// import ContactUs from "./pages/ContactUs";


const Layout = () => {
    return (
        <Router>
            <Navbar />
            <div className="content-wrapper">
                <Routes>
                    <Route element={<HomePage />} path="/" />
                    {/* <Route element={<Login />} path="/login" />
                    <Route element={<Signup />} path="/signup" />
                    <Route element={<ForgotPassword />} path="/forgot-password" />
                    <Route element={<ResetPassword />} path="/reset-password" />
                    <Route element={<FavoriteConnects />} path="/favorite-connects" />
                    <Route element={<Connects />} path="/connects" />
                    <Route element={<Single />} path="/single/:theid" />
                    <Route element={<UserProfile />} path="/user-profile" />
                    <Route element={<ContactUs />} path="/contact-us" /> */}
                    <Route
                        path="*"
                        element={
                            <React.Fragment>
                                <div className="notFoundDiv" style={{ textAlign: 'center' }}>
                                    <h1 className="mt-5">404 Not Found</h1>
                                    <Link to="/">
                                        <button className="btn btn-secondary my-4">Back home</button>
                                    </Link>
                                </div>
                            </React.Fragment>
                        }
                    />
                </Routes>
            </div>
            <Footer />
        </Router>
    );
};

export default Layout;
