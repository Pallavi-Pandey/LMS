<template>
  <div>
    <h1>Welcome to the Library</h1>
    <!-- to show the username -->
    <h2 style="color: blue;"> {{ user_email }} </h2>
    <!-- Search input -->
    <input type="text" v-model="searchQuery" placeholder="Search books...">
    <div v-for="section in filteredSections" :key="section.id">
      <h2>{{ section.name }} 
      :  {{ section.books.length }} -  Books
      </h2>

      <div class="card-group">
        <div v-for="book in section.books" :key="book.id" class="card">
          <img :src="book.image" class="card-img-top" alt="Book Cover">
          <div class="card-body">
            <h5 class="card-title">Title: {{ book.name }}</h5>
            <p class="card-text"> preview-content: {{ book.content }}</p>
            <p class="card-text">Author : {{ book.author }}</p>
            <p class="card-text"> Status : <b style="color: red;">{{ book.status }}</b></p>
            <!-- if requested show requested date , add a v-if-->
            <p v-if="book.status === 'requested'" class="card-text"> Requested on : {{ make_date_readable(book.requested_date) }}</p>
            <p v-if="book.status === 'approved'" class="card-text"> Rented on : {{ make_date_readable(book.requested_date) }} </p>
            <p v-if="book.status === 'approved'" class="card-text"> Due Date : {{ make_date_readable(add_7_days(book.requested_date)) }} </p>
            <p v-if="book.status === 'approved'" class="card-text"> No of Days Left : {{ get_remaining_days(book.requested_date) }} </p>

            <!-- if book is available show rent button, if requested show revoke button, if rented show return -->
            <button v-if="book.status === 'available'" @click="rent_book(book.id)" class="btn btn-primary">Rent</button>
            <button v-if="book.status === 'requested'" @click="revoke_book(book.id)" class="btn btn-danger">Revoke</button>
            <button v-if="book.status === 'approved'" @click="return_book(book.id)" class="btn btn-success">Return</button>
            <button v-if="book.status === 'approved'" type="button" class="btn btn-primary" data-bs-toggle="modal"
                            data-bs-target="#ViewFullBook" @click="get_full_book(book.id)">
                        
View Full Book                    </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="ViewFullBook" tabindex="-1" aria-labelledby="ViewFullBook" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
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
export default {
  data() {
    return {
      sections: [],
      user_email: localStorage.getItem('email'),
      searchQuery: '',
      full_book_modal_content:'',
      books_rented:0
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
          book.name.toLowerCase().includes(this.searchQuery.toLowerCase())||
          book.author.toLowerCase().includes(this.searchQuery.toLowerCase())||
          book.content.toLowerCase().includes(this.searchQuery.toLowerCase())||
          book.status.toLowerCase().includes(this.searchQuery.toLowerCase())           

        )
      })).filter(section => section.books.length > 0);
    }
  },
  methods: {
    add_7_days(date){
      return new Date(date).setDate(new Date(date).getDate() + 7);
    },  
    // Sun, 14 Apr 2024 14:51:17 GMT to convert this to Sun, 14 Apr 2024 14:51
    convert_to_date_and_time(date){
      return new Date(date).toDateString();

    },
    get_remaining_days(date){
      const due_date = new Date(date).setDate(new Date(date).getDate() + 7);
      const remaining_days = Math.ceil((due_date - new Date().getTime()) / (1000 * 60 * 60 * 24));
      return remaining_days;
    },

    async get_full_book(bookId) {
            // fetch book content
            try {
                const response = await fetch(`http://127.0.0.1:5000/full-book/${bookId}`,{
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
    async return_book(book_id) {
      try {
        const response = await fetch('http://127.0.0.1:5000/return-book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({"book_id": book_id })
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

    async get_books_rented() {
      try {
        const response = await fetch('http://127.0.0.1:5000/books-rented', {
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
          if (this.books_rented>=5){
            alert('OOPS !!! You can rent only 5 books at a time.');
            return;
          }
          
        
         if (!confirm('Taking you to payment gateway, do you want to continue?')) {
          return;
         }
         if(!confirm('pay 1000 to rent the book?')){
           return;
         }
        
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
        if (response.status===223){
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
        const response = await fetch('http://127.0.0.1:5000/revoke-book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({"book_id": book_id })
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
        
    make_date_readable(date){
      return new Date(date).toDateString();
    },
  },
};
</script>
