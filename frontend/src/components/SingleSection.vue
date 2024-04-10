<template>
    single section {{ sectionId }}
    {{ section }}

    <div v-if="section">
        <h1>{{ section.name }}</h1>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addBookModal">
            add Book
        </button>
        <ul>
            <div v-for="book in books" :key="book.id">
                <div class="card" style="width: 18rem;">
                    <img :src="book.image" class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title
                        ">{{ book.name }}</h5>
                        <p class="card-text">{{ book.content }}</p>
                        <p class="card-text">{{ book.author }}</p>
                        <div class="d-flex justify-content-between">
                            <button type="button" class="btn btn-primary">Update</button>
                            <button type="button" class="btn btn-danger">Delete</button>
                            
                        </div>
                    </div>
                </div>
                <br>
            </div>
        </ul>
    </div>

    <!-- add Book Modal -->
    <div class="modal fade" id="addBookModal" tabindex="-1" aria-labelledby="addBookModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addBookModalLabel">add Book</h1>
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
                        <button type="submit" class="btn btn-primary">add Book</button>
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
export default {
    data() {
        return {
            sectionId: this.$route.params.id,
            section: {},
            books: [],
            bookName: '',
            content: '',
            author: '',
            image: ''

        };
    },
    created() {
        this.fetchSection();
    },
    methods: {
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
                this.books = data.books;


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