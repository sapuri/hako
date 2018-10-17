function submitWithKeydown() {
    const textarea = document.post_form.body;
    textarea.addEventListener('keydown', e => {
        if (e.keyCode === 13 && e.metaKey) {
            const input = document.createElement('input');
            input.setAttribute('type', 'hidden');
            input.setAttribute('name', 'action');
            input.setAttribute('value', 'save');
            const form = document.forms.post_form;
            form.appendChild(input);
            form.submit();
        }
    });
}

function urlizeResAnchor() {
    Array.from(document.getElementsByClassName("body")).forEach(comment => {
        comment.innerHTML = comment.innerHTML.replace(/&gt;&gt;(\d{1,3})/g, '<a href="./#$1">&gt;&gt;$1</a>');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    submitWithKeydown();
    urlizeResAnchor();
});
