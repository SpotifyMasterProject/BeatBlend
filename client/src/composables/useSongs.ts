import { ref, computed } from 'vue';

export function useSongs(initialSongs) {
    const songs = ref(initialSongs);
    const filteredSongs = ref([]);
    const selectedSong = ref(null);
    const selectedSongs = ref([]);

    // Combines the artists into a single string.
    const combineArtists = (artists) => {
        return artists.join(', ');
    };

    // Compute the songs not already selected.
    const notSelectedSongs = computed(() => {
        const selectedSongsIds = selectedSongs.value.map((song) => song.id);
        return songs.value.filter((song) => !selectedSongsIds.includes(song.id));
    });

    // Function which is executed by the autocomplete component,
    // which filters the songs, based on the user query.
    const search = (event) => {
        console.log('Search triggered with query');
        if (!event.query.trim().length) {
            filteredSongs.value = [...notSelectedSongs.value];
        } else {
            filteredSongs.value = notSelectedSongs.value.filter((song) => {
                const query = event.query.toLowerCase();
                return song.name.toLowerCase().startsWith(query) ||
                    combineArtists(song.artists).toLowerCase().startsWith(query);
            });
        }
        console.log('Songs have been filtered');
    };

    // Selects a song from the autocomplete options and adds it to the
    // selected song list.
    const selectSong = () => {
        selectedSongs.value = [...selectedSongs.value, selectedSong.value];
        selectedSong.value = null;
    }

    // Removes a song from the selected list.
    const removeSong = (songToRemove) => {
        selectedSongs.value = selectedSongs.value.filter(song => song.id !== songToRemove.id);
    };

    return {
        songs,
        filteredSongs,
        selectedSong,
        selectedSongs,
        combineArtists,
        search,
        selectSong,
        removeSong,
        notSelectedSongs,
    };
}