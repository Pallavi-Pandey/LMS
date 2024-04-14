<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1 class="request-heading" >Requests</h1>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Book Title</th>
                                <th>Requested By</th>
                                <th>Requested On</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="request in requests" :key="request.id">
                                <td>{{ request.book_title }} </td>
                                <td>{{ request.user_name }}</td>
                                <td>{{ readable_date(request.requested_date) }}</td>
                                <td>{{ request.status }}</td>
                                <td>
                                   <!-- add approve and reject call the  functions for the buttons on click -->
                                    <button v-if="request.status==='requested'" type="button" class="btn btn-success" @click="approveRequest(request.id)">Approve</button>
                                    <button v-if="request.status==='requested'" type="button" class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>

                                </td>

                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    data() {
        return {
            requests: [],

           
        };
    },
    methods: {
        async getRequests() {
            try {
                const response = await fetch('http://127.0.0.1:5000/requests', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    }
                });
                if (!response.ok) {
                    throw new Error('Unable to fetch requests');
                }
                const data = await response.json();
                console.log('Requests:', data);
                this.requests = data;
                console.log('Requests:', this.requests);
            } catch (error) {
                console.error('Error fetching requests:', error);
            }
        },
        readable_date(date){
            return new Date(date).toLocaleDateString()
        },
        async approveRequest(requestId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/approve-request/${requestId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    }
                });
                if (!response.ok) {
                    throw new Error('Unable to approve request');
                }
                console.log('Request approved successfully');
                this.getRequests();
            } catch (error) {
                console.error('Error approving request:', error);
            }
    },

        async rejectRequest(requestId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/reject-request/${requestId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    }
                });
                if (!response.ok) {
                    throw new Error('Unable to reject request');
                }
                console.log('Request rejected successfully');
                this.getRequests();
            } catch (error) {
                console.error('Error rejecting request:', error);
            }
        },
    },

    created() {
        this.getRequests();
    }
};

</script>
<style>
    .request-heading {
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Style the table */
table {
    width: 100%;
    border-collapse: collapse;
}

/* Style the table header */
th {
    background-color: #7eaad6;
    color: #fff;
    padding: 12px;
    text-align: left;
}

/* Style the table cells */
td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd; /* Add a bottom border to separate rows */
}

/* Style alternating rows */
tr:nth-child(even) {
    background-color: #f2f2f2;
}

/* Hover effect on rows */
tr:hover {
    background-color: #ddd;
}

/* Style the buttons */
.btn {
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
}

/* Style the approve button */
.btn-success {
    background-color: #5cb8a9;
    border: 1px solid #4cae99;
    color: #fff;
}

/* Style the reject button */
.btn-danger {
    background-color: #d9534f;
    border: 1px solid #d43f3a;
    color: #fff;
}

/* Adjust button margins */
.btn {
    margin-right: 5px;
}

    
</style>