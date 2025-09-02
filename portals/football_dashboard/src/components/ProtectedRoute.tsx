import React from "react";
import { Navigate } from "react-router-dom";
import { useContext } from "react";
import AppContext from "../context/AppContext";

interface ProtectedRouteProps {
    children: JSX.Element;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { isLoggedIn } = useContext(AppContext);

    if (!isLoggedIn) {
        return <Navigate to="/" />;
    }

    return children;
};

export default ProtectedRoute;
