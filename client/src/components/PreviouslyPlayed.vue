<template>
  <div class="song-table-container">
    <div class="song-table">
      <table>
        <thead>
          <tr>
            <th class="icon-header"></th>  <!-- Empty for the icon -->
            <th class="track-name">Track Name</th>
            <th>Album</th>
            <th>Artists</th>
            <th>Danceability</th>
            <th>Energy</th>
            <th>Speechiness</th>
            <th>Valence</th>
            <th>Tempo</th>
            <th>Popularity</th>
            <th>Release Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="song in songs" :key="song.id">
            <td class="icon-cell">
              <img src="../assets/table-play-icon.png" alt="play-icon" class="song-icon">
            </td>
            <td class="track-name">{{ song.name }}</td>
            <td>{{ song.album }}</td>
            <td>{{ song.artists.join(', ') }}</td>
            <td>{{ song.danceability }}</td>
            <td>{{ song.energy }}</td>
            <td>{{ song.speechiness }}</td>
            <td>{{ song.valence }}</td>
            <td>{{ song.tempo }}</td>
            <td>{{ song.popularity }}</td>
            <td>{{song.release_date}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Song } from '@/types/Song';

const songs = ref([
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
    })
])


</script>

<style scoped>
.song-table-container {
  background-color: #363636;
  padding: 5px 0px 5px 0px;
  border-radius: 15px;
  overflow: hidden;
}

.song-table {
  width: 100%;
  color: #D9D9D9;
  overflow: hidden;
}

.song-table table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 15px;
  table-layout: fixed;
  overflow: hidden;
}
.song-table th {
  padding: 8px;
  text-align: center;
  word-wrap: break-word;
  border-bottom: 1px solid transparent;
  color: #D9D9D9;
  font-size: 15px;
  font-weight: bold;
}
.song-table td {
  padding: 8px;
  text-align: center;
  word-wrap: break-word;
  border-bottom: 1px solid transparent;
  color: #D9D9D9;
  font-size: 14px;
}

.song-table th.icon-header, .song-table td.icon-cell {
  width: 20px;
  text-align: center;
}

.song-table th.track-name, .song-table td.track-name {
  width: 180px;
}

.song-table img.song-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
}
</style>