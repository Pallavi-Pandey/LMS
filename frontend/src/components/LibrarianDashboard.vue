<template>
  <div class="container-fluid bg-light p-3">
    <div class="row">
      <div class="col-md-12">
        <h1>Librarian Dashboard</h1>
      </div>
    </div>

    <!-- Section Management -->
    <div class="row">
      <div class="col-md-12">
        <div class="card mt-4">
          <div class="card-header">
            <h3>Section Management</h3>
          </div>
          <div class="card-body">
            <ul>
              <div v-for="section in sections" :key="section.id">
                <router-link :to="`/section/${section.id}`" class="btn-primary">{{ section.name }}</router-link>
                <span class="badge bg-secondary">{{ section.books.length }}</span>Books
                <button type="button" class="btn btn-primary">Update</button>
                <button type="button" class="btn btn-danger" @click="confirmDelete(section.id)">Delete</button>
              </div>
            </ul>
          </div>
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSectionModal">
            Add Section
          </button>
        </div>
      </div>
    </div>

    <!-- Add Section Modal -->
    <div class="modal fade" id="addSectionModal" tabindex="-1" aria-labelledby="addSectionModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="addSectionModalLabel">Add Section</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSection">
              <div class="mb-3">
                <label for="sectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control" id="sectionName" v-model.trim="sectionName" required>
              </div>
              <button type="submit" class="btn btn-primary">Add Section</button>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Section Confirmation Modal -->
    <div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-labelledby="confirmDeleteModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="confirmDeleteModalLabel">Confirm Delete</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this section?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="deleteSection">Yes, Delete</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sectionName: '',
      sections: [],
      sectionToDelete: null
    };
  },
  methods: {
    async addSection() {
      const sectionData = {
        name: this.sectionName
      };
      try {
        const response = await fetch('http://127.0.0.1:5000/add-section', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify(sectionData)
        });
        if (!response.ok) {
          throw new Error('Unable to add section');
        }
        const data = await response.json();
        console.log('Section added successfully', data);
        $('#addSectionModal').modal('hide');
        this.sectionName = '';
        this.getSections();
      } catch (error) {
        console.error('Error adding section:', error);
      }
    },
    confirmDelete(sectionId) {
      this.sectionToDelete = sectionId;
      $('#confirmDeleteModal').modal('show');
    },
    async deleteSection() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete-section/${this.sectionToDelete}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          }
        });
        if (!response.ok) {
          throw new Error('Unable to delete section');
        }
        console.log('Section deleted successfully');
        $('#confirmDeleteModal').modal('hide');
        this.getSections(); // Refresh the section list
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    async getSections() {
      try {
        const response = await fetch('http://127.0.0.1:5000/sections', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          }
        });
        if (!response.ok) {
          throw new Error('Unable to fetch sections');
        }
        const data = await response.json();
        this.sections = data;
        console.log('Sections fetched successfully', data);
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    }
  },
  async mounted() {
    // Fetch sections when the component is mounted
    this.getSections();
  }
};
</script>

<style scoped>
/* Add scoped styles for the librarian dashboard */
.card {
  margin-bottom: 20px;
}

</style>
