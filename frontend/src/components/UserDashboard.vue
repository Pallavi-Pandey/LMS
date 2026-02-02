<template>
  <div class="dashboard-container">
    <div class="row mb-4">
      <div class="col-md-12 text-center">
        <h1 class="display-5 fw-bold text-white mb-2">Welcome to Your Library</h1>
        <p class="text-white-50 fs-5 mb-4">{{ user_email }}</p>
        
        <div class="search-wrapper mx-auto">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search books, authors, or sections..." 
            class="form-control form-control-lg search-input glass-input"
          >
        </div>
      </div>
    </div>

    <div v-for="section in filteredSections" :key="section.id" class="mb-5 section-wrapper">
      <div class="d-flex align-items-center mb-3">
        <h2 class="section-title text-white m-0">{{ section.name }}</h2>
        <span class="badge bg-white text-primary ms-3 shadow-sm">{{ section.books.length }} Books</span>
      </div>
      
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">
        <div v-for="book in section.books" :key="book.id" class="col">
          <div class="card h-100 border-0 shadow-sm card-hover glass-panel book-card">
            <div class="card-img-wrapper">
              <img :src="book.image || 'https://via.placeholder.com/300x400?text=No+Cover'" class="card-img-top" alt="Book Cover" @error="$event.target.src='https://via.placeholder.com/300x400?text=No+Cover'">
              <div class="card-overlay" v-if="book.status === 'approved'">
                <span class="badge bg-success mb-2">Rented</span>
                <small class="text-white">Due: {{ get_remaining_days(book.requested_date) }} days left</small>
              </div>
            </div>
            
            <div class="card-body d-flex flex-column">
              <h5 class="card-title fw-bold text-truncate" :title="book.name">{{ book.name }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
              <p class="card-text small text-muted flex-grow-1 line-clamp-3">{{ book.content }}</p>
              
              <div class="mt-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="status-indicator" :class="statusClass(book.status)">
                    {{ book.status }}
                  </span>
                </div>

                <div class="d-grid gap-2">
                  <button v-if="book.status === 'available'" @click="rent_book(book.id)"
                    class="btn btn-premium btn-sm">Rent Now</button>
                    
                  <button v-if="book.status === 'requested'" @click="revoke_book(book.id)"
                    class="btn btn-outline-danger btn-sm">Cancel Request</button>

                  <div v-if="book.status === 'approved'" class="d-grid gap-2">
                    <button type="button" class="btn btn-outline-primary btn-sm" data-bs-toggle="modal"
                      data-bs-target="#reviewBookModal" @click="set_review_modal_data(book.id)">
                      Return & Review
                    </button>
                    <button type="button" class="btn btn-light btn-sm text-primary" data-bs-toggle="modal"
                      data-bs-target="#ViewFullBook" @click="get_full_book(book.id,book.name)">
                      Read Book
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div class="modal fade glass-modal" id="reviewBookModal" tabindex="-1" aria-labelledby="reviewBookModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary" id="reviewBookModalLabel">Review & Return</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addBook">
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
                            <textarea class="form-control custom-input" id="feedback" v-model.trim="feedback" rows="3" placeholder="Share your thoughts..." required></textarea>
                        </div>
                        <div class="d-grid">
                          <button type="button" @click="add_feedback(rating,feedback,review_modal_book_id)" class="btn btn-premium">Submit & Return</button>
                        </div>
                    </form>
                </div>
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

export default {
  data() {
    return {
      sections: [],
      user_email: localStorage.getItem('email'),
      searchQuery: '',
      full_book_modal_content: '',
      full_book_modal_name: '',
      books_rented: 0,
      review_modal_book_id: null,
      rating:"",
      feedback:""
    };
  },
  created() {
    this.fetchSections();
  },
  computed: {
    filteredSections() {
      return this.sections.map(section => ({
        ...section,
        books: section.books.filter(book =>
          book.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          book.author.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          book.content.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          book.status.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      })).filter(section => section.books.length > 0);
    },
  },
  methods: {
    statusClass(status) {
      const classes = {
        'available': 'text-success bg-success-subtle px-2 py-1 rounded',
        'requested': 'text-warning bg-warning-subtle px-2 py-1 rounded',
        'approved': 'text-primary bg-primary-subtle px-2 py-1 rounded',
        'returned': 'text-secondary bg-secondary-subtle px-2 py-1 rounded'
      };
      return classes[status] || '';
    },
    add_feedback(rating,feedback,bookId){
      // ... existing code ...
      console.log(rating,feedback,bookId)
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
          alert('Feedback added successfully');
          document.getElementById('closebookmodal')?.click() || $('#reviewBookModal').modal('hide');
          this.rating="";
          this.feedback="";
          this.return_book(bookId);
           
        })
        .catch(error => {
          console.error('Error adding feedback:', error);
        });
    },

    set_review_modal_data(bookId){
      this.review_modal_book_id=bookId;
    },
    download_book_as_pdf(content,bookname) {
    // ... existing code ...
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
    add_7_days(date) {
      return new Date(date).setDate(new Date(date).getDate() + 7);
    },
    convert_to_date_and_time(date) {
      return new Date(date).toDateString();

    },
    get_remaining_days(date) {
      const due_date = new Date(date).setDate(new Date(date).getDate() + 7);
      const remaining_days = Math.ceil((due_date - new Date().getTime()) / (1000 * 60 * 60 * 24));
      return remaining_days;
    },


    get_book_name_by_id(bookId){
      // ... existing code ...
      return this.sections.map(section => section.books.filter(book => book.id == bookId)[0]?.name)[0];
    },
    

    async get_full_book(bookId,book_name) {
      // ... existing code ...
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
    async return_book(book_id) {
      // ... existing code ...
      try {
        const response = await fetch(`${API_BASE_URL}/return-book`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({ "book_id": book_id })
        });
        if (!response.ok) {
          throw new Error('Unable to return book');
        }
        const data = await response.json();
        console.log('Book returned successfully', data);
        alert('Book returned successfully');
        this.fetchSections();
      } catch (error) {
        console.error('Error returning book:', error);
      }
    },

    async fetchSections() {
      // ... existing code ...
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

    async get_books_rented() {
      // ... existing code ...
      try {
        const response = await fetch(`${API_BASE_URL}/books-rented`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          }
        });
        if (!response.ok) {
          throw new Error('Unable to fetch rented books');
        }
        const data = await response.json();
        console.log('Books rented:', data);
        this.books_rented = data.books_rented;
      } catch (error) {
        console.error('Error fetching rented books:', error);
      }
    },

    async rent_book(book_id) {
      // ... existing code ...
      await this.get_books_rented();
      if (this.books_rented >= 5) {
        alert('OOPS !!! You can rent only 5 books at a time.');
        return;
      }

      if (!confirm('Taking you to payment gateway, do you want to continue?')) {
        return;
      }
      if (!confirm('pay 100 to rent the book?')) {
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/rent-book`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({ "book_id": book_id })
        });
        if (response.status === 223) {
          alert('Aaahhhh !!! You can rent only 5 books at a time.');
          return;
        }
        if (!response.ok) {
          throw new Error('Unable to rent book');
        }
        const data = await response.json();
        console.log('Book rented successfully', data);
        alert('Admin will approve your request soon.');
        this.fetchSections();

      }

      catch (error) {
        console.error('Error renting book:', error);
      }
    },
    async revoke_book(book_id) {
      // ... existing code ...
      try {
        const response = await fetch(`${API_BASE_URL}/revoke-book`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({ "book_id": book_id })
        });
        if (!response.ok) {
          throw new Error('Unable to revoke book');
        }
        const data = await response.json();
        console.log('Book revoked successfully', data);
        alert('Revoke successful');
        this.fetchSections();

      } catch (error) {
        console.error('Error revoking book:', error);
      }
    },
    make_date_readable(date) {
      return new Date(date).toDateString();
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

.glass-input:focus {
  background: #ffffff;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.section-title {
  font-weight: 700;
  letter-spacing: -0.5px;
}

.book-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1) !important;
}

.card-img-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.book-card:hover .card-img-top {
  transform: scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-img-wrapper:hover .card-overlay,
.book-card:hover .card-overlay {
  opacity: 1;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-indicator {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
