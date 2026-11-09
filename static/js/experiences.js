(() => {
    const section = document.getElementById('experiences');
    const list = document.getElementById('experience-list');
    if (!section || !list) return;
    const search = document.getElementById('experience-search');
    const modal = document.getElementById('experience-modal');
    const form = document.getElementById('experience-form');
    const detailPattern = section.dataset.experienceDetailUrl;
    let current = [];
    let timer;

    const csrf = () => document.cookie.split(';').map(x => x.trim()).find(x => x.startsWith('csrftoken='))?.split('=').slice(1).join('=') || form?.elements.csrfmiddlewaretoken.value || '';
    const detailUrl = id => detailPattern.replace('00000000-0000-0000-0000-000000000000', encodeURIComponent(id));
    const toast = (message, type = 'error') => window.showToast?.(message, type);
    const apiMessage = async response => {
        let data = {}; try { data = await response.json(); } catch {}
        if (response.status === 400) return Object.entries(data).flatMap(([key, val]) => (Array.isArray(val) ? val : [val]).map(v => `${key}: ${typeof v === 'string' ? v : v.message || 'Invalid value.'}`)).join('\n') || 'Please check the submitted values.';
        if (response.status === 403) return data.detail || 'You do not have permission to make this change.';
        return data.detail || 'Request failed. Please try again.';
    };
    const renderMessage = message => { const p = document.createElement('p'); p.className = 'role'; p.textContent = message; list.replaceChildren(p); };
    const render = exp => {
        const group = document.createElement('article'); group.className = 'exp-group';
        const row = document.createElement('div'); row.className = 'exp-row';
        const title = document.createElement('span'); title.className = 'organization'; title.textContent = exp.title;
        const date = document.createElement('span'); date.className = 'date'; date.textContent = `${exp.started_at} - ${exp.ended_at || 'Present'}`;
        row.append(title, date);
        const roleRow = document.createElement('div'); roleRow.className = 'role-row';
        const role = document.createElement('p'); role.className = 'role'; role.textContent = `${exp.organization ? `${exp.organization} · ` : ''}${exp.category_display}`; roleRow.append(role);
        const descriptionRow = document.createElement('div'); descriptionRow.className = 'description-row';
        const description = document.createElement('p'); description.className = 'description'; description.textContent = exp.description; descriptionRow.append(description);
        group.append(row, roleRow, descriptionRow);
        if (section.dataset.canEdit === 'true') {
            const actions = document.createElement('div'); actions.className = 'experience-actions';
            const edit = document.createElement('button'); edit.type = 'button'; edit.className = 'btn btn-sm'; edit.textContent = 'Edit'; edit.addEventListener('click', () => openEdit(exp)); actions.append(edit);
            if (section.dataset.canDelete === 'true') { const del = document.createElement('button'); del.type = 'button'; del.className = 'btn btn-sm'; del.textContent = 'Delete'; del.addEventListener('click', () => remove(exp)); actions.append(del); }
            group.append(actions);
        }
        return group;
    };
    const load = async () => {
        list.setAttribute('aria-busy', 'true');
        try {
            const url = new URL(section.dataset.experiencesUrl, location.origin); if (search.value.trim()) url.searchParams.set('q', search.value.trim());
            const response = await fetch(url, { credentials: 'same-origin' }); if (!response.ok) throw new Error(await apiMessage(response));
            current = await response.json(); list.replaceChildren(...(current.length ? current.map(render) : [])); if (!current.length) renderMessage('No experience found.');
        } catch (error) { renderMessage(error.message || 'Unable to load experiences.'); toast(error.message); }
        finally { list.setAttribute('aria-busy', 'false'); }
    };
    const openEdit = exp => { if (!form || !modal) return; form.dataset.id = exp.id; form.elements.title.value = exp.title; form.elements.organization.value = exp.organization; form.elements.description.value = exp.description; form.elements.category.value = exp.category; form.elements.thumbnail.value = exp.thumbnail || ''; form.elements.started_at.value = exp.started_at; form.elements.ended_at.value = exp.ended_at || ''; document.getElementById('experience-modal-title').textContent = 'Edit experience'; modal.showModal(); };
    const remove = async exp => { if (!confirm(`Delete “${exp.title}”?`)) return; try { const response = await fetch(detailUrl(exp.id), { method: 'DELETE', credentials: 'same-origin', headers: { 'X-CSRFToken': decodeURIComponent(csrf()) } }); if (!response.ok) throw new Error(await apiMessage(response)); toast('Experience deleted.', 'success'); await load(); } catch (error) { toast(error.message); } };
    search?.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(load, 300); });
    document.getElementById('add-experience')?.addEventListener('click', () => { form.reset(); delete form.dataset.id; document.getElementById('experience-modal-title').textContent = 'Add experience'; modal.showModal(); });
    document.getElementById('close-experience-modal')?.addEventListener('click', () => modal.close());
    form?.addEventListener('submit', async event => {
        event.preventDefault(); const payload = Object.fromEntries(new FormData(form)); if (!payload.ended_at) payload.ended_at = null; if (!payload.thumbnail) payload.thumbnail = null;
        const id = form.dataset.id; const url = id ? detailUrl(id) : section.dataset.experiencesUrl;
        try { const response = await fetch(url, { method: id ? 'PATCH' : 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': decodeURIComponent(csrf()) }, body: JSON.stringify(payload) }); if (!response.ok) throw new Error(await apiMessage(response)); toast(id ? 'Experience updated.' : 'Experience added.', 'success'); modal.close(); await load(); }
        catch (error) { toast(error.message); }
    });
    load();
})();
