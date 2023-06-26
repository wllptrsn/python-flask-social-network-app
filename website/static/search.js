let searchType = 1;
const searchInput = document.getElementById("search-input");
function searchFor(searching, active, inactive1, inactive2) {
  searchType = searching;
  document.getElementById(active).classList.add("active");
  document.getElementById(inactive1).classList.remove("active");
  document.getElementById(inactive2).classList.remove("active");
  searchInput.dispatchEvent(new Event("input"));
}
fetch("/searchFor")
  .then((response) => response.json())
  .then((data) => {
    const profiles = data["profiles"];
    const posts = data["posts"];
    const groups = data["groups"];
    const usersList = document.getElementById("users-list");
    searchInput.addEventListener("input", () => {
      const searchTerm = searchInput.value.toLowerCase();
      const filteredProfiles = profiles.filter((profile) =>
        profile[1].toLowerCase().includes(searchTerm)
      );
      const filteredPosts = posts.filter((post) =>
        post[1].toLowerCase().includes(searchTerm)
      );
      const filteredGroups = groups.filter((group) =>
        group[1].toLowerCase().includes(searchTerm)
      );
      if (searchType == 1) {
        renderList(filteredProfiles);
      } else if (searchType == 2) {
        renderList(filteredPosts);
      } else if (searchType == 3) {
        renderList(filteredGroups);
      }
      function renderList(filteredItem) {
        usersList.innerHTML = "";
        filteredItem.forEach((searchItem) => {
          const listItem = document.createElement("li");
          listItem.textContent = searchItem[1];
          usersList.appendChild(listItem);
        });
      }
    });
  });
