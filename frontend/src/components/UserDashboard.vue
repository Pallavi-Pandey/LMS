<template>
  <div>
    <h1>Welcome to the Library</h1>
    <div v-for="section in sections" :key="section.id">
      <h2>{{ section.name }}</h2>
      <div class="card-group">
        <div v-for="book in section.books" :key="book.id" class="card">
          <img :src="book.image" class="card-img-top" alt="Book Cover">
          <div class="card-body">
            <h5 class="card-title">{{ book.name }}</h5>
            <p class="card-text">{{ book.content }}</p>
            <p class="card-text">{{ book.author }}</p>
            <button @click="rent_book(book.id)" class="btn btn-primary">Rent</button>
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
      sections: [],
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        // Fetch section and books data from the backend API
        const response = await fetch(`http://127.0.0.1:5000/sections`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          }
        });
       
        if (!response.ok) {
          throw new Error("Unable to fetch section");
        }
        const data = await response.json();
        console.log(data);
        this.sections = data;
        this.books = data.books;
      } catch (error) {
        console.error("Error fetching section:", error);
      }
    },
    async rent_book(book_id) {
      try {
        const response = await fetch('http://127.0.0.1:5000/rent-book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({"book_id": book_id })
        });
        if (!response.ok) {
          throw new Error('Unable to rent book');
        }
        const data = await response.json();
        console.log('Book rented successfully', data);
        alert('Admin will approve your request soon.');

      } catch (error) {
        console.error('Error renting book:', error);
      }
    },
  },
};
</script>
