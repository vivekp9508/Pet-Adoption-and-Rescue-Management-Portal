function getToken() {
    return localStorage.getItem('access_token');
}

function logout() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const isAdmin = user.is_staff === true || user.is_admin_user === true;

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');

    window.location.replace(isAdmin ? '/pets/admin-login/' : '/users/login/');
}

async function refreshAccessToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return null;
    const res = await fetch('/users/api/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });
    if (res.ok) {
        const data = await res.json();
        localStorage.setItem('access_token', data.access);
        return data.access;
    }
    return null;
}

async function loadUserNotifications() {
    let token = getToken();
    if (!token) return;

    let res = await fetch('/pets/api/notifications/', {
        headers: { 'Authorization': 'Bearer ' + token }
    });

    if (res.status === 401) {
        token = await refreshAccessToken();
        if (!token) return;
        res = await fetch('/pets/api/notifications/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
    }

    if (!res.ok) return;
    const notifications = await res.json();
    const unread = notifications.filter(n => !n.is_read);

    const countEl = document.getElementById('notif-count');
    if (unread.length > 0) {
        countEl.textContent = unread.length;
        countEl.style.display = 'flex';
    } else {
        countEl.style.display = 'none';
    }

    const listEl = document.getElementById('notif-list');
    if (!notifications.length) {
        listEl.innerHTML = '<div class="notif-item">No notifications yet.</div>';
        return;
    }

    listEl.innerHTML = notifications.slice(0, 8).map(n => `
        <div class="notif-item ${n.is_read ? '' : 'unread'}">
            ${n.message}
            <small>${new Date(n.created_at).toLocaleDateString('en-IN', {day:'numeric', month:'short', year:'numeric'})}</small>
        </div>
    `).join('');
}

function toggleNotifDropdown() {
    const dropdown = document.getElementById('notif-dropdown');
    const isOpen = dropdown.style.display === 'block';
    dropdown.style.display = isOpen ? 'none' : 'block';

    if (!isOpen) {
        // Mark as read when opened
        const token = getToken();
        if (token) {
            fetch('/pets/api/notifications/read/', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer ' + token }
            }).then(() => {
                document.getElementById('notif-count').style.display = 'none';
            });
        }
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
    const wrapper = document.getElementById('nav-notif-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        const dropdown = document.getElementById('notif-dropdown');
        if (dropdown) dropdown.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const token = getToken();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (token) {
        document.getElementById('nav-login').style.display = 'none';
        document.getElementById('nav-register').style.display = 'none';
        document.getElementById('nav-logout').style.display = 'inline';
        document.getElementById('nav-my-reports').style.display = 'inline';
        document.getElementById('nav-report').style.display = 'inline';
        document.getElementById('nav-search').style.display = 'inline';

        const navUser = document.getElementById('nav-user');
        if (navUser) {
            navUser.textContent = `👤 ${user.username || user.email || ''}`;
            navUser.style.display = 'inline';
        }

        // Show notification bell for regular users only
        if (!user.is_staff && !user.is_admin_user) {
            document.getElementById('nav-notif-wrapper').style.display = 'inline';
            loadUserNotifications();
        }
    }
});