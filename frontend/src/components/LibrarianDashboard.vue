<template>
  <div class="container-fluid bg-light p-3">
    <div class="row">
      <div class="col-md-12 d-flex justify-content-between align-items-center">
        <h1>Librarian Dashboard</h1>
        <div><button @click="downloadResource">Download CSV</button><span v-if="isWaiting"> Waiting... </span></div>
      </div>
    </div>


    <!-- Section Management -->
    <div class="row mb-3">
      <div class="col-md-12">
        <div class="card mt-4">
          <div class="card-header">
            <h3>Section Management</h3>
          </div>
          <div class="card-body">
            <ul>
              <div v-for="section in sections" :key="section.id" style="margin-bottom: 10px;">
                <div class="d-flex justify-content-between align-items-center">
                  <router-link :to="`/section/${section.id}`" class="section" style="font-size:x-large ;" >{{ section.name }}</router-link>
                  <div>
                    <span class="badge bg-secondary">{{ section.books.length }}</span>
                    <span class="align-middle"> - Books</span>
                  </div>
                  <div>
                    <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#exampleModal"
                      @click="updatemodal(section.id)"  style="margin-right: 10px;">Update</button>
                    <button type="button" class="btn btn-danger" @click="confirmDelete(section.id)">Delete</button>
                  </div>
                </div>
              </div>
            </ul>
          </div>
          <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addSectionModal">
            Add Section
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Update Section</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="sectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control" id="sectionName" v-model.trim="sectionName" required>
              </div>
              <button type="submit" class="btn btn-primary" @click="submit_section_update">Update Section</button>
            </form>



          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
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
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
              id="close-add-section">Close</button>
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
      const res = await fetch('http://127.0.0.1:5000/download-csv')
      const data = await res.json()
      console.log("inside download resource", data)
      if (res.ok) {
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`http://127.0.0.1:5000/get-csv/${taskId}`)
          if (csv_res.ok) {
            this.isWaiting = false
            clearInterval(intv)
            window.location.href = `http://127.0.0.1:5000/get-csv/${taskId}`
          }
        }, 1000)
      }
    },


    async submit_section_update() {
      const sectionData = {
        name: this.sectionName
      };
      try {
        const response = await fetch(`http://127.0.0.1:5000/section/${this.sectionId}`, {
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
        $('#exampleModal').modal('hide');
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
        const btnn = document.getElementById('close-add-section');
        console.log(btnn);
        btnn.click();

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

/* change the color of buttons */
.btn-success {
  background-color: rgb(112, 68, 161);
  border-color: #08131f;
}
.btn-primary {
  background-color: rgb(94, 29, 168);
  border-color: #08131f;
}
.section-container {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }

    .section-info {
        display: flex;
        align-items: center;
    }

    .book-count {
        margin-left: 10px;
    }

    .section-actions {
        display: flex;
        align-items: center;
    }
</style>
