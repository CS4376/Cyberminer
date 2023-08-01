// Global variables to store the settings
let searchMode = "";
let resultsPerPage = Number(localStorage.getItem('resultsPerPage') || '10');;
let minYear = "";
let caseSensitive = "";
let sortBy = "";
let expiryDate = "";
let includePastResults = "";

/* When the user clicks on the gear icon, toggle between hiding and showing the dropdown content */
function toggleSettingsDropdown() {
  var settingsDropdown = document.getElementById("settings-dropdown");
  settingsDropdown.classList.toggle("show");
}

function settingsMenu() {
  toggleSettingsDropdown();
}

/* Close the settings menu if the user clicks outside of it */
window.onclick = function (event) {
  const clickedElement = event.target;
  const settingsDropdown = document.getElementById("settings-dropdown");
  const gearIcon = document.querySelector(".fa-gear");

  if (clickedElement !== gearIcon && !settingsDropdown.contains(clickedElement)) {
    settingsDropdown.classList.remove("show");
  }
};

// Attach the event listener to the search-icon class
document.querySelector(".search-icon").addEventListener("click", () => {
  event.preventDefault(); // Prevent form submission
  executeSearch();
});

function executeSearch() {
  const keyword = document.getElementById("keyword").value;
  const searchMode = document.querySelector('input[name="search-mode"]:checked').value;
  const minYear = document.getElementById("min_year").value;
  const caseSensitive = document.getElementById("case").value;
  const sortBy = document.getElementById("sort").value;
  const expiryDate = document.getElementById("expiry_date").value;
  const includePastResults = document.getElementById("all_results").checked;

  // Include the settings in the data sent to the server
  const data = {
    keyword,
    count: resultsPerPage,
    min_year: minYear,
    expiry_date: expiryDate,
    all_results: includePastResults,
    sort_order: "asc",
    search_mode: searchMode,
    page: 1,
  };

  // Save the search data in localStorage
  localStorage.setItem('searchData', JSON.stringify(data));

  console.log(data); // Add this line to check the 'data' object

  fetchSearchResults(data);
  window.location.href = `/results?fromSearch=true`;
}

// Save the settings to local storage
function saveSettings() {
  const searchMode = document.querySelector('input[name="search-mode"]:checked').value;
  const resultsPerPage = document.getElementById("results_per_page").value;
  const minYear = document.getElementById("min_year").value;
  const caseSensitive = document.getElementById("case").value;
  const sortBy = document.getElementById("sort").value;
  const expiryDate = document.getElementById("expiry_date").value;
  const includePastResults = document.getElementById("all_results").checked;

  const settings = {
    searchMode,
    resultsPerPage,
    minYear,
    caseSensitive,
    sortBy,
    expiryDate,
    includePastResults,
  };

  localStorage.setItem("searchSettings", JSON.stringify(settings));
};

function fetchSearchResults(data) {
  // Send the data to the server
  fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      // Save the search results in local storage
      localStorage.setItem("searchResults", JSON.stringify(data));

      // Redirect to the results.html page
      window.location.href = "/results";
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      // Handle errors here, e.g., display an error message on the index page
    });
}