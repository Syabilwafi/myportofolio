window.showToast = (message, type = 'success', timeout = 4000) => {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${['success', 'error', 'info'].includes(type) ? type : 'info'}`;
    toast.textContent = String(message);
    container.append(toast);
    requestAnimationFrame(() => toast.classList.add('is-visible'));
    setTimeout(() => {
        toast.classList.remove('is-visible');
        setTimeout(() => toast.remove(), 250);
    }, timeout);
};
