<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { Session } from "@/types/Session";
import { useAuthStore } from "@/stores/auth";
import { useRouter, useRoute } from 'vue-router';
import Navigation from "@/components/Navigation.vue";
import MainVisualization from "@/components/MainVisualization.vue";
import VisualizationAid from '@/components/VisualizationAid.vue';
import Button from 'primevue/button';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import PreviouslyPlayed from "@/components/PreviouslyPlayed.vue";
import QrcodeVue from 'qrcode.vue'
import AddMoreSong from "@/components/AddMoreSong.vue";
import Sidebar from "primevue/sidebar";
import StartBlendButton from "@/components/StartBlendButton.vue";
import PlaylistCreator from "@/components/PlaylistCreator.vue";
import { HostSession } from "@/types/Session";
import { sessionService } from "@/services/sessionService";

const showPreviouslyPlayed = ref(false);
const showAddMoreSongPopup = ref(false);
const showVisualizationAid = ref(false);

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
const loading = ref(true);

onMounted(async () => {
  await router.isReady();

  const sessionId = isHost ? authStore.user?.sessions?.[0] : route.params.sessionId;
  if (!sessionId) {
    if (!isHost) {
      errorMessage.value = "Could not find session. Please try to join again."
    }
    loading.value = false;
    return;
  }

  try {
    sessions.value = [await sessionService.getSessionById(sessionId)];
    loading.value = false;
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

const createNewSessionFlow = ref(false);
const runningSession = ref();

const startSession = async (session) => {
  sessions.value = [await sessionService.createNewSession(session), ...sessions.value];
  createNewSessionFlow.value = false;
  selectedSessionIndex.value = 0;
};

//Information Button to read more about how the visualization can be read
const infoVisible = ref(true);
function toggleInfo(){
  showVisualizationAid.value = !showVisualizationAid.value;
}
const closeVisualizationAid = () => {
  showVisualizationAid.value = false;
};
</script>

<template>
  <div class="type2">
    <header>
      <div class="function-icon-container">
        <Button icon="pi pi-search" severity="success" text raised rounded aria-label="Search" @click="toggleAddMoreSongPopup" />
      </div>
      <div class="logo-nav-container">
        <logo-intro-screen/>
        <nav>
          <Navigation/>
        </nav>
      </div>
      <i v-if="isHost" class="settings-icon pi pi-cog"></i>
    </header>
    <div class="middle" v-if="!loading">
      <div v-if="errorMessage" class="error">
          {{errorMessage}}
      </div>
      <div v-else-if="!sessions.length && isHost">
        <start-blend-button v-if="!createNewSessionFlow" @click="createNewSessionFlow = true" />
        <playlist-creator v-else @startSession="startSession"></playlist-creator>
      </div>
      <template v-else>
        <div class="info-box" :class="{ active: showVisualizationAid }" @click="toggleInfo">
          <div> i </div>
        </div>
        <MainVisualization />
      </template>
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
    <!-- Conditionally render VisualizationAid component -->
    <VisualizationAid v-if="showVisualizationAid" @close-popup="closeVisualizationAid" />/>
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

.error {
  color: var(--font-color);
}
</style>
