<script setup lang="ts">
import router from '@/router';
</script>

<template>
    <h1>Страница авторизации</h1>
    <form class="flex-col">
        <label for="email">Введите email: </label>
        <input type="email" id="email"/>
        <button @click="router.push('/verify-code')">Отправить код подтверждения</button>
    </form>

    
</template>

<style>
    .flex-col {
        display: flex; flex-direction: column;
    }
</style>