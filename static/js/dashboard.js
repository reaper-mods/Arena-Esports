// ARENA ESPORTS - Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.admin-dashboard')) {
        initAdminDashboard();
    }
});

function initAdminDashboard() {
    loadDashboardStats();
    loadRecentUsers();
    loadTournamentOverview();
    setupCharts();
}

// Load dashboard statistics
function loadDashboardStats() {
    // This would typically fetch from API
    const stats = {
        totalUsers: document.querySelector('[data-stat="total-users"]')?.textContent || '0',
        activeTournaments: document.querySelector('[data-stat="active-tournaments"]')?.textContent || '0',
        totalRevenue: document.querySelector('[data-stat="total-revenue"]')?.textContent || '0',
        newRegistrations: document.querySelector('[data-stat="new-registrations"]')?.textContent || '0'
    };

    animateStats(stats);
}

// Animate statistics numbers
function animateStats(stats) {
    Object.keys(stats).forEach(key => {
        const element = document.querySelector(`[data-stat="${key}"]`);
        if (element) {
            animateValue(element, 0, parseInt(stats[key]), 2000);
        }
    });
}

// Animate value from start to end
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = formatNumber(end);
            clearInterval(timer);
        } else {
            element.textContent = formatNumber(Math.floor(current));
        }
    }, 16);
}

// Format large numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Load recent users
function loadRecentUsers() {
    const userList = document.getElementById('recent-users-list');
    if (!userList) return;

    // Fetch recent users
    fetch('/api/admin/recent-users/')
        .then(response => response.json())
        .then(users => {
            userList.innerHTML = users.map(user => `
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                        <div class="avatar-circle me-3">
                            ${user.full_name.charAt(0)}
                        </div>
                        <div>
                            <h6 class="mb-0">${user.full_name}</h6>
                            <small class="text-muted">${user.email}</small>
                        </div>
                    </div>
                    <div>
                        <span class="badge bg-${user.user_type === 'admin' ? 'danger' : 'primary'}">
                            ${user.user_type}
                        </span>
                        <small class="text-muted ms-2">${formatDate(user.created_at)}</small>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error loading users:', error));
}

// Load tournament overview
function loadTournamentOverview() {
    const tournamentList = document.getElementById('tournament-overview');
    if (!tournamentList) return;

    // Fetch tournaments
    fetch('/api/admin/tournaments-overview/')
        .then(response => response.json())
        .then(tournaments => {
            tournamentList.innerHTML = tournaments.map(tournament => `
                <div class="col-md-6 mb-3">
                    <div class="card tournament-overview-card">
                        <div class="card-body">
                            <h6 class="card-title">${tournament.name}</h6>
                            <p class="card-text">
                                <small class="text-muted">
                                    <span class="me-3">
                                        <i class="bi bi-people"></i> ${tournament.registrations_count} participants
                                    </span>
                                    <span>
                                        <i class="bi bi-trophy"></i> ${formatCurrency(tournament.prize_pool)}
                                    </span>
                                </small>
                            </p>
                            <div class="progress" style="height: 5px;">
                                <div class="progress-bar" 
                                     style="width: ${(tournament.registrations_count / tournament.max_participants) * 100}%">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error loading tournaments:', error));
}

// Setup charts (using Chart.js if available)
function setupCharts() {
    const revenueChart = document.getElementById('revenue-chart');
    if (!revenueChart) return;

    // Check if Chart.js is available
    if (typeof Chart !== 'undefined') {
        createRevenueChart(revenueChart);
        createUserGrowthChart();
        createTournamentDistributionChart();
    }
}

// Create revenue chart
function createRevenueChart(canvas) {
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Revenue',
                data: [12000, 19000, 15000, 25000, 22000, 30000],
                borderColor: '#00d4ff',
                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Create user growth chart
function createUserGrowthChart() {
    const canvas = document.getElementById('user-growth-chart');
    if (!canvas) return;

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'New Users',
                data: [50, 75, 60, 90, 80, 120, 100],
                backgroundColor: '#7b61ff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Create tournament distribution chart
function createTournamentDistributionChart() {
    const canvas = document.getElementById('tournament-distribution-chart');
    if (!canvas) return;

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Valorant', 'CS:GO', 'FIFA', 'PUBG', 'Fortnite'],
            datasets: [{
                data: [30, 25, 20, 15, 10],
                backgroundColor: [
                    '#00d4ff',
                    '#7b61ff',
                    '#ff6b6b',
                    '#4ecdc4',
                    '#ffe66d'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// User search functionality
function searchUsers(query) {
    const resultsContainer = document.getElementById('user-search-results');
    if (!resultsContainer) return;

    if (query.length < 2) {
        resultsContainer.innerHTML = '';
        return;
    }

    fetch(`/api/admin/search-users/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(users => {
            resultsContainer.innerHTML = users.map(user => `
                <a href="/admin/users/${user.uid}/edit/" class="list-group-item list-group-item-action">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0">${user.full_name}</h6>
                            <small class="text-muted">${user.email}</small>
                        </div>
                        <span class="badge bg-${user.is_banned ? 'danger' : 'success'}">
                            ${user.is_banned ? 'Banned' : 'Active'}
                        </span>
                    </div>
                </a>
            `).join('');
        })
        .catch(error => console.error('Search error:', error));
}

// Handle bulk user actions
function bulkUserAction(action) {
    const selectedUsers = document.querySelectorAll('.user-select:checked');
    if (selectedUsers.length === 0) {
        alert('Please select at least one user');
        return;
    }

    const userIds = Array.from(selectedUsers).map(cb => cb.value);

    if (confirm(`Are you sure you want to ${action} ${userIds.length} user(s)?`)) {
        fetch('/api/admin/bulk-user-action/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                action: action,
                user_ids: userIds
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error performing action');
            }
        })
        .catch(error => console.error('Bulk action error:', error));
    }
}

// Tournament management functions
function deleteTournament(uid) {
    if (confirm('Are you sure you want to delete this tournament? This action cannot be undone.')) {
        fetch(`/admin/tournaments/${uid}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Delete error:', error));
    }
}

// Export data function
function exportData(type) {
    window.location.href = `/admin/export/${type}/`;
}