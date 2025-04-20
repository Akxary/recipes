<script lang="ts">
    export default {
        props() {
            timer: Number
        },
        data() {
            return {
                allowed: false,
            }
        },
        mounted() {
            setTimeout(()=>this.allowed=true, 120000)
        }
    }
</script>

<template>
  <form class="flex-col">
    <label for="code">Код подтверждения:</label>
    <input type="number" id="code" />
    <button :disabled="!allowed">Запросить код повторно</button>
  </form>
</template>
