export interface Game {
    id?: number;
    firstTeamId: number;
    secondTeamId: number;
    firstTeamScore: number;
    secondTeamScore: number;
    gameDateAndTime: string;
    scorers?: ScorerOutput[];
}

export interface Stadium {
    id?: number;
    address: string;
    city: string;
    imageUrl: string;
    stadiumCapacity: number;
    stadiumName: string;
    surface: string;
    teamId: number;
    signedPhotoUrl?: string;
}

export interface Player {
    id?: number;
    age: number;
    assists: number;
    fieldPosition: string;
    firstName: string;
    fullName: string;
    goalsTotal: number;
    height: string;
    imageUrl: string;
    isCaptain: boolean;
    isInjured: boolean;
    lastName: string;
    leagueId: string;
    nationality: string;
    teamId: number;
    weight: string;
    signedPhotoUrl?: string;
}

export interface Scorer {
    player: Player;
    minutes: number[];
}

export interface ScorerOutput {
    playerId?: number;
    teamId: number;
    minutes: number[];
}

export interface Team {
    id?: number;
    teamName: string;
    code: string;
    country: string;
    founded: number;
    imageUrl: string;
    stadiumId: number;
    isDeleted: boolean;
    signedPhotoUrl?: string;
}

export interface DeleteGameResponse {
    success: boolean;
    message?: string;
}

export interface CreateGameResponse {
    success: boolean;
    message?: string;
}

export interface Standing {
    team_id: number;
    position: number;
    points: number;
    goalsScored: number;
    goalsConceded: number;
    gamesPlayed: number;
}

export interface TopScorer {
    player_id: number;
    goals_scored: number;
}