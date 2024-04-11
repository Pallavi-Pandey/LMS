<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1>Requests</h1>
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
