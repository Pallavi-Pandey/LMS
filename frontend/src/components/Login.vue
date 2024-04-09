<template>
    <div class="login">
      <h2 style="text-align: center; padding-top: 1cm; color: #007bff;">Welcome to the Login Page</h2>
      <div>
        <h2>Login</h2>
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="username">Username/Email:</label>
            <input type="text" id="username" v-model.trim="email" required>
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model.trim="password" required>
          </div>
          <button type="submit" class="btn-primary">Login</button>
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
      login() {
        if (!this.email || !this.password) {
          this.errormsg = "Please enter both email and password.";
          this.errStatus = true;
          return;
        }
  
        fetch("https://api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",\
          },
          body: JSON.stringify({
            user_id: this.email,
            password: this.password,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Unable to log in. Please try again later.");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data.msg);
            if (data.status) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("user_id", this.email);
              localStorage.setItem("username", data.username);
              this.$router.push("/dashboard");
            } else {
              this.errStatus = true;
              this.errormsg = data.msg;
              this.email = ""; // Reset email field
              this.password = ""; // Reset password field
            }
          })
          .catch((err) => {
            console.error(err);
            this.errStatus = true;
            this.errormsg = "Unable to log in. Please try again later.";
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f4f4f4;
    border-radius: 5px;
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
  
  input[type="text"],
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
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
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
    color: #007bff;
    text-decoration: none;
  }
  
  p router-link:hover {
    text-decoration: underline;
  }
  </style>
  