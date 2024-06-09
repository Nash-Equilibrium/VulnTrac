<template>
    <mi-register :action="/v1/register" />
</template>

<script setup lang="ts">
const handleRegister = () => {
    console.log('register')
    // do sometion
    // return `boolean` or `string`
    return true
}
</script>