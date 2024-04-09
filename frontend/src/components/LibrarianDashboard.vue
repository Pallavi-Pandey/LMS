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
            Section Management
          </div>
          <div class="card-body">
            <p>Show all sections here</p>
            <ul>
              <li v-for="section in sections" :key="section.id">
                {{ section.name }} <button>Update</button> <button>delete</button>
              </li>
            </ul>
          </div>
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSectionModal">
            Add Section
          </button>
        </div>
      </div>
    </div>

    <!-- Add Section Modal -->
    <div class="modal fade" id="addSectionModal" tabindex="-1" aria-labelledby="addSectionModalLabel" aria-hidden="true">
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
                <input type="text" class="form-control" id="sectionName"  v-model.trim="sectionName" required>
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
  </div>
</template>

<script>
import { onMounted } from 'vue';

export default {
  data() {
    return {
      sectionName: '',
      sections: []
    };
  },
  methods: {
    async addSection() {
      const sectionData = {
        name: this.sectionName
      };
     await fetch('http://127.0.0.1:5000/add-section', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('auth-token')
        },
        body: JSON.stringify(sectionData)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Unable to add section');
        }
        return response.json();
      })
      .then(data => {
        console.log('Section added successfully', data);
        $('#addSectionModal').modal('hide');
        this.sectionName = '';
      })
      .catch(error => {
        console.error('Error adding section:', error);
      });
    }
  },
  // to create a function to get all sections
   


  async mounted() {
    const res = await 
     fetch('http://127.0.0.1:5000/sections',{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': localStorage.getItem('auth-token')
      }
    }).then(response => {
      if (!response.ok) {
        throw new Error('Unable to fetch section');
      }
      return response.json();
    }).then(data => {
      // store the data to sections
      console.log(data);
      this.sections = data;
      console.log('Section fetched successfully', data);
    }).catch(error => {
      console.error('Error fetching section:', error);
    });
}
};


</script>

<style scoped>
/* Add scoped styles for the librarian dashboard */
.card {
  margin-bottom: 20px;
}
</style>
