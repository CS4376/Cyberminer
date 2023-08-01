/* When the user clicks on the gear icon, toggle between hiding and showing the dropdown content */
function settingsMenu() {
  var settingsDropdown = document.getElementById("settings-dropdown");
  settingsDropdown.classList.toggle("show");
}

/* Close the settings menu if the user clicks outside of it */
window.onclick = function(event) {
  if (!event.target.matches('.fa-gear')) {
    var settingsDropdown = document.getElementById("settings-dropdown");
    if (settingsDropdown.classList.contains('show')) {
      settingsDropdown.classList.remove('show');
    }
  }
};

function executeSearch() {
  const keyword = document.getElementById("keyword").value;
  const count = document.getElementById("result-count").value;

  // Construct the URL with the query parameters
  const url = `/results?keyword=${encodeURIComponent(keyword)}&count=${encodeURIComponent(count)}`;

  // Redirect to the results page
  window.location.href = url;
}

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
      const resultsDiv = document.getElementById("results");
      resultsDiv.innerHTML = ""; // Clear existing results before adding new ones

      // Display the keyword at the top
      resultsDiv.innerHTML += `<h2>Keyword: ${keyword}</h2>`;

      let counter = 1;
      data.forEach((result) => {
        resultsDiv.innerHTML += `
          <div>
            <h3><a href="${result.url}" target="_blank">${result.url}</a></h3>
            <p>Timestamp: ${result.timestamp}</p>
            <p>Last Published Date: ${result.last_published_date}</p>
          </div>`;
        counter++;
      });
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      // Handle errors here, e.g., display an error message on the results page
    });
}

// Execute the search when the page loads
if (window.location.pathname.endsWith('/results')) {
  // Retrieve the keyword and count from the URL query string
  const urlParams = new URLSearchParams(window.location.search);
  const keyword = urlParams.get("keyword");
  const count = urlParams.get("count");

  // Execute the search when the page loads
  fetchSearchResults(keyword, count, 1);

  // Add event listener for the search-icon to execute the search
  document.getElementById("search-icon").addEventListener("click", () => {
    const keyword = document.getElementById("keyword").value;
    const count = document.getElementById("result-count").value;

    // Fetch and display the search results
    fetchSearchResults(keyword, count, 1);
  });
}