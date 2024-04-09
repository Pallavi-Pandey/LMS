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

      <!-- Links to Dashboards -->
      <router-link to="/librarian-dashboard" class="nav-link ms-auto">Librarian Dashboard</router-link>
      <router-link to="/user-dashboard" class="nav-link">User Dashboard</router-link>
    </div>
  </nav>
</template>

<script>
export default {
};
</script>

