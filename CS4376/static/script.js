document.getElementById("search-form").addEventListener("submit", function (event) {
    event.preventDefault();
  
    const keyword = document.getElementById("keyword").value;
    const count = 10; // You can set the desired count here
  
    const data = { keyword, count };
  
    // Save the current search keyword and count to local storage
    localStorage.setItem('currentSearch', JSON.stringify({ keyword, count }));
  
    fetchSearchResults(keyword, count, 1); // Fetch results for page 1
  });
  
  // Function to fetch search results for a given page
  function fetchSearchResults(keyword, count, page) {
    const data = { keyword, count, page };
  
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
  