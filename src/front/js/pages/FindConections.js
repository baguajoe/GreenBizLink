import React, { useEffect, useState } from "react";
import { discoverUsers, sendConnectionRequest } from "../services/api";
import { useNavigate } from "react-router-dom";
import UserCard from "../components/UserCard";
import SearchBar from "../components/SearchBar";
import Pagination from "../components/Pagination";

const FindConnections = () => {
    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchUsers();
    }, [search, page]);

    const fetchUsers = async () => {
        setLoading(true);
        const response = await discoverUsers(search, page);
        if (response.error) {
            console.error(response.error);
        } else {
            setUsers(response.users);
            setTotalPages(response.total_pages);
        }
        setLoading(false);
    };

    const handleSendRequest = async (id) => {
        const response = await sendConnectionRequest(id);
        if (response.error) {
            alert(response.error);
        } else {
            alert("Connection request sent!");
            setUsers(users.filter(user => user.id !== id));
        }
    };

    return (
        <div className="find-connections">
            <h2>Find Connections</h2>
            <SearchBar search={search} setSearch={setSearch} />
            
            {loading ? <p>Loading...</p> : (
                <>
                    <div className="user-list">
                        {users.map(user => (
                            <UserCard key={user.id} user={user} onConnect={handleSendRequest} />
                        ))}
                    </div>

                    <Pagination page={page} totalPages={totalPages} setPage={setPage} />
                </>
            )}
        </div>
    );
};

export default FindConnections;
