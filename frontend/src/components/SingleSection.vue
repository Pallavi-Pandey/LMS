<template>
  <div class="dashboard-container">
    <div class="glass-panel p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-light pb-3">
        <div>
           <button class="btn btn-sm btn-light text-primary mb-2 rounded-pill px-3 shadow-sm" @click="$router.push('/librarian-dashboard')">
              <i class="bi bi-arrow-left me-1"></i> Back to Dashboard
          </button>
          <h2 class="text-primary fw-bold m-0" v-if="section">{{ section }}</h2>
        </div>
       
        <button type="button" class="btn btn-premium rounded-pill px-4 shadow-sm" data-bs-toggle="modal" data-bs-target="#addBookModal">
          <i class="bi bi-plus-lg me-2"></i>Add New Book
        </button>
      </div>

      <div v-if="section">
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">
          <div v-for="book in books" :key="book.id" class="col">
            <div class="card h-100 border-0 shadow-sm card-hover glass-card book-card">
              <div class="card-img-wrapper position-relative" style="height: 200px; overflow: hidden;">
                <img :src="book.image || 'https://via.placeholder.com/300x400?text=No+Cover'" class="card-img-top w-100 h-100 object-fit-cover" alt="Book Cover" @error="$event.target.src='https://via.placeholder.com/300x400?text=No+Cover'">
                <div class="card-overlay">
                    <button type="button" class="btn btn-light btn-sm rounded-pill px-3 mb-2" data-bs-toggle="modal"
                      data-bs-target="#ViewBook" @click="setmodalcontent(book.content,book.name,book.id)">
                      <i class="bi bi-eye me-1"></i> Preview
                    </button>
                    <button type="button" class="btn btn-primary btn-sm rounded-pill px-3" data-bs-toggle="modal"
                      data-bs-target="#ViewFullBook" @click="get_full_book(book.id,book.name)">
                      <i class="bi bi-book me-1"></i> Read Full
                    </button>
                </div>
              </div>

              <div class="card-body d-flex flex-column p-3">
                <h5 class="card-title fw-bold text-truncate mb-1" :title="book.name">{{ book.name }}</h5>
                <h6 class="card-subtitle mb-3 text-muted small">{{ book.author }}</h6>
                
                <div class="mt-auto d-grid gap-2">
                  <button type="button" class="btn btn-outline-primary btn-sm rounded-pill" data-bs-toggle="modal"
                    data-bs-target="#exampleModal" @click="updatemodal(book.id)">
                    Edit Details
                  </button>
                  <button type="button" class="btn btn-outline-danger btn-sm rounded-pill" @click="confirmDelete(book.id)">
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>

    <!-- Modals (with glass styling) -->
    <!-- View Sample Modal -->
    <div class="modal fade glass-modal" id="ViewBook" tabindex="-1" aria-labelledby="ViewBook" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary">Sample: {{ modal_title }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4 bg-white rounded mx-3 mb-3 shadow-sm">
                    {{ modal_content }}
                </div>
                <div class="modal-footer border-top-0">
                    <button type="button" class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- View Full Book Modal -->
    <div class="modal fade glass-modal" id="ViewFullBook" tabindex="-1" aria-labelledby="ViewFullBook" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary">{{ full_book_view_book_name }}</h1>
                    <div class="ms-auto d-flex gap-2 align-items-center">
                        <button type="button" class="btn btn-outline-primary btn-sm rounded-pill" @click="download_book_as_pdf(full_book_modal_content,full_book_view_book_name)">
                            <i class="bi bi-download me-1"></i> Download
                        </button>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                </div>
                <div class="modal-body p-4 bg-white rounded mx-3 mb-3 shadow-sm">
                    {{ full_book_modal_content }}
                </div>
            </div>
        </div>
    </div>

    <!-- Update Book Modal -->
    <div class="modal fade glass-modal" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary">Edit Book</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submit_book_update">
                        <div class="mb-3">
                            <label class="form-label">Book Name</label>
                            <input type="text" class="form-control custom-input" v-model.trim="bookName" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Author</label>
                            <input type="text" class="form-control custom-input" v-model.trim="author" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Full Content</label>
                            <textarea class="form-control custom-input" v-model.trim="full_book_modal_content" rows="4" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Cover Image URL</label>
                            <input type="text" class="form-control custom-input" v-model.trim="image" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-premium rounded-pill">Update Book</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Book Modal -->
    <div class="modal fade glass-modal" id="addBookModal" tabindex="-1" aria-labelledby="addBookModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-panel border-0">
                <div class="modal-header border-bottom-0">
                    <h1 class="modal-title fs-5 fw-bold text-primary">Add New Book</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addBook">
                        <div class="mb-3">
                            <label class="form-label">Book Name</label>
                            <input type="text" class="form-control custom-input" v-model.trim="bookName" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Author</label>
                            <input type="text" class="form-control custom-input" v-model.trim="author" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Full Content</label>
                            <textarea class="form-control custom-input" v-model.trim="content" rows="4" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Cover Image URL</label>
                            <input type="text" class="form-control custom-input" v-model.trim="image" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-premium rounded-pill">Add Book</button>
                        </div>
                    </form>
                </div>
                 <!-- Logic button -->
                 <button type="button" class="d-none" data-bs-dismiss="modal" id="closebookmodal"></button>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
