// Function to toggle the theme
function toggleTheme() {
    var darkTheme = document.getElementById('darkTheme');
    if (darkTheme.disabled) {
      darkTheme.disabled = false;
      localStorage.setItem('theme', 'dark');
    } else {
      darkTheme.disabled = true;
      localStorage.setItem('theme', 'light');
    }
  }
  
  // Set the initial theme based on localStorage
  window.onload = function() {
    var darkTheme = document.getElementById('darkTheme');
    var theme = localStorage.getItem('theme');
    if (theme === 'dark') {
      darkTheme.disabled = false;
      document.querySelector('.card').classList.add('is-flipped');
    } else {
      darkTheme.disabled = true;
    }
  
    // Add event listener to the toggle button
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
  
    // Flip animation
    var card = document.querySelector('.card');
    card.addEventListener('click', function() {
      card.classList.toggle('is-flipped');
    });
  };
  