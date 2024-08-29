export class User {
    id: string
    username: string
    isHost: boolean
    sessions: string[]

    constructor(data: {
        id: string
        username: string
        isHost: boolean
        sessions: string[]
    }) {
        this.id = data.id
        this.username = data.username
        this.sessions = data.sessions
        this.isHost = data.isHost
    }
}