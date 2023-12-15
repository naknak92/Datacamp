document.getElementById('uploadForm').addEventListener('submit', function(event){
    event.preventDefault();
    const file = document.getElementById('fileInput').files[0];
    const formData = new FormData();
formData.append('csvFile', file);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        // Afficher un message d'erreur à l'utilisateur ici si nécessaire
    });
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    Object.entries(data).forEach(([role, champions]) => {
        const roleDiv = document.createElement('div');
        roleDiv.innerHTML = `<h2>${role}</h2>`;
        champions.forEach(champion => {
            const championDiv = document.createElement('div');

            const img = document.createElement('img');
            img.src = `Projet Datacamp/tiles/${champion.Name}.jpg`; // Assurez-vous que le chemin est correct
            img.alt = champion.Name;

            const name = document.createElement('p');
            name.textContent = champion.Name;

            championDiv.appendChild(img);
            championDiv.appendChild(name);
            roleDiv.appendChild(championDiv);
        });
        resultsDiv.appendChild(roleDiv);
    });
}
