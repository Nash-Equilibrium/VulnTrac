<template>
    <mi-login :action="handelLogin" :socialite-setting="{ domain: 'http://local-account.makeit.vip/v1/oauth' }" />
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
const handelLogin = (data: any) => {
    router.push('/dashboard')
}
</script>