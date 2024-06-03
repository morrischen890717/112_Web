// Function to toggle the theme
function setTheme() {
  var theme = localStorage.getItem('theme');
  var darkThemes = document.querySelectorAll('#darkTheme');
  if(theme === 'dark'){
    darkThemes.forEach(function(darkTheme){
      darkTheme.disabled = false;
    });
  }
  else{
    darkThemes.forEach(function(darkTheme){
      darkTheme.disabled = true;
    });
  }
}

function toggleTheme() {
  var theme = localStorage.getItem('theme');
  var darkThemes = document.querySelectorAll('#darkTheme');
  if (theme === 'dark'){
    localStorage.setItem('theme', 'light');
  }
  else{
    localStorage.setItem('theme', 'dark');
  }
  setTheme();
}
  
// Set the initial theme based on localStorage
window.onload = function() {
  var theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    document.querySelector('.card').classList.add('is-flipped');
  }
  setTheme();
  
  // Add event listener to the toggle button
  document.getElementById('themeToggle').addEventListener('click', toggleTheme);
  
  // Flip animation
  var card = document.querySelector('.card');
  card.addEventListener('click', function() {
    card.classList.toggle('is-flipped');
  });
};
  