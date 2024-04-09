<template>
  <div>
    <h1>List of Books</h1>
    <ul>
      <li v-for="book in books" :key="book.id">
        {{ book.name }} - {{ book.author }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: []
    };
  },
  mounted() {
    // Fetch all books from the backend API
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      axios.get('http://localhost:5000/api/books')
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    }
  }
};
</script>
