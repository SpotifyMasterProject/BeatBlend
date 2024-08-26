export class User {
    id: string
    username: string
    isHost: boolean

    constructor(data: {
        id: string
        username: string
        isHost: boolean
    }) {
        this.id = data.id
        this.username = data.username
        this.isHost = data.isHost
    }
}