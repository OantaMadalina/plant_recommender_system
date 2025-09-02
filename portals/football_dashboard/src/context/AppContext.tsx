import React, { ReactNode, useEffect, useState } from "react";

interface AppContextType {
    isAdmin: boolean;
    setIsAdmin: (isAdmin: boolean) => void;
    isLoggedIn: boolean;
    setIsLoggedIn: (isLoggedIn: boolean) => void;
    validUser: { username: string; password: string; fullName: string };
}

const AppContext = React.createContext<AppContextType>({
    isAdmin: false,
    setIsAdmin: () => {},
    isLoggedIn: false,
    setIsLoggedIn: () => {},
    validUser: { username: "", password: "", fullName: "" },
});

interface AppContextProviderProps {
    children: ReactNode;
}

export const AppContextProvider: React.FC<AppContextProviderProps> = ({
    children,
}) => {
    const [isAdmin, setIsAdmin] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(() => {
        const storedIsLoggedIn = localStorage.getItem("isLoggedIn");
        return storedIsLoggedIn === "true";
    });

    const validUser = {
        username: "test",
        password: "pass",
        fullName: "Antonio Rosu",
    };

    useEffect(() => {
        localStorage.setItem("isLoggedIn", isLoggedIn.toString());
    }, [isLoggedIn]);

    return (
        <AppContext.Provider
            value={{
                isAdmin,
                setIsAdmin,
                isLoggedIn,
                setIsLoggedIn,
                validUser,
            }}
        >
            {children}
        </AppContext.Provider>
    );
};

export default AppContext;
