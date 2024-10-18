export class User {
    id: string
    username: string
    isHost: boolean

    constructor(data: User) {
        this.id = data.id
        this.username = data.username
        this.isHost = data.isHost
    }
}