<template>
    <div class="page-container">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1 class="request-heading">Requests</h1>
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
                                <td>{{ request.book_title }}</td>
                                <td>{{ request.user_name }}</td>
                                <td>{{ readable_date(request.requested_date) }}</td>
                                <td>{{ request.status }}</td>
                                <td>
                                    <button v-if="request.status==='requested'" type="button" class="btn btn-success" @click="approveRequest(request.id)">Approve</button>
                                    <button v-if="request.status==='requested'" type="button" class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
                                    <button v-else-if="request.status==='approved'" type="button" class="btn btn-secondary" @click="revokeAccess(request.id)">Revoke</button>
                                    <p v-else class="no-actions">No Actions</p>
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
            requests: []
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
                this.requests = data;
            } catch (error) {
                console.error('Error fetching requests:', error);
            }
        },
        readable_date(date) {
            return new Date(date).toLocaleDateString();
        },
        async revokeAccess(requestId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/revoke-access/${requestId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    }
                });
                if (!response.ok) {
                    throw new Error('Unable to revoke request');
                }
                this.getRequests();
            } catch (error) {
                console.error('Error revoking request:', error);
            }
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

<style scoped>
.page-container {
    background-color: #c9d7e4;
    padding: 20px;
}

.request-heading {
    margin-top: 10px;
    margin-bottom: 20px;
    color: #343a40;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

th {
    background-color: #8161a7;
    color: #fff;
    padding: 12px;
    text-align: left;
}

td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
}

tbody tr:nth-child(odd) {
    background-color: #f8f9fa;
}

tbody tr:hover {
    background-color: #e2e6ea;
}

.btn {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-success {
    background-color: #28a745;
    border: 1px solid #218838;
    color: #fff;
}

.btn-danger {
    background-color: #dc3545;
    border: 1px solid #c82333;
    color: #fff;
}

.btn-secondary {
    background-color: #6c757d;
    border: 1px solid #5a6268;
    color: #fff;
}

.btn + .btn {
    margin-left: 5px;
}

.no-actions {
    color: #6c757d;
    margin: 0;
}

@media (max-width: 768px) {
    .btn {
        padding: 6px 12px;
    }
}
</style>
