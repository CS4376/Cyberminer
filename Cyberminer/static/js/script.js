/* When the user clicks on the gear icon, toggle between hiding and showing the dropdown content */
function settingsMenu() {
  var settingsDropdown = document.getElementById("settings-dropdown");
  settingsDropdown.classList.toggle("show");
}

// Close the settings menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.fa-gear')) {
    var settingsDropdown = document.getElementById("settings-dropdown");
    if (settingsDropdown.classList.contains('show')) {
      settingsDropdown.classList.remove('show');
    }
  }
};

/* Function to execute the search *//* Function to execute the search */
function executeSearch() {
  const keyword = document.getElementById("search-input").value;
  /* Redirect to results.html with the search query as a parameter */
  window.location.href = `/results?keyword=${encodeURIComponent(keyword)}`;
}

/* Within the main function */
function main() {
  document.getElementById("search-icon").addEventListener("click", executeSearch);
}
  
  class GoogleSearcher {
    constructor() {
      this.count = null;
      this.keyword = null;
      this.results = null;
    }
  
    getResultCount() {
      const resultCount = document.getElementById("result-count").value;
      return parseInt(resultCount);
    }
  
    displaySearches() {
      this.count = this.getResultCount();
    }
  
    executeSearch() {
      this.keyword = document.getElementById("search-input").value;
      try {
        /* Simulating search function as it's not available in JavaScript */
        const results = [
          "https://example.com/result1",
          "https://example.com/result2",
          "https://example.com/result3",
          /* ... add more results here */
        ];
        this.results = results;
      } catch (e) {
        console.error(e);
        console.log("Google Search faced an Exception.");
      }
      console.log("\nGoogle Search performed successfully.");
    }
  
    showSearchResults() {
      const resultList = document.createElement("ul");
      results.forEach((result) => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = result;
        link.textContent = result;
        listItem.appendChild(link);
        resultList.appendChild(listItem);
      });
    }
  }
  
  /* Call the main function */
  main();