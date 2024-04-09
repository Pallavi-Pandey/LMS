<template>
  <div class="signup-container">
    <div class="signup-form">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup">
        <div class="form-group">
          <label for="username">Name:</label>
          <input type="text" id="username" v-model.trim="username" required>
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model.trim="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model.trim="password" required>
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password:</label>
          <input type="password" id="confirmPassword" v-model.trim="confirmPassword" required>
        </div>
        <button type="submit" class="btn-primary">Sign Up</button>
      </form>
      <p>Already have an account? <router-link to="/login">Login</router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    signup() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      const userData = {
        username: this.username,
        email: this.email,
        password: this.password
      };

      fetch("http://127.0.0.1:5000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*", 
        },
        body: JSON.stringify(userData),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unable to register. Please try again later.");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data.msg);
          this.$router.push('/login');
        })
        .catch((err) => {
          console.error(err);
          alert("Unable to register. Please try again later.");
        });
    }
  }
};
</script>


<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.signup-form {
  width: 300px;
  padding: 20px;
  background-color: #f3f4f6;
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

input[type="text"],
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