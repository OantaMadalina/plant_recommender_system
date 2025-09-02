import { createContext, useState } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./shared/Layout";
import ErrorPage from "./errorPage/ErrorPage";
import LibraryPage from "./libraryPage/LibraryPage";
import LoginPage from "./loginPage/LoginPage";
import SongPage from "./songPage/SongPage";

type UserRoleContextType = {
  userRole: string;
  setUserRole: (userRole: string) => void;
};

type ClubThemeContextType = {
  isClubTheme: boolean;
  setIsClubTheme: (theme: boolean) => void;
};

export const isClubThemeContext = createContext<ClubThemeContextType>({
  isClubTheme: false,
  setIsClubTheme: (theme) => {},
});

export const userRoleContext = createContext<UserRoleContextType>({
  userRole: "user",
  setUserRole: (userRole) => {},
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <LibraryPage />,
      },
      {
        path: "/song/:songId",
        element: <SongPage />,
      },
    ],
  },
  {
    path: "login",
    element: <LoginPage />,
    errorElement: <ErrorPage />,
  },
]);

const App = () => {
  const [userRole, setUserRole] = useState("user");
  const [isClubTheme, setIsClubTheme] = useState(false);
  return (
    <isClubThemeContext.Provider value={{ isClubTheme, setIsClubTheme }}>
      <userRoleContext.Provider value={{ userRole, setUserRole }}>
        <RouterProvider router={router} />
      </userRoleContext.Provider>
    </isClubThemeContext.Provider>
  );
};

export default App;
