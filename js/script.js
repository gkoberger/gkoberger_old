$(function(){
    if($('#detect_mobile').is(':hidden') || location.hash == "#mobile") {
        $('body').addClass('mobile');
    } else {
        $('body').addClass('screen');
    }

    if(typeof initBoth == 'function') {
      initBoth();
    }

    if($('body').hasClass('mobile')) {
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

    /* for testing */
    if(location.hash == "#mobile") {
        $('head').append($('<link rel="stylesheet" href="/css/mobile.css">'));
    }

    /*
    $('.parallax').each(function(){
        $(this).children().parallax();
    });
    */

    $('.parallax').append("<div class='parallax_front'></div>");
});


function initNotepad() {
    var articles = $('.note'),
        smoothScroll = false,
        window_top = 0;

    $(document).scroll(function(){
        window_top = $(window).scrollTop();
        articles.trigger('page-scroll', [window_top]);
    });

    $('.note').each(function() {
        var isScrolled = false,
            $sidebar = $(this).find('.sidebar'),
            sidebar_top = $sidebar.offset()['top'],
            $sidebar_scroll = $sidebar.find('.sidebar_scroll'),
            $text = $(this).find('.text'),
            $title = $sidebar.find('.sidebar_title'),
            sidebar_height = $sidebar_scroll.outerHeight(),
            text_height = $text.outerHeight(),
            timeout = false,
            title_height = $title.height();

        //$title.hide();

        $(this).bind("page-scroll", function(e, window_top){
            if(sidebar_top < window_top || sidebar_top - window_top > 0) {
                sidebar_top = $sidebar.offset()['top']; // Ugh, typekit's fault
                var newscroll = window_top - sidebar_top;

                if((newscroll + sidebar_height) > text_height) {
                    // Below the article
                    if(! (!isScrolled && smoothScroll)) {
                      clearTimeout(timeout);
                      $sidebar_scroll.stop().css({'position': 'absolute', 'top': text_height - sidebar_height });
                      //$title.show();
                      isScrolled = true;
                    }
                } else {
                    if(newscroll < 0) {
                        // Above the article
                        isScrolled = false;
                        newscroll = 0;
                        clearTimeout(timeout);
                        $sidebar_scroll.stop().css({'position': 'relative', 'top': 0});
                        //$title.hide();
                    } else {
                        // On the article
                        if(! isScrolled) {
                            clearTimeout(timeout);
                            //$sidebar_scroll.css({'position': 'absolute', 'top': title_height * -1});
                            //$title.show();
                            timeout = setTimeout(function(){
                                isScrolled = true;
                                $sidebar_scroll.animate({'top': newscroll}, function(){
                                    $sidebar_scroll.css({'position': 'fixed', 'top': 0});
                                });
                            }, 550);
                        } else {
                            $sidebar_scroll.stop().css({'position': 'fixed', 'top': 0});
                        }
                    }
                }
            }
        });
    });

    $('.nav_next').click(function(){
        smoothScroll = true;
          articles.trigger('page-scroll', [window_top]);
        next = $(this).closest('.note').next();
        if(next.length) {
          var hash = next.find('.title a').attr('href').match(/(.*)#(.*)/)[2]
          $('html').animate({scrollTop: next.offset()['top'] },'slow', function() {
              smoothScroll = false;
              articles.trigger('page-scroll', [window_top]);
              location.hash = hash;
          });
        }
        return false;
    });

    $('.nav_prev').click(function(){
        smoothScroll = true;
        prev = $(this).closest('.note').next();
        if(prev.length) {
          var hash = prev.find('.title a').attr('href').match(/(.*)#(.*)/)[2]
          $('html').animate({scrollTop: prev.offset()['top'] },'slow', function() {
              smoothScroll = false;
              articles.trigger('page-scroll', [window_top]);
              location.hash = hash;
          });
        }
        return false;
    });

    $('.nav_top').click(function(){
        smoothScroll = true;
        $('html').animate({scrollTop: 0} ,'slow', function() {
            smoothScroll = false;
            articles.trigger('page-scroll', [window_top]);
        });

        return false;
        });

  // TODO: Optimize this!!
    /*
  function scrollSidebar(instant){
    var window_top = $(window).scrollTop();

    instant = (instant == true);

    $('.note').each(function(){
        if(sidebar_top < window_top || sidebar_top > 0) {
        var newscroll = window_top - sidebar_top,
            sidebar_height = $sidebar_scroll.outerHeight(),
            $text = $(this).find('.text'),
            text_height = $text.outerHeight(),
            $title = $sidebar.find('.title');

        if((newscroll + sidebar_height) > text_height) {
          // Below the article
          $sidebar_scroll.css({'position': 'absolute', 'top': text_height - sidebar_height });
          $title.css({'visibility': 'visible'});
        } else {
          if(newscroll < 0) {
            // Above the article
              console.log(1);
            newscroll = 0;
            $sidebar_scroll.css({'position': 'relative', 'top': 0});
            $title.css({'visibility': 'hidden'});
          } else {
            // On the article
            $sidebar_scroll.css({'position': 'fixed', 'top': 0});
            $title.css({'visibility': 'visible'});
          }
        }
      }
    });
 }
*/

  //scrollSidebar(true);
  //$(document).scroll(scrollSidebar);
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

