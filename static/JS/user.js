function myFunction(event) {
  // Prevent the event from bubbling up
  event.stopPropagation();

  const dropdownContent = document.getElementById("myDropdown");
  const isVisible = dropdownContent.classList.contains("show");
  
  // Close all dropdowns first
  closeAllDropdowns();

  // Toggle this dropdown
  if (!isVisible) {
      dropdownContent.classList.add("show");
  }
}

function closeAllDropdowns() {
  const dropdowns = document.getElementsByClassName("dropdown-content");
  for (let i = 0; i < dropdowns.length; i++) {
      dropdowns[i].classList.remove("show");
  }
}

// Handle clicks anywhere on the window
window.onclick = function(event) {
  closeAllDropdowns();
};

setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-messages');
    flashMessages.forEach(msg => msg.style.display = 'none');
}, 5000);

function toggleMenu() {
  const navMenu = document.getElementById("navMenu");
  const isOpen = navMenu.style.display === "flex";
  navMenu.style.display = isOpen ? "none" : "flex";

  // Hide the dropdown content if menu is closed
  if (!isOpen) {
      closeDropdown();
  }
}

function toggleDropdown() {
  const dropdownContent = document.getElementById("dropdownContent");
  const isVisible = dropdownContent.classList.contains("show");

  // Close all dropdowns before toggling
  closeDropdown();

  if (!isVisible) {
      dropdownContent.classList.add("show");
  }
}

function closeDropdown() {
  const dropdownContent = document.getElementById("dropdownContent");
  if (dropdownContent) {
      dropdownContent.classList.remove("show");
  }
}

// Ensure all dropdowns are closed when clicking outside
window.onclick = function (event) {
  if (!event.target.matches('.dropbtn')) {
      closeDropdown();
  }
};
