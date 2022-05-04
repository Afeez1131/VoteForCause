"https://www.facebook.com/sharer/sharer.php?u=";

function shareOnFacebook(){
  const navUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + 'https://github.com/knoldus/angular-facebook-twitter.git';
  window.open(navUrl , '_blank');
}
const fb = document.getElementById('fb');
fb.addEventListener('click', shareonFacebook);