<template>
  <div>
    <h1 style="margin-bottom: 3%;" >Welcome to the Library: <span style="color: mediumpurple;">{{ user_email }}</span></h1>
    <input type="text" v-model="searchQuery" placeholder="Search books..." class="form-control">
    <div v-for="section in filteredSections" :key="section.id">
      <hr>
      <h2 class="section-name">{{ section.name }} : {{ section.books.length }} - Books</h2>
      <hr>
      <div class="row row-cols-1 row-cols-md-3 g-3">
        <div v-for="book in section.books" :key="book.id" class="col">
          <div class="card">
            <img :src="book.image" class="card-img-top" alt="Book Cover">
            <div class="card-body">
              <h5 class="card-title">Book Title: {{ book.name }}</h5>
              <h6 class="card-text">Author: {{ book.author }}</h6>
              <p class="card-text">{{ book.content }}</p>
              <p class="card-text">Status: <b style="color: red;">{{ book.status }}</b></p>
              <p v-if="book.status === 'requested'" class="card-text">Requested on: {{
                make_date_readable(book.requested_date) }}</p>
              <p v-if="book.status === 'approved'" class="card-text">Rented on: {{
                make_date_readable(book.requested_date) }}</p>
              <p v-if="book.status === 'approved'" class="card-text">Due Date: {{
                make_date_readable(add_7_days(book.requested_date)) }}</p>
              <p v-if="book.status === 'approved'" class="card-text">Days Left to Return: {{
                get_remaining_days(book.requested_date) }}</p>
              <div class="d-flex justify-content-between">
                <button v-if="book.status === 'available'" @click="rent_book(book.id)"
                  class="btn btn-primary">Rent</button>
                <button v-if="book.status === 'requested'" @click="revoke_book(book.id)"
                  class="btn btn-danger">Revoke</button>

                <!-- <button v-if="book.status === 'approved'" @click="return_book(book.id)"
                  class="btn btn-success">Return</button> -->
                  <button v-if="book.status === 'approved'" type="button" class="btn btn-secondary" @click="set_review_modal_data(book.id)" data-bs-toggle="modal" data-bs-target="#reviewBookModal">
                    Review & Return
            </button>
                <button v-if="book.status === 'approved'" type="button" class="btn btn-primary" data-bs-toggle="modal"
                  data-bs-target="#ViewFullBook" @click="get_full_book(book.id,book.name)">View Full Book</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="reviewBookModal" tabindex="-1" aria-labelledby="reviewBookModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="reviewBookModalLabel">Review  & Return</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addBook">
                        
                       
                        <!-- Rating 1 to 5 -->
                        <div class="mb-3">
                            <label for="rating" class="form-label">Rating (1-5)</label>
                            <input type="number" class="form-control" id="rating" v-model.trim="rating" required>
                        </div>
                        <!-- image link -->
                        <div class="mb-3">
                            <label for="image" class="form-label">FeedBack</label>
                            <input type="text" class="form-control" id="feedback" v-model.trim="feedback" required>
                        </div>
                        <button  @click="add_feedback(rating,feedback,review_modal_book_id)" class="btn btn-primary">Add Feedback & Return</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
                        id="closebookmodal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="ViewFullBook" tabindex="-1" aria-labelledby="ViewFullBookLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="ViewFullBookLabel">Book Details</h1>
            <!-- dowmload -->
      

            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<h2 class="btn btn-secondary" @click="download_book_as_pdf(full_book_modal_content,full_book_modal_name)">Download  {{ full_book_modal_name }}</h2>
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
    add_feedback(rating,feedback,bookId){
      console.log(rating,feedback,bookId)
      fetch('/add-feedback', {
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
          document.getElementById('closebookmodal').click();
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
    add_7_days(date) {
      return new Date(date).setDate(new Date(date).getDate() + 7);
    },
    // Sun, 14 Apr 2024 14:51:17 GMT to convert this to Sun, 14 Apr 2024 14:51
    convert_to_date_and_time(date) {
      return new Date(date).toDateString();

    },
    get_remaining_days(date) {
      const due_date = new Date(date).setDate(new Date(date).getDate() + 7);
      const remaining_days = Math.ceil((due_date - new Date().getTime()) / (1000 * 60 * 60 * 24));
      return remaining_days;
    },


    get_book_name_by_id(bookId){
      
      console.log(bookId)
      console.log(this.sections)
      
      return this.sections.map(section => section.books.filter(book => book.id == bookId)[0].name)[0];
    },
    

    async get_full_book(bookId,book_name) {
      // fetch book content
      try {
        const response = await fetch(`/full-book/${bookId}`, {
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
      try {
        const response = await fetch('/return-book', {
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
      try {
        const response = await fetch(`/sections`, {
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
      try {
        const response = await fetch('/books-rented', {
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
      // ask confirmation before 

      // get_books_rented call this 
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


        const response = await fetch('/rent-book', {
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
      try {
        const response = await fetch('/revoke-book', {
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
body {
  font-family: Arial, sans-serif;
}

/* Form Control */
.form-control {
  width: 100%;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 10px;
  border: 5px solid rgb(197, 180, 204);
}

/* Section Name */
.section-name {
  margin-top: 20px;
  margin-bottom: 10px;
  color: rgb(109, 60, 134);
}

/* Card */
.card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  width: 100%;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.card-title {
  font-weight: bold;
}

.card-text {
  color: #333;
}

/* Buttons */
.btn {
  border-radius: 10px;
  margin-top: 10px;
}

.btn-primary {
  background-color: rgb(116, 90, 168);
  border-color: rgb(101, 76, 151);
}

.btn-secondary {
  background-color: lightseagreen;
  border-color: lightseagreen;
}

.btn-success {
  background-color: forestgreen;
  border-color: forestgreen;
}

/* Modal */
.modal-header {
  background-color: rgb(109, 60, 134);
  color: #fff;
  border-bottom: none;
}

.modal-body {
  color: #333;
}

.modal-footer {
  background-color: #f3f3f3;
}

</style>
