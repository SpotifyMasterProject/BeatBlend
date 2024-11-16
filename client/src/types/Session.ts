import { User } from './User';
import { Playlist } from '@/types/Playlist';
import {Recommendation, RecommendationList} from '@/types/Recommendation';
import {Artifacts} from "@/types/Artifact";

export class Session {
    id: string;
    name: string;
    hostId: string;
    hostName: string;
    guests: { [key: string]: User };
    playlist: Playlist;
    recommendations: RecommendationList[];
    isRunning: boolean;
    artifacts: Artifacts | null = null; // Ensure artifacts exists from the start

    constructor(data: Session) {
        this.id = data.id;
        this.name = data.name;
        this.hostId = data.hostId;
        this.hostName = data.hostName;
        this.guests = data.guests;
        this.playlist = data.playlist;
        this.recommendations = data.recommendations;
        this.isRunning = data.isRunning;
        this.artifacts = data.artifacts ?? null; // Initialize artifacts to null if not provided
    }
}
