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
    releaseDate: string
    popularity: number
    durationMs: number
    duration: string
    genre: string

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
        releaseDate: string
        popularity: number
        durationMs: number
        genre: string
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
        this.releaseDate = this.formatDate(data.releaseDate);
        this.popularity = data.popularity
        this.durationMs = data.durationMs
        this.duration = this.formatDuration(this.durationMs);
        this.genre = data.genre
    }

    // Convert duration from milliseconds to minute:second format
    formatDuration(durationMs: number): string {
        const minutes = Math.floor(durationMs / 60000);
        const seconds = Math.floor((durationMs % 60000) / 1000);
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }

    // Format release_date to 'YYYY-MM-DD' format
    formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toISOString().split('T')[0]; // Returns YYYY-MM-DD
    }
}