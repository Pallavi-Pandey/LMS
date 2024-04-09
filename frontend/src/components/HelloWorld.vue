<template>
  <div class="home">
    <header>
      <h1>Welcome to Library Management System</h1>
      <p>A comprehensive platform for managing your library resources</p>
    </header>
    <main>
      <section class="hero">
        <div class="hero-content">
          <h2>Explore a World of Knowledge</h2>
          <p>Access thousands of e-books across various genres.</p>
          <router-link to="/books" class="btn-primary">Explore Books</router-link>
        </div>
      </section>
      <section class="cta">
        <div class="cta-content">
          <h2>Join Our Community</h2>
          <p>Sign up now to start exploring and enjoying all the benefits of our library system.</p>
          <router-link to="/register" class="btn-primary">Sign Up</router-link>
          <p>Already a member?</p>
          <router-link to="/login" class="btn-secondary">Login</router-link>
        </div>
      </section>
    </main>
    <footer>
      <p>&copy; 2024 Library Management System. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  // Add any script logic if needed
};
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 50px;
}

header h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

header p {
  font-size: 18px;
  color: #666;
}

.hero {
  background-image: url('/path/to/hero-image.jpg'); /* Add your hero image URL */
  background-size: cover;
  background-position: center;
  padding: 100px 0;
  color: #fff;
  text-align: center;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero h2 {
  font-size: 42px;
  margin-bottom: 20px;
}

.hero p {
  font-size: 18px;
  margin-bottom: 30px;
}

.cta {
  background-color: #f4f4f4;
  padding: 100px 0;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta h2 {
  font-size: 36px;
  margin-bottom: 20px;
}

.cta p {
  font-size: 18px;
  margin-bottom: 30px;
}

.btn-primary, .btn-secondary {
  display: inline-block;
  padding: 10px 20px;
  font-size: 18px;
  text-decoration: none;
  color: #fff;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  margin-right: 10px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #495057;
}

footer {
  text-align: center;
  margin-top: 50px;
}

footer p {
  font-size: 14px;
  color: #666;
}
</style>
