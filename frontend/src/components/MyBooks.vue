<template>
  <div class="page-container">
    <div class="container">
      <h1>My Books</h1>
      <hr>
      <div class="row">
        <div class="col-md-12">
          <div>
            <h2>My Current Books</h2>
            <div class="search-bar">
              <input type="search" v-model="searchCurrent" placeholder="Search Current Books" class="form-control">
            </div>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Book ID</th>
                    <th>Book-Title</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in filteredCurrentBooks" :key="book.book_id">
                    <td>{{ book.book_id }}</td>
                    <td>{{ book.book_title }}</td>
                    <td>{{ book.author_name }}</td>
                    <td>{{ book.section_name }}</td>
                    <td>{{ book.status }}</td>
                    <td>
                      <button v-if="book.status === 'approved'" type="button" class="btn btn-danger"
                        @click="returnBook(book.book_id)">Return</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h2>Requested Books</h2>
            <div class="search-bar">
              <input type="search" v-model="searchRequested" placeholder="Search Requested Books" class="form-control">
            </div>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Book ID</th>
                    <th>Book-Title</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in filteredRequestedBooks" :key="book.book_id">
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

          <div>
            <h2>My Completed Books</h2>
            <div class="search-bar">
              <input type="search" v-model="searchCompleted" placeholder="Search Completed Books" class="form-control">
            </div>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Book ID</th>
                    <th>Book-Title</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
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
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE_URL from "../config";
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
        const response = await fetch(`${API_BASE_URL}/my-books`, {
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
        const response = await fetch(`${API_BASE_URL}/return-book`, {
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

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 5%;
  background-color: #cfd8e0;
}

.search-bar {
  margin-bottom: 10px;

}

.container {
  color: #553761;
  padding: 20px;
}

h1 {
  text-align: center;
}

.search-bar {
  margin-bottom: 10px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.table th,
.table td {
  padding: 8px;
  text-align: left;
}

.table th {
  background-color: #f8f9fa;
}

.btn {
  padding: 6px 12px;
  margin: 2px;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}
</style>
