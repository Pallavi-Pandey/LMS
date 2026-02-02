<template>
  <div class="signup-container">
    <div class="signup-card glass-panel">
      <h2 class="text-center mb-4 brand-title">Create Account</h2>
      <p class="text-center text-muted mb-4">Join LMS Portal today</p>
      
      <form @submit.prevent="signup" class="signup-form">
        <div class="mb-3">
          <label for="username" class="form-label">Full Name</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            class="form-control custom-input" 
            placeholder="John Doe" 
            required>
        </div>
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
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password" 
            class="form-control custom-input" 
            placeholder="Create a password" 
            required>
        </div>
        <div class="mb-4">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model.trim="confirmPassword" 
            class="form-control custom-input" 
            placeholder="Confirm password" 
            required>
        </div>

        <button class="btn btn-premium w-100 py-2 rounded-3 shadow-sm">
          Sign Up
        </button>

        <div v-if="errorMsg" class="alert alert-danger mt-3 py-2 text-center text-small">
          {{ errorMsg }}
        </div>
      </form>

      <div class="text-center mt-4">
        <p class="text-muted small">
          Already have an account? 
          <router-link to="/login" class="text-primary fw-bold text-decoration-none">
            Sign In
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// Use relative path or env var
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      errorMsg: ''
    };
  },
  methods: {
    async signup() {
      this.errorMsg = '';
      if (this.password !== this.confirmPassword) {
        this.errorMsg = "Passwords do not match";
        return;
      }

      const userData = {
        name: this.username,
        email: this.email,
        password: this.password
      };

      try {
        const res = await fetch(`${API_URL}/register`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*", 
          },
          body: JSON.stringify(userData),
        })
        const data = await res.json()
        
        if (res.ok) {
          alert('Registration successful! Please login.');
          this.$router.push({ path: '/login' })
        } else {
          this.errorMsg = data.message || "Registration failed";
        }
      } catch (err) {
        console.error(err);
        this.errorMsg = "Network error";
      }
    }
  }
};
</script>

<style scoped>
.signup-container {
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at top right, rgba(79, 70, 229, 0.05), transparent),
              radial-gradient(circle at bottom left, rgba(99, 102, 241, 0.05), transparent);
}

.signup-card {
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
  background: rgba(255, 255, 255, 0.85);
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