<template>
  <div class="dashboard-container">
    <div class="row align-items-center mb-5">
      <div class="col-md-6">
        <h1 class="display-5 fw-bold text-white mb-0">Librarian Dashboard</h1>
        <p class="text-white-50 mt-2">Manage sections, books, and requests</p>
      </div>
      <div class="col-md-6 text-end">
        <button @click="downloadResource" class="btn btn-light shadow-sm text-primary fw-bold px-4 rounded-pill" :disabled="isWaiting">
          <i class="bi bi-cloud-arrow-down me-2"></i>
          {{ isWaiting ? 'Generating Report...' : 'Download Report CSV' }}
        </button>
      </div>
    </div>

    <!-- Section Management -->
    <div class="glass-panel p-4 mb-5">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-light pb-3">
            <h3 class="m-0 text-primary fw-bold">Section Management</h3>
            <button type="button" class="btn btn-premium rounded-pill px-4" data-bs-toggle="modal" data-bs-target="#addSectionModal">
                <i class="bi bi-plus-lg me-2"></i>Add New Section
            </button>
        </div>

        <div class="row row-cols-1 row-cols-lg-2 g-4">
            <div v-for="section in sections" :key="section.id" class="col">
                <div class="section-card glass-card h-100 p-3 d-flex flex-column justify-content-between position-relative overflow-hidden">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <router-link :to="`/section/${section.id}`" class="text-decoration-none">
                            <h4 class="fw-bold text-dark m-0 section-link">{{ section.name }}</h4>
                        </router-link>
                        <span class="badge bg-primary-subtle text-primary rounded-pill px-3 py-2">
                            {{ section.books.length }} Books
                        </span>
                    </div>
                    
                    <div class="d-flex gap-2 mt-auto">
                        <button class="btn btn-sm btn-outline-primary flex-grow-1" data-bs-toggle="modal" data-bs-target="#exampleModal"
                            @click="updatemodal(section.id)">
                            Edit
                        </button>
                        <button class="btn btn-sm btn-outline-danger flex-grow-1" @click="confirmDelete(section.id)">
                            Delete
                        </button>
                    </div>
                    
                    <!-- Decorative Circle -->
                    <div class="decorative-circle"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Update Section Modal -->
    <div class="modal fade glass-modal" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-panel border-0">
          <div class="modal-header border-bottom-0">
            <h1 class="modal-title fs-5 fw-bold text-primary" id="exampleModalLabel">Update Section</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submit_section_update">
              <div class="mb-3">
                <label for="updateSectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control custom-input" id="updateSectionName" v-model.trim="sectionName" required>
              </div>
              <div class="d-grid">
                  <button type="submit" class="btn btn-premium">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Section Modal -->
    <div class="modal fade glass-modal" id="addSectionModal" tabindex="-1" aria-labelledby="addSectionModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-panel border-0">
          <div class="modal-header border-bottom-0">
            <h1 class="modal-title fs-5 fw-bold text-primary" id="addSectionModalLabel">Add New Section</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSection">
              <div class="mb-3">
                <label for="newSectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control custom-input" id="newSectionName" v-model.trim="sectionName" placeholder="e.g., Science Fiction" required>
              </div>
              <div class="d-grid">
                  <button type="submit" class="btn btn-premium">Create Section</button>
              </div>
            </form>
          </div>
          <!-- Hidden Button specific for logic (if needed) or remove if logic changed to standard modal hiding -->
           <button type="button" class="d-none" data-bs-dismiss="modal" id="close-add-section"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Keep existing script logic, just update styling
import API_BASE_URL from "../config";
export default {
    data() {
    return {
      sectionName: '',
      sections: [],
      sectionToDelete: null,
      sectionId: null,
      isWaiting: false,
    };
  },
  methods: {
    async updatemodal(sectionId) {
      this.sectionName = this.sections.find(section => section.id === sectionId).name;
      this.sectionId = sectionId;

    },
    async downloadResource() {
      this.isWaiting = true
      const res = await fetch(`${API_BASE_URL}/download-csv`)
      const data = await res.json()
      console.log("inside download resource", data)
      if (res.ok) {
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`${API_BASE_URL}/get-csv/${taskId}`)
          if (csv_res.ok) {
            this.isWaiting = false
            clearInterval(intv)
            window.location.href = `${API_BASE_URL}/get-csv/${taskId}`
          }
        }, 1000)
      }
    },


    async submit_section_update() {
      const sectionData = {
        name: this.sectionName
      };
      try {
        const response = await fetch(`${API_BASE_URL}/section/${this.sectionId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify(sectionData)
        });

        if (!response.ok) {
          throw new Error('Unable to update section');
        }
        const data = await response.json();
        console.log('Section updated successfully', data);
        $('#exampleModal').modal('hide'); // Requires jQuery or bootstrap instance in scope
        this.sectionName = '';
        this.getSections();


      } catch (error) {
        console.error('Error updating section:', error);
      }
    },

    async addSection() {
      const sectionData = {
        name: this.sectionName
      };
      try {
        const response = await fetch(`${API_BASE_URL}/add-section`, {
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
        const btnn = document.getElementById('close-add-section');
        if(btnn) btnn.click();

        this.sectionName = '';
        this.getSections();
      } catch (error) {
        console.error('Error adding section:', error);
      }
    },
    confirmDelete(sectionId) {
      this.sectionToDelete = sectionId;
      if (confirm('Are you sure you want to delete this section?')) {
        this.deleteSection();

      }

    },
    async deleteSection() {
      try {
        //get_full_book
        const response = await fetch(`${API_BASE_URL}/delete-section/${this.sectionToDelete}`, {
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
        this.getSections(); // Refresh the section list
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    async getSections() {
      try {
        const response = await fetch(`${API_BASE_URL}/sections`, {
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
    this.getSections();
  }
};
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 2rem;
  background: var(--bg-gradient);
}

/* Glass Card for Sections */
.section-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.section-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.section-link {
    transition: color 0.2s;
}

.section-link:hover {
    color: #4f46e5 !important;
}

/* Decorative Circle */
.decorative-circle {
    position: absolute;
    bottom: -20px;
    right: -20px;
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(147, 51, 234, 0.1));
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
}

/* Modal Styling */
.glass-modal .modal-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.custom-input {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem;
}

.custom-input:focus {
  background: #fff;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
</style>
