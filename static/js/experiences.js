(() => {
    const section = document.getElementById('experiences');
    const list = document.getElementById('experience-list');
    if (!section || !list) return;

    const renderMessage = message => {
        const item = document.createElement('div');
        item.className = 'exp-group';
        const text = document.createElement('p');
        text.className = 'role';
        text.textContent = message;
        item.append(text);
        list.replaceChildren(item);
        list.setAttribute('aria-busy', 'false');
    };

    const renderExperience = experience => {
        const group = document.createElement('article');
        group.className = 'exp-group';

        const row = document.createElement('div');
        row.className = 'exp-row';
        const title = document.createElement('span');
        title.className = 'organization';
        title.textContent = experience.title;
        const date = document.createElement('span');
        date.className = 'date';
        date.textContent = `${experience.started_at} - ${experience.ended_at || 'Present'}`;
        row.append(title, date);

        const roleRow = document.createElement('div');
        roleRow.className = 'role-row';
        const role = document.createElement('p');
        role.className = 'role';
        role.textContent = experience.category;
        roleRow.append(role);

        const descriptionRow = document.createElement('div');
        descriptionRow.className = 'description-row';
        const description = document.createElement('p');
        description.className = 'description';
        description.textContent = experience.description;
        descriptionRow.append(description);

        group.append(row, roleRow, descriptionRow);
        return group;
    };

    fetch(section.dataset.experiencesUrl, { credentials: 'same-origin' })
        .then(response => {
            if (!response.ok) throw new Error('Unable to load experiences.');
            return response.json();
        })
        .then(experiences => {
            if (!Array.isArray(experiences)) throw new Error('Invalid experiences response.');
            if (!experiences.length) {
                renderMessage('No experience found.');
                return;
            }
            list.replaceChildren(...experiences.map(renderExperience));
            list.setAttribute('aria-busy', 'false');
        })
        .catch(() => renderMessage('Unable to load experiences. Please try again later.'));
})();
