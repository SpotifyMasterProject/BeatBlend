import apiClient from '@/services/axios';
import { AnonymousSession, Session } from '@/types/Session';
import { Song } from '@/types/Song';

export const sessionService = {

    async getSessionByInviteToken(inviteToken: string): Promise<AnonymousSession> {
        return apiClient.get(`/sessions/join/${inviteToken}`).then((response) => {
            return response.data;
        })
    },
    async joinSession(inviteToken: string): Promise<Session> {
        return apiClient.post(`/sessions/join/${inviteToken}`).then((response) => {
            return response.data;
        })
    },
    async getSessions(): Promise<Session[]> {
        return apiClient.get('/sessions').then((response) => {
            return response.data;
        })
    },
    async getSessionById(sessionId: string): Promise<AnonymousSession> {
        return apiClient.get(`/sessions/${sessionId}`).then((response) => {
            return response.data;
        })
    },
    async getSongs(pattern: string): Promise<Song[]> {
        return apiClient.get(`/songs/${pattern}`).then((response) => {
            return response.data;
        })
    },
    async createNewSession(session: Session): Promise<Session> {
        return apiClient.post(`/sessions`, {...session}).then((response) => {
            return response.data;
        })
    }
};