document.addEventListener('DOMContentLoaded', function () {
  const dropdownButton = document.getElementById('profileDropdownButton');
  const dropdownMenu = document.getElementById('profileDropdownMenu');

  if (dropdownButton && dropdownMenu) {
    dropdownButton.addEventListener('click', function (e) {
      e.stopPropagation(); // Mencegah event click bubbling ke body
      dropdownMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', function (e) {
      if (!dropdownMenu.contains(e.target) && !dropdownButton.contains(e.target)) {
        dropdownMenu.classList.add('hidden');
      }
    });
  }
});
