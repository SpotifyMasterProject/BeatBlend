import { User } from './User';
import { Playlist } from '@/types/Playlist';
import { Recommendation } from '@/types/Recommendation';

export class Session {
    id: string
    name: string
    hostId: string
    hostName: string
    inviteLink: string
    guests: User[]
    playlist: Playlist
    creationDate: Date
    recommendations: Recommendation[]

    constructor(data: Session) {
        this.id = data.id
        this.name = data.name
        this.hostId = data.hostId
        this.hostName = data.hostName
        this.inviteLink = data.inviteLink
        this.guests = data.guests
        this.playlist = data.playlist
        this.creationDate = data.creationDate
        this.recommendations = data.recommendations
    }
}
