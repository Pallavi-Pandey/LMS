<template>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center">
            <h2 style="color: brown;">{{ section }}</h2>
            <button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#addBookModal">
                Add Book
            </button>
        </div>

        <div v-if="section">
            <h1>{{ section.name }}</h1>
            <div class="row row-cols-1 row-cols-md-3 g-3">
                <div v-for="book in books" :key="book.id" class="col">
                    <div class="card">
                        <img :src="book.image" class="card-img-top" alt="...">
                        <div class="card-body">
                            <h5 class="card-title">{{ book.name }}</h5>
                            <p class="card-text">{{ book.author }}</p>
                            <div class="d-flex justify-content-between">
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#ViewBook" @click="setmodalcontent(book.content,book.name,book.id)">
                                    View Book Sample
                                </button>
                                <button type="button" class="btn btn-success" data-bs-toggle="modal"
                                    data-bs-target="#exampleModal" @click="updatemodal(book.id)">
                                    Update
                                </button>
                            </div>
                            <hr>
                            <div class="d-flex justify-content-between">
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#ViewFullBook" @click="get_full_book(book.id,book.name)">
                                    View Full Book
                                </button>

                                <button type="button" class="btn btn-danger" @click="confirmDelete(book.id)">
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="ViewBook" tabindex="-1" aria-labelledby="ViewBook" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel"> {{ modal_title }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    {{ modal_content }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="ViewFullBook" tabindex="-1" aria-labelledby="ViewFullBook" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header" style="align-items: center;justify-content: space-between;">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Book Name: {{ full_book_view_book_name }}</h1>
                    <!-- download  book-->
                    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
                    <button type="button" class="btn btn-primary" @click="download_book_as_pdf(full_book_modal_content,full_book_view_book_name)">Download {{ full_book_view_book_name }}</button>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    {{ full_book_modal_content }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="bookName" class="form-label">Book Name</label>
                            <input type="text" class="form-control" id="bookName" v-model.trim="bookName" required>
                        </div>
                        <div class="mb-3">
                            <label for="author" class="form-label">Author</label>
                            <input type="text" class="form-control" id="author" v-model.trim="author" required>
                        </div>
                        <div class="mb-3">
                            <label for="content" class="form-label">Full Content</label>
                            <textarea class="form-control" id="content" v-model.trim="full_book_modal_content" required></textarea>
                        </div>
                        <!-- image link -->
                        <div class="mb-3">
                            <label for="image" class="form-label">Image</label>
                            <input type="text" class="form-control" id="image" v-model.trim="image" required>
                        </div>
                        <button type="submit" class="btn btn-primary" @click="submit_book_update">Update
                            Book</button>
                    </form>



                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <!-- add Book Modal -->
    <div class="modal fade" id="addBookModal" tabindex="-1" aria-labelledby="addBookModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addBookModalLabel">Add Book</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addBook">
                        <div class="mb-3">
                            <label for="bookName" class="form-label">Book Name</label>
                            <input type="text" class="form-control" id="bookName" v-model.trim="bookName" required>
                        </div>
                        <div class="mb-3">
                            <label for="author" class="form-label">Author</label>
                            <input type="text" class="form-control" id="author" v-model.trim="author" required>
                        </div>
                        <div class="mb-3">
                            <label for="content" class="form-label">Content</label>
                            <textarea class="form-control" id="content" v-model.trim="content" required></textarea>
                        </div>
                        <!-- image link -->
                        <div class="mb-3">
                            <label for="image" class="form-label">Image</label>
                            <input type="text" class="form-control" id="image" v-model.trim="image" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Add Book</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
                        id="closebookmodal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <!-- add book delete modal -->
    <div class="modal fade" id="deleteBookModal" tabindex="-1" aria-labelledby="deleteBookModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                </div>
                <div class="modal-body">
                    Are you sure you want to delete this book?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
// to get section if from url
import jsPDF from 'jspdf';

export default {

    data() {
        return {
            sectionId: this.$route.params.id,
            section: {},
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
                const response = await fetch(`http://127.0.0.1:5000/full-book/${bookId}`, {
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
            this.contentfull_book_modal_content = this.books.find(book => book.id === bookId).full_book_modal_content;
            this.author = this.books.find(book => book.id === bookId).author;
            this.image = this.books.find(book => book.id === bookId).image;
        },
        async submit_book_update() {
            console.log(this.contentfull_book_modal_content,"aaaaaaaaaaaaa")
            const bookData = {
                name: this.bookName,
                full_content: this.full_book_modal_content,
                author: this.author,
                image: this.image,
            };
            console.log(bookData);
            try {
                const response = await fetch('http://127.0.0.1:5000/book/' + this.bookId, {
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
                const response = await fetch(`http://127.0.0.1:5000/book/${this.bookToDelete}`, {
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
                const response = await fetch(`http://127.0.0.1:5000/section/${this.sectionId}`);
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
                const response = await fetch('http://127.0.0.1:5000/add-book', {
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
                // to hide the modal
                // to reload the page
                this.bookName = '';
                this.content = '';
                this.author = '';
                this.image = '';
                this.fetchSection();
                // to close the modal
                // click on close button
                const closebtn = document.getElementById('closebookmodal');
                closebtn.click();
            } catch (error) {
                console.error('Error adding section:', error);
            }
        },
    }
};
</script>
<style>
.container {
    padding: 20px;
}

.card {
    margin-bottom: 20px;
}

.card-img-top {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.btn-primary {
    width: 49%; 
    background-color: rgb(94, 29, 168);
  border-color: #08131f;
}
.btn-secondary {
    background-color: rgb(29, 124, 168);
  border-color: #08131f;
}
.btn-success {
    background-color: rgb(8, 122, 122);
  border-color: #08131f;
}
.section-border {
    border: 2px solid brown;
    padding: 10px;
    margin-bottom: 20px;
}
</style>