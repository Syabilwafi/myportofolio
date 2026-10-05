document.addEventListener('DOMContentLoaded', () => {
    const blog = document.querySelector('.blog');
    const postList = document.getElementById('post-list');
    const article = document.querySelector('.post-article');
    const activePost = document.getElementById('active-post');
    const commentArea = document.getElementById('comment-area');
    const windowTitle = document.getElementById('window-title');
    const postDate = document.getElementById('post-date');
    const postText = document.getElementById('post-text');
    const commentPostIdInput = document.getElementById('comment-post-id');
    const commentsContainer = document.getElementById('comments-container');
    const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
    const blogSidebar = document.querySelector('.blog-sidebar');
    const modal = document.getElementById('create-post-modal');
    const openBtn = document.getElementById('open-modal-btn');
    const closeBtn = document.getElementById('close-modal-btn');

    const renderComments = comments => {
        commentsContainer.replaceChildren();
        if (!comments.length) {
            const empty = document.createElement('p');
            empty.className = 'no-comments-text';
            empty.style.cssText = 'color: rgba(181, 245, 66, 0.5); margin-top: 1rem;';
            empty.textContent = 'No comments yet.';
            commentsContainer.append(empty);
            return;
        }

        comments.forEach(comment => {
            const item = document.createElement('div');
            item.className = 'comment-item';
            const author = document.createElement('span');
            author.className = 'comment-author-name';
            author.textContent = comment.username;
            const row = document.createElement('div');
            row.className = 'comment-row';
            const content = document.createElement('span');
            content.className = 'comment-text';
            content.textContent = comment.content;
            const time = document.createElement('span');
            time.className = 'comment-time';
            time.textContent = comment.time;
            row.append(content, time);
            item.append(author, row);
            commentsContainer.append(item);
        });
    };

    const selectPost = post => {
        postList.querySelectorAll('.post-item').forEach(item => item.classList.remove('active'));
        postList.querySelector(`[data-post-id="${post.id}"]`)?.classList.add('active');
        windowTitle.textContent = post.title;
        postDate.textContent = `> Posted on ${post.created_at}`;
        postText.textContent = post.content;
        commentPostIdInput.value = post.id;
        activePost.hidden = false;
        commentArea.hidden = false;
        renderComments(post.comments);
        blogSidebar.classList.remove('show');
    };

    const loadPosts = async () => {
        try {
            const response = await fetch(blog.dataset.postsUrl, { credentials: 'same-origin' });
            if (!response.ok) throw new Error('Unable to load posts. Please try again.');
            const posts = await response.json();
            postList.replaceChildren();
            article.querySelector('.no-posts')?.remove();

            if (!posts.length) {
                const message = document.createElement('p');
                message.className = 'no-posts';
                message.textContent = '> Nothing has been posted yet.';
                article.prepend(message);
                const item = document.createElement('li');
                item.className = 'no-posts-item';
                const empty = document.createElement('p');
                empty.className = 'no-posts';
                empty.textContent = 'Nothing has been posted yet.';
                item.append(empty);
                postList.append(item);
                windowTitle.textContent = 'BLOG';
                activePost.hidden = true;
                commentArea.hidden = true;
                return;
            }

            posts.forEach(post => {
                const item = document.createElement('li');
                item.className = 'post-item';
                item.dataset.postId = post.id;
                const link = document.createElement('a');
                link.href = '#';
                link.className = 'post-tab';
                link.textContent = post.title;
                link.addEventListener('click', event => {
                    event.preventDefault();
                    selectPost(post);
                });
                item.append(link);

                if (postList.dataset.canDelete === 'true') {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = postList.dataset.deleteUrl;
                    form.className = 'delete-form';
                    form.style.display = 'inline';
                    form.onsubmit = () => window.confirm('Are you sure you want to delete this post?');
                    const csrf = document.createElement('input');
                    csrf.type = 'hidden';
                    csrf.name = 'csrfmiddlewaretoken';
                    csrf.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    const postId = document.createElement('input');
                    postId.type = 'hidden';
                    postId.name = 'post_id';
                    postId.value = post.id;
                    const button = document.createElement('button');
                    button.type = 'submit';
                    button.className = 'delete-btn';
                    button.textContent = 'X';
                    form.append(csrf, postId, button);
                    item.append(form);
                }
                postList.append(item);
            });

            selectPost(posts[0]);
        } catch (error) {
            const message = document.createElement('p');
            message.className = 'no-posts';
            message.textContent = 'Unable to load posts. Please try again.';
            article.replaceChildren(message);
            postList.replaceChildren();
            const item = document.createElement('li');
            item.className = 'no-posts-item';
            const sidebarMessage = document.createElement('p');
            sidebarMessage.className = 'no-posts';
            sidebarMessage.textContent = error.message;
            item.append(sidebarMessage);
            postList.append(item);
        } finally {
            article.setAttribute('aria-busy', 'false');
            postList.setAttribute('aria-busy', 'false');
        }
    };

    sidebarToggleBtn?.addEventListener('click', () => blogSidebar?.classList.toggle('show'));
    openBtn?.addEventListener('click', () => {
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
    });
    closeBtn?.addEventListener('click', () => {
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
    });
    window.addEventListener('click', event => {
        if (event.target === modal) {
            modal.classList.add('hidden');
            modal.setAttribute('aria-hidden', 'true');
        }
    });

    loadPosts();
});
