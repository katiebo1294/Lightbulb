// const slider = document.querySelector('.items');
// let isDown = false;
// let startX;
// let scrollLeft;

// slider.addEventListener('mousedown', (e) => {
//   isDown = true;
//   slider.classList.add('active');
//   startX = e.pageX - slider.offsetLeft;
//   scrollLeft = slider.scrollLeft;
// });
// slider.addEventListener('mouseleave', () => {
//   isDown = false;
//   slider.classList.remove('active');
// });
// slider.addEventListener('mouseup', () => {
//   isDown = false;
//   slider.classList.remove('active');
// });
// slider.addEventListener('mousemove', (e) => {
//   if(!isDown) return;
//   e.preventDefault();
//   const x = e.pageX - slider.offsetLeft;
//   const walk = (x - startX) * 3; //scroll-fast
//   slider.scrollLeft = scrollLeft - walk;
//   console.log(walk);
// });

// Modified version of code from this site: https://css-tricks.com/draggable-elements-push-others-way/

// $(".items").sortable({
//  placeholder: 'item-placeholder',
//  axis: "y",
//  revert: 150,
//  start: function(e, ui){
     
//      placeholderHeight = ui.item.outerHeight();
//      ui.placeholder.height(placeholderHeight + 15);
//      $('<div class="item-placeholder-animator" data-height="' + placeholderHeight + '"></div>').insertAfter(ui.placeholder);
 
//  },
//  change: function(event, ui) {
     
//      ui.placeholder.stop().height(0).animate({
//          height: ui.item.outerHeight() + 15
//      }, 300);
     
//      placeholderAnimatorHeight = parseInt($(".item2-placeholder-animator").attr("data-height"));
     
//      $(".item2-placeholder-animator").stop().height(placeholderAnimatorHeight + 15).animate({
//          height: 0
//      }, 300, function() {
//          $(this).remove();
//          placeholderHeight = ui.item.outerHeight();
//          $('<div class="item-placeholder-animator" data-height="' + placeholderHeight + '"></div>').insertAfter(ui.placeholder);
//      });
     
//  },
//  stop: function(e, ui) {
     
//      $(".item-placeholder-animator").remove();
     
//  },
// });

$(".slide").each(function(i) {
  var item = $(this);
  var item_clone = item.clone();
  item.data("clone", item_clone);
  var position = item.position();
  item_clone
  .css({
    left: position.left,
    top: position.top,
    visibility: "hidden"
  })
    .attr("data-pos", i+1);
  
  $("#cloned-slides").append(item_clone);
});

$(".all-slides").sortable({
  
  axis: "y",
  revert: true,
  scroll: false,
  placeholder: "sortable-placeholder",
  cursor: "move",

  start: function(e, ui) {
    ui.helper.addClass("exclude-me");
    $(".all-slides .slide:not(.exclude-me)")
      .css("visibility", "hidden");
    ui.helper.data("clone").hide();
    $(".cloned-slides .slide").css("visibility", "visible");
  },

  stop: function(e, ui) {
    $(".all-slides .slide.exclude-me").each(function() {
      var item = $(this);
      var clone = item.data("clone");
      var position = item.position();

      clone.css("left", position.left);
      clone.css("top", position.top);
      clone.show();

      item.removeClass("exclude-me");
    });
    
    $(".all-slides .slide").each(function() {
      var item = $(this);
      var clone = item.data("clone");
      
      clone.attr("data-pos", item.index());
    });

    $(".all-slides .slide").css("visibility", "visible");
    $(".cloned-slides .slide").css("visibility", "hidden");
  },

  change: function(e, ui) {
    $(".all-slides .slide:not(.exclude-me)").each(function() {
      var item = $(this);
      var clone = item.data("clone");
      clone.stop(true, false);
      var position = item.position();
      clone.animate({
        left: position.left,
        top: position.top
      }, 200);
    });
  }
  
});