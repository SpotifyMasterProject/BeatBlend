export class Song {
    id: string
    name: string
    artists: string[]
    album: string
    danceability: number
    energy: number
    speechiness: number
    valence: number
    tempo: number
    release_date: string
    popularity: number

    constructor(data: {
        id: string
        name: string
        artists: string[]
        album: string
        danceability: number
        energy: number
        speechiness: number
        valence: number
        tempo: number
        release_date: string
        popularity: number
    }) {
        this.id = data.id
        this.name = data.name
        this.artists = data.artists
        this.album = data.album
        this.danceability = data.danceability
        this.energy = data.energy
        this.speechiness = data.speechiness
        this.valence = data.valence
        this.tempo = data.tempo
        this.release_date = data.release_date
        this.popularity = data.popularity
    }
}