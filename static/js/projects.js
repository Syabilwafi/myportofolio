const initializeProjects = () => {
    const sidebar = document.getElementById('project-sidebar');
    const display = document.getElementById('project-display');
    const search = document.getElementById('search-input');
    const star = document.getElementById('star-btn');
    const modal = document.getElementById('project-modal');
    const form = document.getElementById('project-create-form');
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

    const updateDisplay = item => {
        current = item;
        const fields = item.fields;
        document.getElementById('active-project-title').textContent = fields.name;
        document.getElementById('active-project-desc').textContent = fields.description;
        const link = document.getElementById('active-project-link');
        const frame = document.getElementById('active-project-frame');
        const url = safeUrl(fields.url);
        if (url) link.href = url;
        else link.removeAttribute('href');
        frame.src = url || 'about:blank';
        frame.title = fields.name;
        document.getElementById('star-count').textContent = fields.star_count ?? fields.stars_count;
        star.classList.toggle('is-starred', fields.is_starred);
        star.setAttribute('aria-pressed', String(fields.is_starred));
        ['edit-btn', 'delete-btn'].forEach(id => {
            const button = document.getElementById(id);
            if (button) button.style.display = 'flex';
        });
    };

    const loadProjects = async (preferredId = current?.pk) => {
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
            const selected = projects.find(item => item.pk === preferredId) || projects[0];
            projects.forEach(item => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'project-tab-btn';

                button.textContent = `> ${item.fields.name}`;
                button.classList.toggle('active', item.pk === selected.pk);
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
    window.editProject = () => { if (current) location.assign(current.update_url); };
    window.deleteProject = () => { if (current) location.assign(current.delete_url); };

    if (!star.classList.contains('login-required')) {
        star.addEventListener('click', async () => {
            const item = current;
            if (!item || star.disabled) return;
            star.disabled = true;
            try {
                const response = await fetch(item.star_url, {
                    method: 'POST', credentials: 'same-origin',
                    headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
                });
                if (!response.ok || response.redirected) throw new Error('Unable to star project. Check your login and try again.');
                const data = await response.json();
                Object.assign(item.fields, data);
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
                    headers: { 'X-CSRFToken': form.elements.csrfmiddlewaretoken.value }
                });
                if (!response.headers.get('content-type')?.includes('application/json')) {
                    throw new Error('Request rejected. Reload the page to renew your session and try again.');
                }
                const data = await response.json();
                if (!response.ok) {
                    errors.textContent = Object.entries(data.errors || {}).flatMap(([field, items]) =>
                        items.map(item => `${field}: ${item.message}`)).join('\n') || data.message;
                    errors.focus();
                    showToast(data.message || 'Project could not be created.', 'error');
                    return;
                }
                form.reset();
                modal.close();
                clearTimeout(debounceTimer);
                search.value = '';
                showToast(data.message);
                await loadProjects(data.id);
            } catch (error) {
                errors.textContent = error.message;
                showToast(error.message, 'error');
            } finally { submit.disabled = false; }
        });
    }
    loadProjects();
};

document.addEventListener('DOMContentLoaded', initializeProjects);
