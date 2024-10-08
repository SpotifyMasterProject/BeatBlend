import { Song } from '@/types/Song';

export class Playlist {
    played_songs: Song[]
    current_song: Song
    queued_songs: Song[]

    constructor(data: Playlist) {
        this.played_songs = data.played_songs
        this.current_song = data.current_song
        this.queued_songs = data.queued_songs
    }
}
