<template>
    <div>
      <h1>Sections</h1>
      <div v-for="section in sections" :key="section.id">
        <h2>{{ section.name }}</h2>
        <ul>
          <li v-for="book in section.books" :key="book.id">
            {{ book.name }} by {{ book.author }}
          </li>
        </ul>
        <!-- Add Book Button -->
        <button @click="showAddBookModal(section)" class="btn btn-primary">Add Book</button>
      </div>
  
      <!-- Add Book Modal -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span @click="closeModal" class="close">&times;</span>
          <h2>Add Book</h2>
          <form @submit.prevent="addBook">
            <div class="form-group">
              <label for="bookName">Name:</label>
              <input type="text" id="bookName" v-model="newBook.name" required>
            </div>
            <div class="form-group">
              <label for="bookContent">Content:</label>
              <textarea id="bookContent" v-model="newBook.content" required></textarea>
            </div>
            <!-- Add more input fields as needed -->
            <button type="submit" class="btn btn-primary">Save</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sections: [],
        showModal: false,
        newBook: {
          name: '',
          content: '',
          // Add more properties as needed
        }
      };
    },
    created() {
      this.fetchSections();
    },
    methods: {
      async fetchSections() {
        try {
          // Fetch sections and books data from the backend API
        } catch (error) {
          console.error("Error fetching sections:", error);
        }
      },
      showAddBookModal(section) {
        this.showModal = true;
        // Additional logic to handle adding book to specific section if needed
      },
      closeModal() {
        this.showModal = false;
        // Additional logic to reset newBook object if needed
      },
      addBook() {
        // Handle adding a new book
        console.log("Adding book:", this.newBook);
        // Additional logic to send new book data to backend API
        this.closeModal();
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add scoped styles for the section page */
  h1 {
    text-align: center;
  }
  
  /* Modal styles */
  .modal {
    display: block;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>
  