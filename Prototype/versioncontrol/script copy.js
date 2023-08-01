document.getElementById("search-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const keyword = document.getElementById("keyword").value;
  const count = 10; // You can set the desired count here

  const data = { keyword, count };

  fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Received data:", data);
      // Handle the received data here and update the results page accordingly
      // Assuming you stored the search results in a variable called 'results'
      localStorage.setItem('searchResults', JSON.stringify(data));
      window.location.href = '/results'; // Redirect to the results.html page
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      // Handle errors here, e.g., display an error message on the results page
    });
});




// Code to load results on the results.html page
if (window.location.pathname.endsWith('/results')) {
    const results = JSON.parse(localStorage.getItem('searchResults') || '[]');
    console.log("Results:", results); // Check if the results are retrieved correctly
    const resultsDiv = document.getElementById('results');
    results.forEach(result => {
        resultsDiv.innerHTML += `<div>
            <p>Keyword: ${result.keyword}</p>
            <p>URL: <a href="${result.url}" target="_blank">${result.url}</a></p>
            <p>Timestamp: ${result.timestamp}</p>
            <p>Last Published Date: ${result.last_published_date}</p>
        </div>`;
    });
}
