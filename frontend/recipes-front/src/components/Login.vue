<script lang="ts">
import router from '@/router'
import { StateKey } from '@/types/auth'
import { defineComponent } from 'vue'
interface LogInComponentData {
  email: string
  verifyFlg: boolean
  errorCodeFlg: boolean
  codeArray: Array<string | null>
  seconds: number
  timerID?: number
}
export default defineComponent({
  props: {},
  inject: {
    state: { from: StateKey },
  },
  data(): LogInComponentData {
    return {
      email: '',
      verifyFlg: false,
      seconds: 0,
      codeArray: Array(6).fill(null),
      errorCodeFlg: false,
    }
  },
  methods: {
    startTimer(): void {
      this.stopTimer()
      this.timerID = setInterval(() => {
        this.seconds--
        if (this.seconds <= 0) {
          this.stopTimer()
        }
      }, 1000)
    },
    stopTimer(): void {
      if (this.timerID) {
        clearInterval(this.timerID)
      }
    },
    sendVerifyCode(event: Event): void {
      event.preventDefault()
      this.errorCodeFlg = false
      this.verifyFlg = true
      this.seconds = 5
      this.startTimer()
      this.$nextTick(() => this.$refs.inputs[0].focus())
      return
    },
    isInputValid(value: string | null): boolean {
      if (value === null) return false
      try {
        const parsed = Number.parseInt(value)
        return parsed >= 0 && parsed < 10
      } catch {
        return false
      }
    },
    handleInput(event: Event, idx: number): void {
      if (this.isInputValid(this.codeArray[idx])) {
        if (idx != 5) this.$refs.inputs[idx + 1].focus()
        else {
          this.verifyCode()
        }
      } else {
        this.codeArray[idx] = null
      }
    },
    handleDelete(event: Event, idx: number): void {
      if (idx != 0 && this.codeArray[idx] === null)
        this.$nextTick(() => this.$refs.inputs[idx - 1].focus())
    },
    handlePaste(event: Event) {
      event.preventDefault()
      const pasteData = event.clipboardData.getData('text/plain').trim()
      if (/^\d{6}$/.test(pasteData)) {
        this.codeArray = pasteData.split().slice(0, 6)

        this.$nextTick(() => {
          this.$refs.inputs[5].focus()
          this.verifyCode()
        })
      }
    },
    async verifyCode(): Promise<void> {
      const isValid: boolean = this.codeArray.join('') === '123456'
      if (isValid && this.state) {
        this.state.userToken = 'asdab'
        this.state.user = {
          name: 'John',
          email: 'john@smith.ru',
        }
        console.log(this.state)
        router.push('/')
      } else {
        this.errorCodeFlg = true
        this.codeArray = Array(6).fill(null)
        this.$refs.inputs[0].focus()
      }
    },
  },
  computed: {
    allowedReSend(): boolean {
      return this.seconds === 0
    },
    allowedSend(): boolean {
      const re: RegExp = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return re.test(this.email)
    },
    formatedTimer(): string {
      return !this.allowedReSend
        ? `через ` +
            new Intl.DateTimeFormat('default', {
              minute: '2-digit',
              second: '2-digit',
            }).format(new Date(this.seconds * 1000))
        : ''
    },
  },
  mounted() {
    console.log(this.state)
  },
})
</script>

<template>
  <h1>Страница авторизации</h1>
  <form v-if="!verifyFlg" class="flex-col">
    <label for="email">Введите email: {{ email }}</label>
    <input type="email" id="email" v-model="email" placeholder="john@smith.com" />
    <button @click="sendVerifyCode" :disabled="!allowedSend">Отправить код подтверждения</button>
  </form>
  <form v-else class="flex-col">
    <label>Код подтверждения направлен на {{ email }}: </label>
    <div class="code-block">
      <input
        v-for="(code, idx) of codeArray"
        :id="`${idx}`"
        type="text"
        @input="handleInput($event, idx)"
        @keydown.delete="handleDelete($event, idx)"
        class="code-cell"
        :class="codeArray[idx] ? 'code-fill-cell' : ''"
        ref="inputs"
        v-model="codeArray[idx]"
      />
    </div>

    <button :disabled="!allowedReSend" @click="sendVerifyCode">
      Запросить код подтверждения повторно {{ formatedTimer }}
    </button>
  </form>
  <div v-if="errorCodeFlg" class="error-code">Введён неверный код</div>
</template>

<style>
.error-code {
  display: flex;
  text-align: center;
  border: 10px red;
  border-radius: 4px;
  font-weight: bold;
}
.flex-col {
  display: flex;
  flex-direction: column;
}
.code-cell {
  display: block;
  height: 21%;
  width: 7%;
  /* margin: 2px; */
  margin-top: 1%;
  margin-bottom: 1%;
  text-align: center;
  border-radius: 4px;
}
.code-fill-cell {
  background-color: rgb(164, 148, 129);
}
.code-block {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
