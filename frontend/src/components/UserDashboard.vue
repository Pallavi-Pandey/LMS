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
            <button type="button" class="btn btn-primary">Rent</button>
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
                const response = await fetch(`http://127.0.0.1:5000/sections`);
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
  },
};
</script>
