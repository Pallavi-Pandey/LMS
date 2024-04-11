<template>

  <div class="container">
    <h1>My Books</h1>
    <div class="row">
      <div class="col-md-12">
        <h2>My Current Books</h2>
        <!-- Search bar for current books -->
        <label for="searchCurrent">Search</label>
        <input type="search" v-model="searchCurrent" placeholder="Search Current Books">
        <table class="table">

          <thead>
            <tr>
              <th scope="col">Book ID</th>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Filtered current books based on search query -->
            <tr v-for="book in filteredCurrentBooks" :key="book.book_id">

              <td>{{ book.book_id }}</td>
              <td>{{ book.book_title }}</td>
              <td>{{ book.author_name }}</td>
              <td>{{ book.section_name }}</td>
              <td>{{ book.status }}</td>
              <td>
                <button v-if="book.status === 'approved'" type="button" class="btn btn-danger" @click="returnBook(book.book_id)">Return</button>
              </td>

            </tr>
          </tbody>
        </table>
        <h2> Requested Books</h2>
        <!-- Search bar for requested books -->
        <label for="searchRequested">Search</label>
        <input type="search" v-model="searchRequested" placeholder="Search Requested Books">
        <table class="table">

          <thead>
            <tr>
              <th scope="col">Book ID</th>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <!-- Filtered requested books based on search query -->
            <tr v-for="book in filteredRequestedBooks" :key="book.book_id">

              <td>{{ book.book_id }}</td>
              <td>{{ book.book_title }}</td>
              <td>{{ book.author_name }}</td>
              <td>{{ book.section_name }}</td>
              <td>{{ book.status }}</td>

            </tr>
          </tbody>
        </table>
        
        <h2>My Completed Books</h2>
        <!-- Search bar for completed books -->
        <label for="searchCompleted">Search</label>
        <input type="search" v-model="searchCompleted" placeholder="Search Completed Books">
        <table class="table">

          <thead>
            <tr>
              <th scope="col">Book ID</th>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <!-- Filtered completed books based on search query -->
            <tr v-for="book in filteredCompletedBooks" :key="book.book_id">

              <td>{{ book.book_id }}</td>
              <td>{{ book.book_title }}</td>
              <td>{{ book.author_name }}</td>
              <td>{{ book.section_name }}</td>
              <td>{{ book.status }}</td>

            </tr>
          </tbody>
        </table>

      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "MyBooks",
  data() {
    return {
      books: [],
      searchCurrent: '',
      searchRequested: '',
      searchCompleted: ''
    };
  },
  created() {
    this.fetchBooks();
  },
  computed: {
    filteredCurrentBooks() {
      return this.filterBooksBySearch(this.books.filter(book => book.status === 'approved'), this.searchCurrent);
    },
    filteredRequestedBooks() {
      return this.filterBooksBySearch(this.books.filter(book => book.status === 'requested'), this.searchRequested);
    },
    filteredCompletedBooks() {
      return this.filterBooksBySearch(this.books.filter(book => book.status === 'returned'), this.searchCompleted);
    }
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/my-books`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        });
        if (!response.ok) {
          throw new Error("Unable to fetch books");
        }
        const data = await response.json();
        console.log(data);
        this.books = data;
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    filterBooksBySearch(books, searchQuery) {
      if (!searchQuery) return books;
      return books.filter(book => 
        book.book_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.author_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.section_name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    },
    async returnBook(book_id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/return-book`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: JSON.stringify({ book_id }),
        });
        if (!response.ok) {
          throw new Error("Unable to return book");
        }
        this.fetchBooks();
      } catch (error) {
        console.error("Error returning book:", error);
      }
    }, 
  },
};

</script>
