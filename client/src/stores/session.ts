import {defineStore} from 'pinia'
import {ref} from 'vue'
import {sessionService} from '@/services/sessionService'
import {Session} from '@/types/Session'
import {Playlist} from '@/types/Playlist'
import { SongList } from '@/types/Song'
import { SessionWebsocketService, PlaylistWebsocketService, RecommendationWebsocketService } from "@/services/websocketService";

export const useSession = defineStore('session', () => {

    const session = ref<Session>();

    const sessionSocket = new SessionWebsocketService();
    const playlistSocket = new PlaylistWebsocketService();
    const recommendationsSocket = new RecommendationWebsocketService();

    const storedSessionId = localStorage.getItem('sessionId')

    const handleSessionMessages = (sessionMessage: Session) => {
        const playlist = sessionMessage.playlist || session.value.playlist;
        const recommendations = sessionMessage.recommendations || session.value.recommendations;
        session.value = {
            isRunning: session.value.isRunning,
            ...sessionMessage,
            playlist,
            recommendations
        };
    };
      
    const handlePlaylistMessages = (playlistMessage: Playlist) => {
        if (session.value.playlist.currentSong?.id !== playlistMessage.currentSong?.id) {
            session.value.recommendations = [];
            fetchRecommendations();
        }
        session.value.playlist = playlistMessage;
    };
      
    const handleRecommendationMessages = (recommendationMessage: SongList) => {
       session.value.recommendations = recommendationMessage.songs;
       session.value.votingStartTime = recommendationMessage.votingStartTime;
    };

    const fetchRecommendations = () => {
        console.log("Fetching recommendations");
        sessionService.getRecommendations(session.value.id);
    }

    const initialize = async () => {
        session.value.isRunning = true;
        console.log(session.value);
        if (session.value.recommendations.length === 0) {
            fetchRecommendations();
        }

        localStorage.setItem('sessionId', session.value.id);

        sessionSocket.connect(session.value.id, handleSessionMessages);
        playlistSocket.connect(session.value.id, handlePlaylistMessages);
        recommendationsSocket.connect(session.value.id, handleRecommendationMessages);
    }



    const fetchSession = async (sessionId: string | null) => {
        const id = sessionId || storedSessionId;
        if (!id) {
            return;
        }
        try {
            session.value = await sessionService.getSessionById(id);
            return initialize();
        } catch (error) {
            localStorage.removeItem('sessionId');
        }
    }

    const createSession = async (newSession: Session) => {
        session.value = await sessionService.createNewSession(newSession);
        return initialize();
    }

    const endSession = async () => {
        await sessionService.endSession(session.value.id);

        session.value.isRunning = false;
        session.value.guests = {};

        sessionSocket.close;
        playlistSocket.close();
        recommendationsSocket.close();
    }

    return {session, fetchSession, createSession, endSession};
});


