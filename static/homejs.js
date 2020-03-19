document.addEventListener("DOMContentLoaded", function(){
  let start_index = 0;
  let stop_index = 9;
  let book_start = 0;
  book_stop = book_start + 17;
  let max_val = parseInt(document.querySelector(".page-navigate").getAttribute("data-total"));
  display_item(start_index, stop_index, "pn-item");
  // display_item(book_start, book_stop, "book");

  let btn_prev = document.querySelector(".pn-btn-prev");
  let btn_forw = document.querySelector(".pn-btn-forw");
  btn_forw.addEventListener("click", function() {
    if (stop_index <= max_val) {
      display_item(start_index, stop_index, "pn-item");
      start_index += 10;
      stop_index += 10;
      display_item(start_index, stop_index, "pn-item");
    }
  });
  btn_prev.addEventListener("click", function() {
    if (stop_index >= 10) {
      display_item(start_index, stop_index, "pn-item");
      start_index -= 10;
      stop_index -= 10;
      display_item(start_index, stop_index, "pn-item");
    }
  });

  let btns = document.querySelectorAll(".pn-link");
  btns.forEach(function(btn){
    btn.addEventListener("click", function(e) {
      if (book_stop < max_val*18) {
        console.log(e);
        display_item(book_start, book_stop, "book");
        book_start = parseInt(e.target.getAttribute("data-btn"))*18;
        console.log(book_start)
        book_stop = book_start + 17;
        console.log(book_stop)
        display_item(book_start, book_stop, "book");
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
});

function display_item(start_index, stop_index, class_name) {
  let objs = document.querySelectorAll("." + class_name);
  objs.forEach(function(item, index) {
    if (index >= start_index && index <= stop_index) {
      item.classList.toggle("displayed");
    }
    else {
      item.classList.toggle("display-none");
    }
  }); 
}