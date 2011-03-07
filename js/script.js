$(function(){
    if($('#detect_mobile').is(':hidden')) {
        $('body').addClass('mobile');
    } else {
        $('body').addClass('screen');
    }

    if(typeof initBoth == 'function') {
      initBoth();
    }

    if($('body').hasClass('.mobile')) {
      if(typeof initMobile == 'function') {
        initMobile();
      }
    } else {
      if(typeof initScreen == 'function') {
        initScreen();
      }
    }

    if($('#notebook').length > 0) {
      initNotepad();
    }
});


function initNotepad() {
  // TODO: Optimize this!!
  function scrollSidebar(instant){
    var window_top = $(window).scrollTop();

    instant = (instant == true);

    $('.note').each(function(){
      var $sidebar = $(this).find('.sidebar'),
          sidebar_top = $sidebar.offset()['top'],
          $sidebar_scroll = $sidebar.find('.sidebar_scroll');

      if(sidebar_top < window_top || sidebar_top > 0) {
        var newscroll = window_top - sidebar_top,
            sidebar_height = $sidebar_scroll.outerHeight(),
            $text = $(this).find('.text'),
            text_height = $text.outerHeight(),
            $title = $sidebar.find('.title');

    console.log($title);
    console.log((newscroll + sidebar_height) , text_height);

        if((newscroll + sidebar_height) > text_height) {
          /* Below the article */
          $sidebar_scroll.css({'position': 'absolute', 'top': text_height - sidebar_height });
          $title.css({'visibility': 'visible'});
        } else {
          if(newscroll < 0) {
            /* Above the article */
              console.log(1);
            newscroll = 0;
            $sidebar_scroll.css({'position': 'relative', 'top': 0});
            $title.css({'visibility': 'hidden'});
          } else {
            /* On the article */
            $sidebar_scroll.css({'position': 'fixed', 'top': 0});
            $title.css({'visibility': 'visible'});
          }
        }
      }
    });

  }

  scrollSidebar(true);
  $(document).scroll(scrollSidebar);
}


/* Created by Potch
 * http://potch.me/8/updates_to_truncation_script */

function debounce(fn, ms, ctxt) {
    var ctx = ctxt || window;
    var it, to, del = ms, fun = fn;
    return function () {
        var args = arguments;
        if (!it) {
            it = setInterval(function () {
                fun.apply(ctx, args);
            },del);
        }
        clearTimeout(to);
        to = setTimeout(function() {
            clearInterval(it);
            it = false;
        },del);
    };
}

