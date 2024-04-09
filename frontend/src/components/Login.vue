<template>
  <div class="login-container">
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model.trim="email" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model.trim="password" placeholder="Enter your password" required>
        </div>
        <button class="btn btn-primary mt-2"> Login </button>
        <p v-if="errStatus" class="error-msg">{{ errormsg }}</p>
      </form>
      <p>Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
    </div>
  </div>
</template>

<script>
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

      const res = await fetch("http://127.0.0.1:5000/user-login", {
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
      console.log("aaaaaaaaa",data)
      if (res.ok) {
        localStorage.setItem('auth-token', data.token);
        localStorage.setItem('role', data.role);
        // refresh
        console.log(data);
        if (data.role[0] === 'admin') {
          console.log('admin');
          this.$router.push({ path: '/librarian-dashboard' });
        } else {
          this.$router.push({ path: '/user-dashboard' });
        }
      } else {
        this.errormsg = data.message;
        this.errStatus = true;
      }
    }
  }
}
</script>
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  color: #fff;
  background-color: #47b8a9;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #199479;
}

.error-msg {
  color: red;
  margin-top: 10px;
  text-align: center;
}

p {
  text-align: center;
  margin-top: 20px;
}

p router-link {
  color: #43caa2;
  text-decoration: none;
}

p router-link:hover {
  text-decoration: underline;
}
</style>
