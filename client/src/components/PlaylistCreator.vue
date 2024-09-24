<script setup>
import { ref, computed, } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import SongSelector from "@/components/SongSelector.vue";
import { Song } from '@/types/Song';
import { Session } from "@/types/Session";

const title = ref('');
const selectedSongs = ref([]);
const emit = defineEmits(['startSession']);

// True, if the session can be started.
// Currently, if the user selected at least 3 songs and a title.
const canStartSession = computed(() => {
    return selectedSongs.value.length >= 3 && title.value;
});

const startSession = async () => {
    emit('startSession', new Session({
        name: title.value,
        playlist: selectedSongs.value,
    }));
};

</script>
<template>
    <div class="playlist-creator">
        <InputText class="title" type="text" v-model="title" placeholder="Playlist Title..." />
        <SongSelector
            v-model="selectedSongs"
            headerText="Add 3 songs to start the blend" />
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
    width: min(30%, 300px);
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
    color: var(--button-disabled-font-color);
}
</style>
