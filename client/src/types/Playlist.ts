import { Song } from '@/types/Song';

export class Playlist {
    playedSongs: Song[]
    currentSong: Song | null
    queuedSongs: Song[]

    constructor(data: Playlist) {
        this.playedSongs = data.playedSongs
        this.currentSong = data.currentSong
        this.queuedSongs = data.queuedSongs
    }
}
