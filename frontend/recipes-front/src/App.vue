<script lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { defineComponent, provide } from 'vue'
import { StateKey, UpdateTokenKey } from './types/auth'

interface HeaderData {
  isNavOpen: boolean
  token: string | null
}

export default defineComponent({
  data(): HeaderData {
    return {
      isNavOpen: false,
      token: null,
    }
  },
  inject: {
    state: { from: StateKey, default: () => ({ userToken: null, user: null }) },
  },
  methods: {
    toggleNavList(event: Event): void {
      this.isNavOpen = !this.isNavOpen
    },
    logOut(event: Event): void {
      this.state.userToken = null;
      this.state.user = null;
      this.toggleNavList(event);
    },
  },
  computed: {
    isLogin(): boolean {
      return this.state.userToken !== null;
    },
  },
})
</script>

<template>
  <header>
    <div class="dropdown-container">
      <button class="dropdown-button" @click="toggleNavList">
        <img alt="Vue logo" src="@/assets/user-icon.svg" width="75" height="75" />
      </button>
      <p v-if="this.state.user">{{state.user.name}}</p>
      <ul v-if="isNavOpen" class="dropdown-menu">
        <li v-if="isLogin">
          <RouterLink to="/" @click="logOut">Выйти из аккаунта</RouterLink>
        </li>
        <li v-else>
          <RouterLink to="/log-in" @click="toggleNavList">Войти в аккаунт</RouterLink>
        </li>
      </ul>
    </div>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Домашняя страница</RouterLink>
        <RouterLink v-if="isLogin" to="/profile">Профиль</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.dropdown-container {
  position: relative;
  display: block;
}

.dropdown-button {
  /* padding: 8px 16px; */
  background: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  margin-left: auto;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  min-width: 160px;
  padding: 0;
  margin: 2px 0 0;
  list-style: none;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.dropdown-menu li {
  padding: 8px 16px;
  cursor: pointer;
}

.dropdown-menu li:hover {
  background-color: #f5f5f5;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.user-icon {
  display: block;
  margin-left: auto;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .user-icon {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
