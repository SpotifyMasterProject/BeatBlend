export class User {
    id: string
    username: string

    constructor(data: {
        id: string
        username: string
    }) {
        this.id = data.id
        this.username = data.username
    }
}