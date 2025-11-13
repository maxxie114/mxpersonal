document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('content');
    const routes = {
        '#home': 'home.html',
        '#about': 'about.html',
        '#projects': 'projects.html',
        '#publications': 'publications.html',
        '#resume': 'resume.html',
        '#contact': 'contact.html'
    };

    function loadContent() {
        const hash = window.location.hash || '#home';
        const url = routes[hash];

        if (url) {
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    content.innerHTML = data;
                })
                .catch(error => {
                    console.error('Error loading content:', error);
                    content.innerHTML = '<p>Error loading content. Please try again later.</p>';
                });
        } else {
            content.innerHTML = '<p>Page not found.</p>';
        }
    }

    window.addEventListener('hashchange', loadContent);
    loadContent(); // Load initial content
});