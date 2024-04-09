<template>
  <div>
    <div class="container-fluid bg-light p-3">
      <div class="row">
        <div class="col-md-2">
          <h1>Librarian Dashboard</h1>
        </div>
        <div class="col-md-10">
          <div class="card">
            <div class="card-header">
              Recent Activities
            </div>
            <div class="card-body">
              <ul>
                <li>User A issued Book X</li>
                <li>User B returned Book Y</li>
              </ul>
            </div>
          </div>
          <div class="card mt-4">
            <div class="card-header">
              Section Management
            </div>
            <div class="card-body">
              <p>Create new sections, edit existing sections, remove sections, etc.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // Add your script logic here if needed
};
</script>

<style scoped>
/* Add scoped styles for the librarian dashboard */
.card {
  margin-bottom: 20px;
}
</style>
