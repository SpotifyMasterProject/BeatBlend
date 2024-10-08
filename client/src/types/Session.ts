import { User } from './User';
import { Playlist } from '@/types/Playlist';

export class Session {
    id: string
    name: string
    hostName: string
    inviteLink: string
    guests: User[]
    playlist: Playlist[]
    creationDate: Date

    constructor(data: Session) {
        this.id = data.id
        this.name = data.name
        this.hostName = data.hostName
        this.inviteLink = data.inviteLink
        this.guests = data.guests
        this.playlist = data.playlist
        this.creationDate = data.creationDate
    }
}

