<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <!-- Logo -->
      <img src="https://img.icons8.com/ios/452/book.png" alt="logo" width="30" height="30" class="d-inline-block align-top logo">
      <a class="navbar-brand">Pallavi Library Management</a>

      <!-- Search Form -->
      
      <!-- Navbar Links -->
      <div class="navbar-links">
        <div v-if="role === 'admin'" class="admin-links">
          <router-link to="/librarian-dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/requests" class="nav-link">Requests <span style="color: red; border: 2px solid black;padding:2px 10px; "> {{ no_of_requests }}</span> </router-link>
          <router-link to="/status" class="nav-link">Stats</router-link>
        </div>
        <div v-else-if="role === 'stud'" class="student-links">
          <router-link to="/my-books" class="nav-link">My Books</router-link>
          <router-link to="/user-dashboard" class="nav-link">My Dashboard</router-link>
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
      role: "",
      is_login: "",
      no_of_requests: 0,
    };
  },
  created() {
    this.role = localStorage.getItem('role');
    this.is_login = localStorage.getItem('auth-token') !== null;
    if (this.role === 'admin'){
      this.fetch_requests();
    }
    
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('role');
      // reload
      this.$router.push({ path: '/login' });
    },
    fetch_requests() {
      fetch('http://127.0.0.1:5000/requests',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('auth-token')
        }
      })
        .then(res => res.json())
        .then(data => {
          // filter unapproved requests
          data = data.filter(request => request.status === 'requested');
          this.no_of_requests = data.length;
        });
      
  }
  },
}
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
