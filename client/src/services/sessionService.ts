import apiClient from '@/services/axios';
import { Session } from '@/types/Session';
import { Song } from '@/types/Song';

export const sessionService = {

    async joinSession(sessionId: string): Promise<Session> {
        return apiClient.post(`/sessions/${sessionId}/guests`).then((response) => {
            return response.data;
        })
    },
    async getSessions(): Promise<Session[]> {
        return apiClient.get('/sessions').then((response) => {
            return response.data;
        })
    },
    async getSessionById(sessionId: string): Promise<Session> {
        return apiClient.get(`/sessions/${sessionId}`).then((response) => {
            return response.data;
        })
    },
    async getSongs(pattern: string): Promise<Song[]> {
        return apiClient.get(`/songs`, {params: {pattern}}).then((response) => {
            return response.data['songs'];
        })
    },
    async createNewSession(session: Session): Promise<Session> {
        return apiClient.post(`/sessions`, {...session}).then((response) => {
            return response.data;
        })
    }
};