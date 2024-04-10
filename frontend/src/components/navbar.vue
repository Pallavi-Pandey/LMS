<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <!-- Logo -->
      <img src="https://img.icons8.com/ios/452/book.png" alt="logo" width="30" height="30" class="d-inline-block align-top logo">
      <a class="navbar-brand">Pallavi Library Management</a>

      <!-- Search Form -->
      <form class="d-flex search-form" role="search">
        <input class="form-control me-2 search-input" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success search-btn" type="submit">Search</button>
      </form>

      <!-- Navbar Links -->
      <div class="navbar-links">
        <div v-if="role === 'admin'" class="admin-links">
          <router-link to="/librarian-dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/books" class="nav-link">Requests</router-link>
          <router-link to="/status" class="nav-link">Stats</router-link>
        </div>
        <div v-else-if="role === 'stud'" class="student-links">
          <router-link to="/allbooks" class="nav-link">All Books</router-link>
          <router-link to="/mydashboard" class="nav-link">My Dashboard</router-link>
        </div>
      </div>

      <!-- Logout Button -->
      <button v-if="is_login" @click="logout" class="btn btn-outline-danger logout-btn">Logout</button>
    </div>
  </nav>
</template>

<script>
import router from '@/router';

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

<style scoped>
.logo {
  margin-right: 10px;
}

.search-form {
  margin-right: auto;
}

.search-input {
  width: 200px;
}

.search-btn {
  margin-left: 10px;
}

.navbar-links {
  display: flex;
}

.navbar-links .nav-link {
  margin-right: 10px;
}

.admin-links {
  display: flex;
}

.student-links {
  display: flex;
}

.logout-btn {
  margin-left: 10px;
}
</style>
