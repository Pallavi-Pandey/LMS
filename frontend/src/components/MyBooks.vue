<template>
  <div class="dashboard-container">
    <div class="row mb-5">
      <div class="col-md-12 text-center">
        <h1 class="display-5 fw-bold text-white mb-2">My Bookshelf</h1>
        <p class="text-white-50">Track your current reads and history</p>
        
        <div class="search-wrapper mx-auto mt-4">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search your books..." 
            class="form-control form-control-lg search-input glass-input"
          >
        </div>
      </div>
    </div>

    <div class="glass-panel p-4">
      <ul class="nav nav-pills mb-4 nav-justified glass-tabs" id="pills-tab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active rounded-pill fw-bold" id="current-tab" data-bs-toggle="pill" data-bs-target="#current" type="button" role="tab">
            <i class="bi bi-book-half me-2"></i>Current Reads
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link rounded-pill fw-bold" id="completed-tab" data-bs-toggle="pill" data-bs-target="#completed" type="button" role="tab">
            <i class="bi bi-check-circle me-2"></i>Completed
          </button>
        </li>
      </ul>
      
      <div class="tab-content" id="pills-tabContent">
        <!-- Current/Active Books -->
        <div class="tab-pane fade show active" id="current" role="tabpanel">
           <div v-if="filterBooksBySearch(activeBooks, searchQuery).length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div v-for="book in filterBooksBySearch(activeBooks, searchQuery)" :key="book.id" class="col">
                <div class="card h-100 border-0 shadow-sm glass-card book-card">
                  <div class="row g-0 h-100">
                    <div class="col-4 overflow-hidden rounded-start">
                       <img :src="book.image || 'https://via.placeholder.com/150x200?text=No+Cover'" class="w-100 h-100 object-fit-cover" 
                       alt="Book Cover" @error="$event.target.src='https://via.placeholder.com/150x200?text=No+Cover'">
                    </div>
                    <div class="col-8">
                       <div class="card-body d-flex flex-column h-100 py-3">
                          <h6 class="card-subtitle text-primary mb-1 small fw-bold">{{ book.section_name }}</h6>
                          <h5 class="card-title fw-bold text-truncate" :title="book.book_title">{{ book.book_title }}</h5>
                          <p class="card-text small text-muted mb-2">{{ book.author_name }}</p>
                          
                          <div class="mt-auto">
                              <span class="badge bg-secondary mb-2" v-if="book.status === 'requested'">Requested</span>
                              <div v-if="book.status === 'approved'">
                                  <small class="d-block text-muted mb-2">Due: {{ make_date_readable(add_7_days(book.issue_date)) }}</small>
                                  <div class="d-grid gap-2">
                                    <button class="btn btn-primary btn-sm rounded-pill" type="button" data-bs-toggle="modal"
                                       data-bs-target="#ViewFullBook" @click="get_full_book(book.book_id,book.book_title)">
                                      Read
                                    </button>
                                     <button class="btn btn-outline-primary btn-sm rounded-pill" type="button" data-bs-toggle="modal"
                                      data-bs-target="#reviewBookModal" @click="set_return_book_id(book.book_id)">
                                      Return
                                    </button>
                                  </div>
                              </div>
                              <button v-if="book.status === 'requested'" @click="returnBook(book.book_id)" class="btn btn-outline-danger btn-sm w-100 rounded-pill">
                                Cancel Request
                              </button>
                          </div>
                       </div>
                    </div>
                  </div>
                </div>
            </div>
           </div>
           <div v-else class="text-center py-5 text-muted">
              <i class="bi bi-journal-x fs-1 mb-3 d-block"></i>
              No active books found.
           </div>
        </div>

        <!-- Completed/Returned Books -->
        <div class="tab-pane fade" id="completed" role="tabpanel">
           <div v-if="filterBooksBySearch(completedBooks, searchQuery).length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
              <div v-for="book in filterBooksBySearch(completedBooks, searchQuery)" :key="book.id" class="col">
                  <div class="card h-100 border-0 shadow-sm glass-card opacity-75">
                      <div class="card-body">
                          <h5 class="card-title text-truncate">{{ book.book_title }}</h5>
                          <h6 class="card-subtitle mb-2 text-muted">{{ book.author_name }}</h6>
                          <p class="text-success small mb-0"><i class="bi bi-check-all me-1"></i>Returned on {{ make_date_readable(book.return_date) }}</p>
                      </div>
                  </div>
              </div>
           </div>
           <div v-else class="text-center py-5 text-muted">
              No history found.
           </div>
        </div>
      </div>
    </div>
    
     <!-- Review Modal (Copied/Styled from UserDashboard for consistency if needed or kept simple here, but using glass) -->
    <div class="modal fade glass-modal" id="reviewBookModal" tabindex="-1" aria-labelledby="reviewBookModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary" id="reviewBookModalLabel">Return & Review</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent>
                        <div class="mb-3">
                            <label for="rating" class="form-label">Rating</label>
                            <select class="form-select custom-input" id="rating" v-model.trim="rating" required>
                                <option value="" disabled selected>Select a rating</option>
                                <option value="5">⭐⭐⭐⭐⭐ (Excellent)</option>
                                <option value="4">⭐⭐⭐⭐ (Good)</option>
                                <option value="3">⭐⭐⭐ (Average)</option>
                                <option value="2">⭐⭐ (Poor)</option>
                                <option value="1">⭐ (Terrible)</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="feedback" class="form-label">Feedback</label>
                            <textarea class="form-control custom-input" id="feedback" v-model.trim="feedback" rows="3" placeholder="How was the book?" required></textarea>
                        </div>
                        <div class="d-grid">
                            <button type="button" @click="add_feedback(rating, feedback, return_book_id)" class="btn btn-premium">Submit & Return</button>
                        </div>
                    </form>
                </div>
                <!-- Logic button -->
                 <button type="button" class="d-none" data-bs-dismiss="modal" id="closebookmodal"></button>
            </div>
        </div>
    </div>


     <!-- View Full Book Modal -->
    <div class="modal fade glass-modal" id="ViewFullBook" tabindex="-1" aria-labelledby="ViewFullBookLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content glass-panel border-0">
          <div class="modal-header border-bottom-0">
            <h1 class="modal-title fs-5 fw-bold text-primary" id="ViewFullBookLabel">{{ full_book_modal_name }}</h1>
            <div class="ms-auto d-flex gap-2">
              <button class="btn btn-outline-primary btn-sm" @click="download_book_as_pdf(full_book_modal_content,full_book_modal_name)">
                <i class="bi bi-download"></i> Download PDF
              </button>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
          </div>
          <div class="modal-body text-dark">
            <div class="p-3 bg-white rounded shadow-sm">
              {{ full_book_modal_content }}
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import API_BASE_URL from "../config";
import jsPDF from 'jspdf';
// Note: Some methods for review/read might be duplicated logic from UserDashboard. 
// Ideally would be a mixin or store, but keeping local for now.

