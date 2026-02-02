<template>
  <div class="login-container">
    <div class="login-card glass-panel">
      <h2 class="text-center mb-4 brand-title">Welcome Back</h2>
      <p class="text-center text-muted mb-4">Sign in to your account</p>
      
      <form @submit.prevent="login" class="login-form">
        <div class="mb-3">
          <label for="email" class="form-label">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model.trim="email" 
            class="form-control custom-input" 
            placeholder="name@example.com" 
            required>
        </div>
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password" 
            class="form-control custom-input" 
            placeholder="••••••••" 
            required>
        </div>
        
        <button class="btn btn-premium w-100 py-2 rounded-3 shadow-sm">
          Sign In
        </button>

        <div v-if="errStatus" class="alert alert-danger mt-3 py-2 text-center text-small">
          {{ errormsg }}
        </div>
      </form>

      <div class="text-center mt-4">
        <p class="text-muted small">
          New here? 
          <router-link to="/signup" class="text-primary fw-bold text-decoration-none">
            Create an account
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// Use relative path or env var, defaulting to relative for proxy support
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export default {
  name: "LoginForm",
  data() {
    return {
      email: "",
      password: "",
      errormsg: "",
      errStatus: false,
    };
  },
  methods: {
    async login() {
      if (!this.email || !this.password) {
        this.errormsg = "Please enter both email and password.";
        this.errStatus = true;
        return;
      }

      try {
        const res = await fetch(`${API_URL}/user-login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });
        const data = await res.json();
        
        if (res.ok) {
          localStorage.setItem('auth-token', data.token);
          localStorage.setItem('role', data.role);
          localStorage.setItem('email', data.email);
          
          if (data.role[0] === 'admin') {
            this.$router.push({ path: '/librarian-dashboard' });
          } else {
            this.$router.push({ path: '/user-dashboard' });
          }
          // Force UI update
          setTimeout(() => window.location.reload(), 50);
        } else {
          this.errormsg = data.message || "Login failed";
          this.errStatus = true;
        }
      } catch (error) {
        console.error(error);
        this.errormsg = "Network error. Please try again.";
        this.errStatus = true;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at top left, rgba(79, 70, 229, 0.05), transparent),
              radial-gradient(circle at bottom right, rgba(99, 102, 241, 0.05), transparent);
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
  background: rgba(255, 255, 255, 0.85); /* Fallback */
}

.brand-title {
  color: var(--vt-c-indigo);
  font-weight: 700;
  letter-spacing: -0.5px;
}

.custom-input {
  border: 1px solid #e5e7eb;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background-color: #f9fafb;
  transition: all 0.2s;
}

.custom-input:focus {
  border-color: #4f46e5;
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

.form-label {
  font-weight: 500;
  font-size: 0.9rem;
  color: #374151;
  margin-bottom: 0.5rem;
}

.text-small {
  font-size: 0.875rem;
}
</style>
