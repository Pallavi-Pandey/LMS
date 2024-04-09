<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <!-- Logo -->
      <img src="https://img.icons8.com/ios/452/book.png" alt="logo" width="30" height="30" class="d-inline-block align-top">
      <a class="navbar-brand">Pallavi Library</a>

      <!-- Search Form -->
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>

      <!-- Navbar Links -->

        <div v-if="role === 'admin'">
          <router-link to="/books" class="nav-link">Books</router-link>
          <router-link to="/status" class="nav-link">Status</router-link>
        </div>
        <div v-else-if="role === 'stud'">
          <router-link to="/allbooks" class="nav-link">All Books</router-link>
          <router-link to="/mydashboard" class="nav-link">My Dashboard</router-link>
        </div>

      <!-- Logout Button -->
      <button v-if="is_login" @click="logout" class="btn btn-outline-danger ms-auto">Logout</button>
    </div>
  </nav>
</template>

<script>
export default {
  data() {

    return {
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token'),
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('role');
      // reload
      this.$router.push({ path: '/login' });
    },
  },
};
</script>
