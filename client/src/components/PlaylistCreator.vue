<script setup>
import { ref, computed } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import SongSelector from "@/components/SongSelector.vue";
import { Song } from '@/types/Song';

const title = ref('');
const selectedSongs = ref([]);

// TODO: Get from BE.
const initialSongs = [
    new Song({
        id: "123",
        name: "Cruel Summer",
        artists: ["Taylor Swift"]
    }),
     new Song({
        id: "234",
        name: "Cruel Summer1",
        artists: ["Taylor Swift"]
    }),
    new Song({
        id: "345",
        name: "Cruel Summer2",
        artists: ["Taylor Swift"]
    }),
     new Song({
        id: "456",
        name: "Cruel Summer3",
        artists: ["Taylor Swift"]
    }),
    new Song({
        id: "567",
        name: "Not Like Us",
        artists: ["Kendrick Lamar"]
    }),
    new Song({
        id: "678",
        name: "Too Sweet",
        artists: ["Hozier"]
    }),
     new Song({
        id: "789",
        name: "Guess",
        artists: ["Charli xcx", "Billie Eilish"]
    }),
];

// True, if the session can be started.
// Currently, if the user selected at least 3 songs and a title.
const canStartSession = computed(() => {
    return selectedSongs.value.length >= 3 && title.value;
});

const startSession = () => {
    // TODO: Call BE with the selected songs.
    console.log("Start Session");
};

</script>

<template>
    <div class="playlist-creator">
        <InputText class="title" type="text" v-model="title" placeholder="Playlist Title..." />
        <SongSelector
            :selectedSongs="selectedSongs"
            @update:selectedSongs="val => selectedSongs = val"
            :initialSongs="initialSongs" headerText="Add 3 songs to start the blend" />
        <Button class="start-session" :disabled="!canStartSession" @click="startSession">
            Start
        </Button>
    </div>
</template>

<style>

.playlist-creator {
    --margin-inline: 20px;
    background-color: var(--backcore-color3);
    width: min(700px, 90vw);
    height: min(600px, 60vh);
    display: flex;
    flex-direction: column;
    gap: 8px;
    border-radius: 20px;
    position: relative;
}

.title {
    margin: var(--margin-inline) 32px 5px;
    width: 70%;
    font-weight: 700;
    font-size: 25px;
    border: none;
}

.title, .songs input {
  background-color: var(--backcore-color3);
  font-family: inherit;
  color: var(--font-color);
}

input:focus {
    outline: none;
}

.songs .search.p-autocomplete ::placeholder {
    color: var(--backcore-color3);
}

.p-autocomplete-overlay.overlay {
    margin-top: 10px;
    background-color: var(--backcore-color3);
    color: var(--font-color);
    font-family: inherit;
    border-radius: 10px;
    overflow-y: auto;
    padding: 5px;
    width: 30%;
}

.start-session {
    position: absolute;
    bottom: 20px;
    right: var(--margin-inline);
    font-size: 16px;
    background-color: var(--logo-highlight-color);
    border-radius: 12px;
    border: none;
    padding: 8px 20px;
    cursor: pointer;
    font-weight: bold;
    color: white;
}
.start-session:disabled {
    color: #c4c4c4;
}
</style>
