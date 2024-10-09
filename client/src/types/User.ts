export class User {
    id: string
    username: string
    isHost: boolean
    sessions: string[]

    constructor(data: User) {
        this.id = data.id
        this.username = data.username
        this.sessions = data.sessions
        this.isHost = data.isHost
    }
}