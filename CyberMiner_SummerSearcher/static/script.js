document.getElementById("search-form").addEventListener("submit", function (event) {
  event.preventDefault();
  
  const keyword = document.getElementById("keyword").value;
  const count = document.getElementById("per_page").value; // You can set the desired count here
  const sortOrder = document.getElementById("sort").value;
  const minYear = Number(document.getElementById("min_year").value);
  const expiryDate = document.getElementById("expiry_date").value;
  const allResults = document.getElementById("all_results").checked;
  const resultsPerPage = document.getElementById("results_per_page").value;
  localStorage.setItem("resultsPerPage", resultsPerPage);
  // Get the selected Boolean search mode
  const searchMode = document.querySelector('input[name="search-mode"]:checked').value;

  // Include the search mode in the data sent to the server
  const data = { keyword, count, min_year: minYear, expiry_date: expiryDate, all_results: allResults, search_mode: searchMode };

  // Save the current search keyword and count to local storage
  localStorage.setItem('currentSearch', JSON.stringify({ keyword, count, min_year: minYear, expiry_date: expiryDate, all_results: allResults, sortOrder})); // include sortOrder
  fetchSearchResults(keyword, count, minYear, expiryDate, allResults, sortOrder, searchMode, 1);
});

// Function to fetch search results for a given page
// ...

function fetchSearchResults(keyword, count, minYear, expiryDate, allResults, sortOrder, searchMode, page) {
  const data = { keyword, count, min_year: minYear, expiry_date: expiryDate, all_results: allResults, sortOrder, searchMode, page };

// ...


  

  fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      localStorage.setItem('searchResults', JSON.stringify(data));
      localStorage.setItem('currentPage', '1');
      window.location.href = '/results'; // Redirect to the results.html page
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      // Handle errors here, e.g., display an error message on the results page
    });
}

// Code to load results on the results.html page
if (window.location.pathname.endsWith('/results')) {
  const results = JSON.parse(localStorage.getItem('searchResults') || '[]');
  const { keyword, count } = JSON.parse(localStorage.getItem('currentSearch') || '{}');
  const resultsDiv = document.getElementById('results');
  results.forEach(result => {
    resultsDiv.innerHTML += `<div>
        <p>Keyword: ${result.keyword}</p>
        <p>Title: ${result.title}</p>
        <p>URL: <a href="${result.url}" target="_blank">${result.url}</a></p>
        <p>Timestamp: ${result.timestamp}</p>
        <p>Last Published Date: ${result.last_published_date}</p>
    </div>`;
  });

  // Add pagination controls
  const paginationDiv = document.getElementById('pagination');
  for (let page = 1; page <= 10; page++) { // Assuming max 10 pages
    const pageLink = document.createElement('a');
    pageLink.textContent = page;
    pageLink.href = '#';
    pageLink.addEventListener('click', (e) => {
      e.preventDefault();
      fetchSearchResults(keyword, count, page); // Fetch results for the clicked page
    });
    paginationDiv.appendChild(pageLink);
  }
}