export default {
  data() {
    return {
      books: [],
      searchQuery: "",
      rating: "",
      feedback: "",
      return_book_id: null,
      full_book_modal_content: '',
      full_book_modal_name: ''
    };
  },
  created() {
    this.fetchBooks();
  },
  computed: {
      activeBooks() {
          return this.books.filter(book => book.status === 'approved' || book.status === 'requested');
      },
      completedBooks() {
          return this.books.filter(book => book.status === 'returned');
      }
  },
  methods: {
    add_7_days(date) {
      if(!date) return new Date();
      return new Date(date).setDate(new Date(date).getDate() + 7);
    },
    make_date_readable(date) {
       if(!date) return 'N/A';
      return new Date(date).toLocaleDateString();
    },
    set_return_book_id(id) {
        this.return_book_id = id;
    },
    async get_full_book(bookId,book_name) {
      // fetch book content
      try {
        const response = await fetch(`${API_BASE_URL}/full-book/${bookId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          }

        });
        if (!response.ok) {
          throw new Error('Unable to fetch book');
        }
        const data = await response.json();
        console.log(data);
        this.full_book_modal_content = data.content;
        this.full_book_modal_name=book_name;
      } catch (error) {
        console.error('Error fetching book:', error);
      }
    },
    download_book_as_pdf(content,bookname) {
        console.log(content);
        var pdf = new jsPDF();
        var textLines = pdf.splitTextToSize(content, pdf.internal.pageSize.width - 20); 
        var y = 10;
        for (var i = 0; i < textLines.length; i++) {
            if (y + 10 > pdf.internal.pageSize.height) { 
                pdf.addPage();
                y = 10;
            }
            pdf.text(10, y, textLines[i]);
            y += 10;
        }
        pdf.save(bookname+".pdf");
    },

    add_feedback(rating, feedback, bookId) {
         fetch(`${API_BASE_URL}/add-feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('auth-token')
        },
        body: JSON.stringify({ "rating": rating, "feedback": feedback, "book_id": bookId })
      })
        .then(res => res.json())
        .then(data => {
          console.log('Feedback added successfully', data);
          alert('Feedback added and book returned successfully');
        
          document.getElementById('closebookmodal')?.click() || $('#reviewBookModal').modal('hide');
          this.rating="";
          this.feedback="";
          this.returnBook(bookId);  // Actually return the book after feedback
        })
        .catch(error => {
          console.error('Error adding feedback:', error);
        });
    },

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
.dashboard-container {
  min-height: 100vh;
  padding: 2rem;
  background: var(--bg-gradient);
}
.glass-panel {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.search-wrapper {
  max-width: 600px;
}

.glass-input {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50px;
  padding-left: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.glass-tabs .nav-link {
    color: #6c757d;
    background: rgba(255,255,255,0.5);
    margin: 0 0.5rem;
    transition: all 0.3s ease;
}

.glass-tabs .nav-link.active {
    background: #4f46e5;
    color: white;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
}

.book-card {
  transition: transform 0.3s ease;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

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
</style>
