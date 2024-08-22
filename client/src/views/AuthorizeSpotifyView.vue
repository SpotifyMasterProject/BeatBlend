<script setup lang="ts">
import {onMounted, ref} from 'vue'
import {authService} from '@/services/authService'
import { useRouter } from 'vue-router'

const urlParams = new URLSearchParams(window.location.search)
const code = urlParams.get('code')
const state = urlParams.get('state')

const router = useRouter();

onMounted(async () => {
  if (code != null) {
    await authService.authorizeSpotify('username_placeholder', code)
        .then((response) => {
          router.push('session');
        })
        .catch((error) => {
          router.push('landing');
        })
  }
})

</script> 