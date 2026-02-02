<template>
  <nav class="navbar navbar-expand-lg glass-panel sticky-top mb-4">
    <div class="container-fluid">
      <!-- Logo & Brand -->
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-2">
        <img src="https://img.icons8.com/ios/452/book.png" alt="logo" width="32" height="32" class="logo-img">
        <span class="brand-text">LMS Portal</span>
      </router-link>

      <!-- Toggle Button (Mobile) -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Links -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav align-items-center gap-3">
          
          <template v-if="role === 'admin'">
            <li class="nav-item">
              <router-link to="/librarian-dashboard" class="nav-link custom-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/requests" class="nav-link custom-link d-flex align-items-center gap-1">
                Requests
                <span v-if="no_of_requests > 0" class="badge rounded-pill bg-danger shadow-sm">
                  {{ no_of_requests }}
                </span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/mystats" class="nav-link custom-link">Stats</router-link>
            </li>
          </template>

          <template v-else-if="role === 'stud'">
            <li class="nav-item">
              <router-link to="/user-dashboard" class="nav-link custom-link">Explere Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/my-books" class="nav-link custom-link">My Library</router-link>
            </li>
          </template>

          <!-- Logout -->
          <li class="nav-item" v-if="is_login">
            <button @click="logout" class="btn btn-premium px-4 rounded-pill shadow-sm btn-sm">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
// ... existing script ...
import API_BASE_URL from "../config";
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
      // Force reload to update navbar state if needed, or rely on reactivity
      setTimeout(() => window.location.reload(), 100);
    },
    fetch_requests() {
      fetch(`${API_BASE_URL}/requests`,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('auth-token')
        }
      })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
             const pending = data.filter(request => request.status === 'requested');
             this.no_of_requests = pending.length;
          }
        })
        .catch(err => console.error("Error fetching requests:", err));
    }
  },
}
</script>

<style scoped>
.brand-text {
  font-weight: 700;
  font-size: 1.25rem;
  letter-spacing: -0.5px;
  color: var(--color-heading);
}

.custom-link {
  font-weight: 500;
  color: var(--color-text);
  transition: color 0.2s;
}

.custom-link:hover,
.router-link-active {
  color: #4f46e5 !important; /* Indigo-600 */
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
}

.logo-img {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}
</style>
