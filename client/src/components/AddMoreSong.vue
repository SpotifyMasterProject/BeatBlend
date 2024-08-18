<script setup lang="ts">
import { ref, computed } from 'vue';
import Button from 'primevue/button';
import SongSelector from "@/components/SongSelector.vue";
import { Song } from '@/types/Song';


const props = defineProps({
  onClosePopup: {
    type: Function,
    required: true,
  },
});

const initialSongs = [
    new Song({
        id: '3P4SOWJr8k0iMULpLnXlGz',
        name: 'Banned From Living',
        album: 'Hostage',
        artists: ['Gloomcvlt'],
        danceability: 0.658,
        energy: 0.914,
        speechiness: 0.0356,
        valence: 0.751,
        tempo: 100.006,
        release_date: '2014',
        popularity: 23
    }),
    new Song({
        id: '0ohhx5bZqF21Fnup6wKNrm',
        name: 'Modern Waste',
        album: 'Running From A Gamble',
        artists: ['Company of Thieves'],
        danceability: 0.476,
        energy: 0.956,
        speechiness: 0.0779,
        valence: 0.642,
        tempo: 136.983,
        release_date: '2011-05-17',
        popularity: 10
    }),
    new Song({
        id: '5YN1Ck5J6xKblPFYYIzN34',
        name: 'Drunk on You',
        album: 'LionHeart',
        artists: ['Geko'],
        danceability: 0.781,
        energy: 0.879,
        speechiness: 0.111,
        valence: 0.79,
        tempo: 109.958,
        release_date: '2017-03-10',
        popularity: 16
    }),
    new Song({
        id: '5gyYY2RTMy7vmxmW3t6iDK',
        name: 'Como Ayer',
        album: 'Sin Restricciones',
        artists: ['La Energia Nortena'],
        danceability: 0.565,
        energy: 0.577,
        speechiness: 0.0537,
        valence: 0.625,
        tempo: 90.437,
        release_date: '2013-05-28',
        popularity: 19
    }),
    new Song({
        id: '7wU8yeQOdyXmhWvusmL6KZ',
        name: 'Papillon Des Nuits (a.k.a. "Cuban Waltz")',
        album: 'Reflections',
        artists: ['Kendra Shank'],
        danceability: 0.503,
        energy: 0.236,
        speechiness: 0.0398,
        valence: 0.348,
        tempo: 169.946,
        release_date: '2005-01-01',
        popularity: 0
    }),
    new Song({
        id: '43M3NnRvDiEftdnXBGQYmK',
        name: 'Boomerang (feat. LOLO)',
        album: 'Young Kind of Love',
        artists: ['Joey Contreras, LOLO'],
        danceability: 0.479,
        energy: 0.946,
        speechiness: 0.0931,
        valence: 0.717,
        tempo: 163.016,
        release_date: '2014-11-11',
        popularity: 2
    }),
    new Song({
      id: '1wk5J5wnnir7oXFwqWSQKC',
      name: 'Paralyzed',
      album: 'Gravity',
      artists: ['Caliban'],
      danceability: 0.42,
      energy: 0.96,
      speechiness: 0.115,
      valence: 0.0662,
      tempo: 144.985,
      release_date: '2016-03-25',
      popularity: 40
    })
]

const selectedSongs = ref([]);

const canConfirm = computed(() => {
    return selectedSongs.value.length >= 1;
});

//TODO: call BE to add new songs to playlist when confirmed
const addNewSongs = () => {
    console.log("add new songs!")


    // clear the previous selected songs\
    selectedSongs.value = [];
}

</script>

<template>
    <div class="playlist-creator">
        <button class="close-button" @click="props.onClosePopup">X</button>
        <SongSelector
            :selectedSongs="selectedSongs"
            @update:selectedSongs="val => selectedSongs = val"
            :initialSongs="initialSongs"
            headerText="Add more songs to the playlist"
        />
        <Button class="start-session" :disabled="!canConfirm" @click="addNewSongs">
            Confirm
        </Button>
    </div>
</template>

<style scoped>
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
    padding-top: 30px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  border-radius: 25%;
  color: var(--font-color);
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 25px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.close-button:hover {
  background-color: var(--backcore-color1);
  color: #CCCCCC;
  transform: scale(1.07);
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