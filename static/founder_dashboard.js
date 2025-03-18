document.addEventListener("DOMContentLoaded", function () {
    // Modal functionality
    const modal = document.getElementById('company-modal');
    const openModalBtn = document.getElementById('list-company-btn');
    const closeModalBtn = document.querySelector('.modal-close');
    const cancelBtn = document.querySelector('.cancel-btn');
    const toast = document.getElementById('toast');

    // Open modal
    openModalBtn.addEventListener('click', () => {
        modal.classList.add('show');
    });

    // Close modal
    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    // Close modal with cancel button
    cancelBtn.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });

    // Show toast notification
    function showToast(title, message) {
        document.querySelector('.toast-title').textContent = title;
        document.querySelector('.toast-message').textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // Handle form submission
    document.getElementById('company-form').addEventListener('submit', function (e) {
        showToast('Company Listed', 'Your company has been successfully listed.');
    });

    // Connect button functionality
    document.querySelectorAll('.connect-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            showToast('Connection Request', 'Your connection request has been sent.');
        });
    });

    // Details button functionality
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            showToast('Startup Details', 'Viewing details for this startup.');
        });
    });

    // Logout functionality
    document.getElementById('logout-btn').addEventListener('click', () => {
        showToast('Logged out', 'You have been successfully logged out.');
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
    });
});
