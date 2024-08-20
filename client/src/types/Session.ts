import { User } from './User';
import { Song } from './Song';

export class Session {
    id: string
    name: string
    inviteLink: string
    guests: User[]
    playlist: Song[]
    creationDate: Date
    isRunning: boolean

    constructor(data: {
        id: string
        name: string
        inviteLink: string
        guests: User[]
        playlistName: string
        playlist: Song[]
        creationDate: Date
        isRunning: boolean
    }) {
        this.id = data.id
        this.name = data.name
        this.inviteLink = data.inviteLink
        this.guests = data.guests
        this.playlist = data.playlist
        this.creationDate = data.creationDate
        this.isRunning = data.isRunning ?? false
    }
}

export class AnonymousSession {
    name: string
    hostUsername: string

    constructor(data: {
        name: string
        hostUsername: string
        guests: User[]
        playlistName: string
        playlist: Song[]
        creationDate: Date
        isRunning: boolean
    }) {
        this.name = data.name
        this.hostUsername = data.hostUsername
    }
}
