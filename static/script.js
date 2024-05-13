document.addEventListener("DOMContentLoaded", function() {
    const menuItems = document.querySelectorAll('.menu-item');
  
    menuItems.forEach(item => {
      const icon = item.querySelector('.menu-icon');
      const subMenu = item.querySelector('.sub-menu');
      let isImageSwapped = false;
      let isSubMenuVisible = false;
  

      function swapImage() {
        if (isImageSwapped) {
          icon.src = 'Assets/arrow.png';
        } else {
          icon.src = 'Assets/arrowdown.png';
        }
        isImageSwapped = !isImageSwapped;
      }
  
      function toggleSubMenu() {
        if (isSubMenuVisible) {
          subMenu.style.display = 'none';
        } else {
          subMenu.style.display = 'block';
        }
        isSubMenuVisible = !isSubMenuVisible;
      }
  
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        swapImage();
        toggleSubMenu();
      });
  

      icon.addEventListener('click', function(event) {
        event.stopPropagation();
        swapImage();
        toggleSubMenu();
      });
    });
  });