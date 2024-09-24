export class Song {
    id: string
    trackName: string
    artists: string[]
    album: string
    danceability: number
    energy: number
    speechiness: number
    valence: number
    tempo: number
    scaledTempo: number
    release_date: string
    popularity: number

    constructor(data: {
        id: string
        trackName: string
        artists: string[]
        album: string
        danceability: number
        energy: number
        speechiness: number
        valence: number
        tempo: number
        scaledTempo: number
        release_date: string
        popularity: number
    }) {
        this.id = data.id
        this.trackName = data.trackName
        this.artists = data.artists
        this.album = data.album
        this.danceability = data.danceability
        this.energy = data.energy
        this.speechiness = data.speechiness
        this.valence = data.valence
        this.tempo = data.tempo
        this.scaledTempo = data.scaledTempo
        this.release_date = data.release_date
        this.popularity = data.popularity
    }
}