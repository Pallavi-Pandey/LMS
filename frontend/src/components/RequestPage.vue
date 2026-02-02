<template>
  <div class="dashboard-container">
    <div class="row mb-5">
      <div class="col-md-12 text-center">
        <h1 class="display-5 fw-bold text-white mb-2">Book Requests</h1>
        <p class="text-white-50">Manage student access and book approvals</p>
      </div>
    </div>

    <div class="glass-panel p-4">
      <div v-if="requests.length > 0" class="table-responsive">
        <table class="table table-hover align-middle mb-0 custom-table">
          <thead class="text-primary fw-bold border-bottom border-light">
            <tr>
              <th scope="col" class="ps-4">Book Details</th>
              <th scope="col">Student</th>
              <th scope="col">Date</th>
              <th scope="col">Status</th>
              <th scope="col" class="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id" class="table-row-hover">
              <td class="ps-4">
                <div class="d-flex align-items-center">
                  <div class="icon-square bg-primary-subtle text-primary rounded-3 me-3">
                    <i class="bi bi-book"></i>
                  </div>
                  <div>
                    <h6 class="mb-0 fw-bold text-dark">{{ request.book_title }}</h6>
                    <small class="text-muted">ID: {{ request.id }}</small>
                  </div>
                </div>
              </td>
              <td>
                <div class="d-flex align-items-center gap-2">
                   <div class="avatar-circle bg-white text-secondary shadow-sm">
                      {{ request.user_name.charAt(0).toUpperCase() }}
                   </div>
                   <span class="fw-medium">{{ request.user_name }}</span>
                </div>
              </td>
              <td>{{ readable_date(request.requested_date) }}</td>
              <td>
                <span class="badge rounded-pill px-3 py-2" :class="statusClass(request.status)">
                  {{ request.status }}
                </span>
              </td>
              <td class="text-end pe-4">
                <div v-if="request.status === 'requested'" class="d-flex justify-content-end gap-2">
                  <button @click="approveRequest(request.id)" class="btn btn-sm btn-premium rounded-pill px-3">
                    <i class="bi bi-check-lg me-1"></i> Approve
                  </button>
                  <button @click="rejectRequest(request.id)" class="btn btn-sm btn-outline-danger rounded-pill px-3">
                    <i class="bi bi-x-lg me-1"></i> Reject
                  </button>
                </div>
                <div v-else-if="request.status === 'approved'">
                   <button @click="revokeAccess(request.id)" class="btn btn-sm btn-outline-warning rounded-pill px-3">
                    <i class="bi bi-arrow-counterclockwise me-1"></i> Revoke
                  </button>
                </div>
                <span v-else class="text-muted small fst-italic">Completed</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center py-5">
         <div class="empty-state">
            <i class="bi bi-inbox fs-1 text-white-50 mb-3 d-block"></i>
            <p class="text-white fs-5">No pending requests found.</p>
         </div>
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE_URL from "../config";

export default {
    data() {
        return {
            requests: []
        };
    },
    created() {
        this.getRequests();
    },
    methods: {
        statusClass(status) {
            switch(status) {
                case 'requested': return 'bg-warning-subtle text-warning-emphasis border border-warning';
                case 'approved': return 'bg-success-subtle text-success-emphasis border border-success';
                case 'rejected': return 'bg-danger-subtle text-danger-emphasis border border-danger';
                default: return 'bg-secondary-subtle text-secondary';
            }
        },
        async getRequests() {
            try {
                const response = await fetch(`${API_BASE_URL}/requests`, {
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
            return new Date(date).toLocaleDateString(undefined, {
                year: 'numeric', month: 'short', day: 'numeric'
            });
        },
        async revokeAccess(requestId) {
            try {
                const response = await fetch(`${API_BASE_URL}/revoke-access/${requestId}`, {
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
                const response = await fetch(`${API_BASE_URL}/approve-request/${requestId}`, {
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
                const response = await fetch(`${API_BASE_URL}/reject-request/${requestId}`, {
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
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* For table border radius */
}

/* Custom Table Styling */
.custom-table {
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.custom-table thead th {
  background: rgba(255, 255, 255, 0.5);
  padding: 1.25rem 1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-size: 0.85rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.05);
}

.custom-table tbody td {
  padding: 1.25rem 1rem;
  vertical-align: middle;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  background: transparent;
}

.table-row-hover {
  transition: all 0.2s ease;
}

.table-row-hover:hover {
  background-color: rgba(255, 255, 255, 0.6) !important;
  transform: scale(1.002);
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  position: relative;
  z-index: 1;
}

.icon-square {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 700;
}
</style>
