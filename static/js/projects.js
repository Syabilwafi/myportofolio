const initializeProjects = () => {
    const sidebar = document.getElementById('project-sidebar');
    const display = document.getElementById('project-display');
    const search = document.getElementById('search-input');
    const star = document.getElementById('star-btn');
    const modal = document.getElementById('project-modal');
    const form = document.getElementById('project-create-form');
    const editModal = document.getElementById('project-edit-modal');
    const editForm = document.getElementById('project-edit-form');
    let current = null;
    let controller;
    let requestVersion = 0;
    let debounceTimer;

    const safeUrl = value => {
        try {
            const url = new URL(value);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : null;
        } catch { return null; }
    };

    const urlForProject = (pattern, id) =>
        pattern.replace('00000000-0000-0000-0000-000000000000', encodeURIComponent(id));
    const apiError = async (response, fallback) => {
        let data = {};
        try { data = await response.json(); } catch { return fallback; }
        if (response.status === 400) {
            return Object.entries(data).flatMap(([field, errors]) =>
                (Array.isArray(errors) ? errors : [errors]).map(error =>
                    `${field}: ${typeof error === 'string' ? error : error.message || 'Invalid value.'}`
                )).join('\n') || fallback;
        }
        if (response.status === 403) return data.detail || 'You do not have permission to perform this action.';
        return data.detail || fallback;
    };

    const getCookie = name => {
        const prefix = `${name}=`;
        const cookie = document.cookie.split(';').map(value => value.trim())
            .find(value => value.startsWith(prefix));
        return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
    };

    const updateDisplay = item => {
        current = item;
        document.getElementById('active-project-title').textContent = item.name;
        document.getElementById('active-project-desc').textContent = item.description;
        const link = document.getElementById('active-project-link');
        const frame = document.getElementById('active-project-frame');
        const url = safeUrl(item.url);
        if (url) link.href = url;
        else link.removeAttribute('href');
        frame.src = url || 'about:blank';
        frame.title = item.name;
        document.getElementById('star-count').textContent = item.star_count;
        star.classList.toggle('is-starred', item.is_starred);
        star.setAttribute('aria-pressed', String(item.is_starred));
        ['edit-btn', 'delete-btn'].forEach(id => {
            const button = document.getElementById(id);
            if (button) button.style.display = 'flex';
        });
    };

    const loadProjects = async (preferredId = current?.id) => {
        controller?.abort();
        controller = new AbortController();
        const version = ++requestVersion;
        sidebar.setAttribute('aria-busy', 'true');
        sidebar.replaceChildren();
        const loading = document.createElement('p');
        loading.className = 'no-projects';
        loading.textContent = 'Loading projects...';
        sidebar.append(loading);
        display.style.display = 'none';
        current = null;
        try {
            const url = new URL(document.querySelector('[data-projects-url]').dataset.projectsUrl, location.origin);
            url.searchParams.set('q', search.value.trim());
            const response = await fetch(url, { signal: controller.signal, credentials: 'same-origin' });
            if (!response.ok) throw new Error('Unable to load projects. Please try again.');
            const projects = await response.json();
            if (version !== requestVersion) return false;
            sidebar.replaceChildren();
            display.style.display = projects.length ? 'flex' : 'none';
            current = null;
            if (!projects.length) {
                const empty = document.createElement('p');
                empty.className = 'no-projects';
                empty.textContent = search.value ? 'No matching projects.' : 'No projects available.';
                sidebar.append(empty);
                return true;
            }
            const projectArea = document.querySelector('.projects-content');
            projects.forEach(item => {
                item.detail_url = urlForProject(projectArea.dataset.projectDetailUrl, item.id);
                item.star_url = urlForProject(projectArea.dataset.projectStarUrl, item.id);
            });
            const selected = projects.find(item => item.id === preferredId) || projects[0];
            projects.forEach(item => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'project-tab-btn';

                button.textContent = `> ${item.name}`;
                button.classList.toggle('active', item.id === selected.id);
                button.addEventListener('click', () => {
                    sidebar.querySelectorAll('button').forEach(tab => tab.classList.remove('active'));
                    button.classList.add('active');
                    updateDisplay(item);
                });
                sidebar.append(button);
            });
            updateDisplay(selected);
            return true;
        } catch (error) {
            if (error.name !== 'AbortError' && version === requestVersion) {
                showToast(error.message, 'error');
                sidebar.replaceChildren();
                const message = document.createElement('p');
                message.className = 'no-projects';
                message.textContent = 'Unable to load projects. Try searching again.';
                sidebar.append(message);
            }
            return false;
        } finally {
            if (version === requestVersion) sidebar.setAttribute('aria-busy', 'false');
        }
    };

    search.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        controller?.abort();
        ++requestVersion;
        debounceTimer = setTimeout(() => loadProjects(), 400);
    });
    const editButton = document.getElementById('edit-btn');
    if (editButton && editModal && editForm) {
        editButton.addEventListener('click', () => {
            if (!current) return;
            editForm.elements.name.value = current.name;
            editForm.elements.url.value = current.url || '';
            editForm.elements.description.value = current.description;
            editForm.dataset.detailUrl = current.detail_url;
            editModal.showModal();
        });
        document.getElementById('close-project-edit-modal').addEventListener('click', () => editModal.close());
        editForm.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = editForm.querySelector('[type=submit]');
            submit.disabled = true;
            try {
                const response = await fetch(editForm.dataset.detailUrl, {
                    method: 'PATCH', credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || editForm.elements.csrfmiddlewaretoken.value },
                    body: JSON.stringify({ name: editForm.elements.name.value, url: editForm.elements.url.value || null, description: editForm.elements.description.value })
                });
                if (!response.ok) throw new Error(await apiError(response, 'Unable to update project.'));
                const updated = await response.json();
                await loadProjects(updated.id);
                editModal.close();
                showToast('Project updated successfully!', 'success');
            } catch (error) { showToast(error.message, 'error'); }
            finally { submit.disabled = false; }
        });
    }
    const deleteButton = document.getElementById('delete-btn');
    if (deleteButton) deleteButton.addEventListener('click', async () => {
        if (!current || !window.confirm(`Delete “${current.name}”?`)) return;
        deleteButton.disabled = true;
        try {
            const response = await fetch(current.detail_url, { method: 'DELETE', credentials: 'same-origin', headers: { 'X-CSRFToken': getCookie('csrftoken') || document.querySelector('.projects-content [name=csrfmiddlewaretoken]').value } });
            if (!response.ok) throw new Error(await apiError(response, 'Unable to delete project.'));
            showToast('Project deleted successfully!', 'success');
            await loadProjects();
        } catch (error) { showToast(error.message, 'error'); }
        finally { deleteButton.disabled = false; }
    });

    if (!star.classList.contains('login-required')) {
        star.addEventListener('click', async () => {
            const item = current;
            if (!item || star.disabled) return;
            star.disabled = true;
            try {
                const response = await fetch(item.star_url, {
                    method: 'POST', credentials: 'same-origin',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') || '' }
                });
                if (!response.ok || response.redirected) throw new Error(await apiError(response, 'Unable to star project. Check your login and try again.'));
                const data = await response.json();
                Object.assign(item, data);
                if (current === item) updateDisplay(item);
            } catch (error) { showToast(error.message, 'error'); }
            finally { star.disabled = false; }
        });
    }

    if (modal && form) {
        const trigger = document.getElementById('open-project-modal');
        trigger.addEventListener('click', () => modal.showModal());
        document.getElementById('close-project-modal').addEventListener('click', () => modal.close());
        modal.addEventListener('click', event => {
            const bounds = modal.getBoundingClientRect();
            if (event.target === modal && (event.clientX < bounds.left || event.clientX > bounds.right ||
                event.clientY < bounds.top || event.clientY > bounds.bottom)) modal.close();
        });

        form.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = form.querySelector('[type=submit]');
            const errors = document.getElementById('project-form-errors');
            if (submit.disabled) return;
            submit.disabled = true;
            errors.textContent = '';
            try {
                const response = await fetch(form.action, {
                    method: 'POST', credentials: 'same-origin', body: new FormData(form),
                    headers: { 'X-CSRFToken': getCookie('csrftoken') || form.elements.csrfmiddlewaretoken.value }
                });
                if (!response.headers.get('content-type')?.includes('application/json')) {
                    throw new Error('Request rejected. Reload the page to renew your session and try again.');
                }
                const data = await response.json();
                if (!response.ok) {
                    const validationErrors = Object.entries(data.errors || data).flatMap(([field, items]) =>
                        (Array.isArray(items) ? items : [items]).map(item =>
                            `${field}: ${typeof item === 'string' ? item : item.message || 'Invalid value.'}`
                        )).join('\n');
                    const message = response.status === 400
                        ? validationErrors || data.message || 'Please correct the form.'
                        : response.status === 403
                            ? data.message || 'You do not have permission to add a project.'
                            : 'Terjadi kesalahan pada sistem. Silakan coba lagi.';
                    errors.textContent = message;
                    errors.focus();
                    showToast(message, 'error');
                    return;
                }
                if (response.status !== 201) throw new Error('Terjadi kesalahan pada sistem. Silakan coba lagi.');
                form.reset();
                modal.close();
                clearTimeout(debounceTimer);
                search.value = '';
                showToast(data.message || 'Project created successfully!', 'success');
                await loadProjects(data.id);
            } catch (error) {
                const message = 'Terjadi kesalahan pada sistem. Silakan coba lagi.';
                errors.textContent = message;
                showToast(message, 'error');
            } finally { submit.disabled = false; }
        });
    }
    loadProjects();
};

document.addEventListener('DOMContentLoaded', initializeProjects);
