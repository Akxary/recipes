<script lang="ts">
import { StateKey } from '@/types/auth';
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      editFlg: false,
    }
  },
  inject: {
    state: { from: StateKey, default: () => ({ userToken: null, user: null }) },
  }
})
</script>

<template>
  <h1>Профиль</h1>
  <button>Отредактировать</button>
  <br>
  <label for="name">Имя:</label>
  <input :disabled="!editFlg" type="text" id="name" v-model="state.user.name" />
  <br>
  <label for="email">Email:</label>
  <input :disabled="!editFlg" type="email" id="email" v-model="state.user.email">
</template>
