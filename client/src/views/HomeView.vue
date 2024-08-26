<script setup lang="ts">
import Button from 'primevue/button';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";
import PreviouslyPlayed from "@/components/PreviouslyPlayed.vue";
import QrcodeVue from 'qrcode.vue'
import AddMoreSong from "@/components/AddMoreSong.vue";
import { sessionService } from "@/services/sessionService";
import { ref, onMounted, computed } from "vue";
import { Session } from "@/types/Session";
import { useAuthStore } from "@/stores/auth";
import { useRouter, useRoute } from 'vue-router';
import Sidebar from "primevue/sidebar";
import SessionHistoryItem from "@/components/SessionHistoryItem.vue";
import StartBlendButton from "@/components/StartBlendButton.vue";
import PlaylistCreator from "@/components/PlaylistCreator.vue";

const showPreviouslyPlayed = ref(false);
const showAddMoreSongPopup = ref(false);

const LOCAL_IP_ADDRESS = import.meta.env.VITE_LOCAL_IP_ADDRESS;

const toggleVisibility = () => {
  showPreviouslyPlayed.value = !showPreviouslyPlayed.value;
};

const router = useRouter();
const route = useRoute();

const sessions = ref<Session[]>([]);

const authStore = useAuthStore();
const isHost = authStore.user?.isHost ?? false;
const errorMessage = ref();

onMounted(async () => {
  await router.isReady();

  try {
    // This path is accesable only by guests.
    if (isHost) {
      sessions.value = await sessionService.getSessions();
    } else if (route.params.sessionId) {
      sessions.value = [await sessionService.getSessionById(route.params.sessionId)];
    } else {
      errorMessage.value = "Could not find session. Please try to join again."
    }
  } catch (error) {
    // We redirect users to landing page, if we have any errors.
    router.push({name: 'landing'});
  }
});
const selectedSessionIndex = ref(0);

const currentSession = computed(() => {
  if (sessions.value && sessions.value.length) {
    return sessions.value[selectedSessionIndex.value];
  }

  return null;
});

const toggleAddMoreSongPopup = () => {
  showAddMoreSongPopup.value = !showAddMoreSongPopup.value;
};

const flowerData = [
  { value: 0.4, color: '#144550' },
  { value: 0.6, color: '#31431E' },
  { value: 0.5, color: '#EEE8C4' },
  { value: 0.7, color: '#E4832E' },
  { value: 0.3, color: '#BB7DEC' },
];

const sessionHistoryVisible = ref(false);
const createNewSessionFlow = ref(false);
const runningSession = ref();

const startSession = async (session) => {
  sessions.value = [await sessionService.createNewSession(session), ...sessions.value];
  createNewSessionFlow.value = false;
  selectedSessionIndex.value = 0;
};

</script>

<template>
  <div class="type2">
    <header>
      <div v-if="currentSession?.isRunning" class="function-icon-container">
        <Button icon="pi pi-search" severity="success" text raised rounded aria-label="Search" @click="toggleAddMoreSongPopup" />
      </div>
      <div class="logo-nav-container">
        <logo-intro-screen/>
      </div>
      <i v-if="isHost" class="settings-icon pi pi-cog" @click="sessionHistoryVisible = true"></i>
    </header>
    <div>
      <Sidebar
          v-model:visible="sessionHistoryVisible"
          :showCloseIcon="false">
          <div class="session-history-container">
              <session-history-item
                  class="session-history"
                  v-for="(session, index) in sessions"
                  :session="session"
                  @click="() => selectedSessionIndex = index"
              />
          </div>
      </Sidebar>
    </div>
    <div class="middle">
        <div v-if="errorMessage" class="error">
          {{errorMessage}}
        </div>
        <start-blend-button v-else-if="!createNewSessionFlow && !currentSession?.isRunning && isHost" @click="createNewSessionFlow = true" />
        <div class="visualization" v-else-if="!createNewSessionFlow" :class="{ expanded: !showPreviouslyPlayed }">
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
          <Flower :features="flowerData" :size="300" :circleRadius="100" />
        </div>
        <playlist-creator v-else @startSession="startSession"></playlist-creator>
    </div>
    <div v-if="currentSession" class="footer-section">
      <div
        class="previously-played"
        :class="{ minimized: !showPreviouslyPlayed }"
      >
        <div class="table-header-container">
          <h3>Previously Played</h3>
          <button
            class="text-sm rounded min-h-[32px] px-3 py-0.5 font-semibold hover:bg-gray-800"
            @click="toggleVisibility"
          >
            {{ showPreviouslyPlayed ? "Hide" : "Show" }}
          </button>
        </div>
        <div v-show="showPreviouslyPlayed" class="table-scroll">
          <PreviouslyPlayed
            :songs="currentSession.playlist"
            ></PreviouslyPlayed>
        </div>
      </div>
      <qrcode-vue v-if="isHost" :value="currentSession.inviteLink" />
    </div>

    <!-- Popup Overlay -->
    <div v-if="showAddMoreSongPopup" class="popup-overlay" @click="toggleAddMoreSongPopup">
      <div class="popup-content" @click.stop>
        <AddMoreSong @close-popup="toggleAddMoreSongPopup"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.function-icon-container {
  position: absolute;
  top: 55px;
  left: 40px;
  z-index: 1000;
}

.function-icon-container button {
  width: 45px;
  height: 45px;
  align-items: center;
  justify-content: center;
  background-color: #6BA149;
  color: #D9D9D9;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  border-radius: 25%;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.function-icon-container button:hover {
  background-color: #6AA834;
  transform: scale(1.05);
}

.previously-played.minimized{
  height: auto;
}

.previously-played{
  background-color: var(--backcore-color1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  overflow-y: hidden;
  box-sizing: border-box;
  border-radius: 18px;
  text-align: left;
  color: #FFFFFF;
  transition: all 0.5s ease;
  max-height: 23vh;
  width: 100%;
}

.previously-played .table-header-container {
  display: flex;
  flex-direction: row;  /* Aligns the header and button horizontally */
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: #272525;
}
.previously-played.minimized .table-header-container {
  padding-bottom: 0; /* No padding when minimized */
}
.previously-played:not(.minimized) .table-header-container {
  padding-bottom: 10px; /* Adds space between the header/button and the table when shown */
}
.previously-played h3 {
  margin: 0;
  font-size:16px;
  width: 100%;
}
.previously-played button {
  padding: 8px 16px;
  background-color: #6BA149;
  color: #D9D9D9;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.previously-played button:hover {
  background-color: #6AA834;
  transform: scale(1.05); /* Slightly enlarge the button on hover */
}
.previously-played .table-scroll {
  max-height: 700px;
  overflow-y: auto;
  overflow-x: hidden;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
}

.footer-section {
  display: flex;
  flex-direction: row;
  margin: 0 20px 20px;
  gap: 8px;
  justify-content: space-between;
}
.settings-icon {
    position: absolute;
    right: 30px;
    color: var(--logo-highlight-color);
    font-size: 30px;
    cursor: pointer;
}

.visualization {
  display: contents;
}

.session-history-container {
  background-color: var(--backcore-color2);
  padding-top: 20px;
  height: 100vh;
  width: 30vw;
  position: relative;
}

.error {
  color: var(--font-color);
}
</style>
