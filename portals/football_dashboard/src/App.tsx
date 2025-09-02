import React from "react";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import FixturesPage from "./pages/FixturesPage";
import NotFoundPage from "./pages/NotFoundPage";
import GamePage from "./pages/GamePage";
import TeamPage from "./pages/TeamPage";
import PlayerPage from "./pages/PlayerPage";
import StandingsPage from "./pages/StandingsPage";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import PlayersPage from "./pages/PlayersPage";

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route
                    path="/fixtures"
                    element={
                        <ProtectedRoute>
                            <FixturesPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/standings"
                    element={
                        <ProtectedRoute>
                            <StandingsPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/players"
                    element={
                        <ProtectedRoute>
                            <PlayersPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/games/:gameId"
                    element={
                        <ProtectedRoute>
                            <GamePage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/teams/:teamId"
                    element={
                        <ProtectedRoute>
                            <TeamPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/players/:playerId"
                    element={
                        <ProtectedRoute>
                            <PlayerPage />
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </BrowserRouter>
    );
};

export default App;