// Logic remains mostly the same, ensuring API_BASE_URL is imported and used
import API_BASE_URL from "../config";
import jsPDF from 'jspdf';

export default {

    data() {
        return {
            sectionId: this.$route.params.id,
            section: null, // Init as null to show loader
            books: [],
            bookName: '',
            content: '',
            author: '',
            image: '',
            modal_content: '',
            modal_title:'',
            modal_book_id:"",
            full_book_view_book_name:"",
            full_book_view_book_id:"",
            full_book_modal_content: '',
            bookToDelete: null,
            bookId: null,
            contentfull_book_modal_content: '' // This variable name in original was weird but keeping logic consistent

        };
    },
    created() {
        this.fetchSection();
    },
    methods: {
        download_book_as_pdf(content,bookname) {
            console.log(content);
            var pdf = new jsPDF();
            var textLines = pdf.splitTextToSize(content, pdf.internal.pageSize.width - 20); // Adjust width as needed
            var y = 10;
            for (var i = 0; i < textLines.length; i++) {
                if (y + 10 > pdf.internal.pageSize.height) { // Check if new page needed
                    pdf.addPage();
                    y = 10;
                }
                pdf.text(10, y, textLines[i]);
                y += 10;
            }
            pdf.save(bookname+".pdf");
        },
        
        async get_full_book(bookId,book_name) {
            // fetch book content
            this.full_book_view_book_name=book_name;
            this.full_book_view_book_id=bookId;
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
            } catch (error) {
                console.error('Error fetching book:', error);
            }


        },
        setmodalcontent(content,title,book_id) {
            this.modal_content = content;
            this.modal_title = title;
            this.modal_book_id = book_id;
        },
        async updatemodal(bookId) {
            await  this.get_full_book(bookId);
            console.log(this.full_book_modal_content);
            this.modal_name = this.books.find(book => book.id === bookId).name;
            this.modal_book_id=bookId;
            console.log ("bbbbbbbbbbbbbb")
            this.bookId = bookId;
            this.bookName = this.books.find(book => book.id === bookId).name;
            // Original code had this check/assignment potentially buggy or redundant, ensuring consistency
            this.full_book_modal_content = this.books.find(book => book.id === bookId).full_book_modal_content || this.full_book_modal_content; 
            
            this.author = this.books.find(book => book.id === bookId).author;
            this.image = this.books.find(book => book.id === bookId).image;
        },
        async submit_book_update() {
           
            const bookData = {
                name: this.bookName,
                // Using full_book_modal_content as it is bound to the textarea in update modal
                full_content: this.full_book_modal_content, 
                author: this.author,
                image: this.image,
            };
            console.log(bookData);
            try {
                const response = await fetch(`${API_BASE_URL}/book/` + this.bookId, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    },
                    body: JSON.stringify(bookData)
                });
                if (!response.ok) {
                    throw new Error('Unable to update book');
                }
                const data = await response.json();
                console.log('Book updated succeUpdatessfully', data);
                $('#exampleModal').modal('hide');
                this.bookName = '';
                this.content = '';
                this.author = '';
                this.image = '';
                this.fetchSection();
            } catch (error) {
                console.error('Error updating book:', error);
            }
        },
        confirmDelete(bookId) {
            this.bookToDelete = bookId;
            if (confirm('Are you sure you want to delete this book?')) {
                this.deletebook();

            }
        },

        async deletebook() {
            try {
                const response = await fetch(`${API_BASE_URL}/book/${this.bookToDelete}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    }
                });
                if (!response.ok) {
                    throw new Error('Unable to delete book');
                }
                const data = await response.json();
                console.log('book deleted successfully', data);
                this.fetchSection();
            } catch (error) {
                console.error('Error deleting section:', error);
            }
        },

        async fetchSection() {
            try {
                // Fetch section and books data from the backend API
                const response = await fetch(`${API_BASE_URL}/section/${this.sectionId}`);
                if (!response.ok) {
                    throw new Error("Unable to fetch section");
                }
                const data = await response.json();
                console.log(data);

                this.section = data.name;
                // filter the delted books

                this.books = data.books.filter(book => book.is_deleted === false);
                console.log(this.books);

            } catch (error) {
                console.error("Error fetching section:", error);
            }
        },
        async addBook() {
            const bookData = {
                name: this.bookName,
                content: this.content,
                author: this.author,
                image: this.image,
                section_id: this.sectionId

            };
            try {
                const response = await fetch(`${API_BASE_URL}/add-book`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    },
                    body: JSON.stringify(bookData)
                });
                if (!response.ok) {
                    throw new Error('Unable to add section');
                }
                const data = await response.json();
                console.log('Section added successfully', data);

                this.bookName = '';
                this.content = '';
                this.author = '';
                this.image = '';
                this.fetchSection();
                const closebtn = document.getElementById('closebookmodal');
                if(closebtn) closebtn.click();
            } catch (error) {
                console.error('Error adding section:', error);
            }
        },
    }
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

.book-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  border-radius: 12px;
  background: #fff;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.card-img-wrapper:hover .card-overlay {
    opacity: 1;
}

.card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
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