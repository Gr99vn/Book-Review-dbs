document.addEventListener("DOMContentLoaded", function(){
  let stars = document.querySelectorAll('.ustar');
  stars.forEach(function(star) {
    star.addEventListener('click', setRating);
  });

  let rating = parseInt(document.querySelector(".rating").getAttribute("data-rating"));
  if (rating > 0) {
    let target = stars[rating-1];
    target.dispatchEvent(new MouseEvent('click'));
  }
});

function setRating(e) {
  let span = e.currentTarget;
  let stars = document.querySelectorAll('.ustar');
  let match = false;
  let num = 0;
  stars.forEach(function(star, index){
    if (match) {
      star.classList.remove("rated");
    }
    else {
      star.classList.add("rated");
    }
    if (span == star) {
      match = true;
      num = index;
    }
    document.querySelector(".rating").setAttribute("data-rating", num)
  });

}