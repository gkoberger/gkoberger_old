function initBoth(){
    // Buildings
    // TODO: Don't hardcode 46.
    for(var n=0;n<46;n++) {
        addBuilding($('#clouds_back'), buildings_back)
    }
    for(var n=0;n<46;n++) {
        addBuilding($('#clouds_front'), buildings_front)
    }

    // Add circles to ball.


    for(i = 1; i <= 10; i += 2) {
    console.log((i*i*10) + 'px / ' + (i *100) + 'px');
    $('<div>').appendTo('#nye_ball').css({'left':(100 - i*10), 'border-radius': (i*i*10) + 'px / ' + (i *100) + 'px', 'width':i*20, 'height':200});

    $('<div class="lines">').appendTo('#nye_ball').css({'top':(100 - (i * 9)), left:(i * i / 2), 'height':(i)*17.8, 'width':200 - (i * i)});
    }

    // Start the ball!
    startBall();
}

function initScreen() {
}

function initMobile() {
}
    var buildings_front = [
{'height': 400, 'width': 70},
{'height': 320, 'width': 20},
{'height': 385, 'width': 60},
{'height': 300, 'width': 10},
{'height': 365, 'width': 44, 'windows': 52, 'ww': 7, 'wh': 7},
{'height': 385, 'width': 60},
{'height': 310, 'width': 20},
{'height': 375, 'width': 30, 'windows': 17, 'ww': 27, 'wh': 5},
{'height': 325, 'width': 30},
{'height': 385, 'width': 40},
{'height': 310, 'width': 30},
];

var buildings_back = [
{'height': 400, 'width': 56, 'windows': 100, 'ww': 10, 'wh': 5, 'hat':[10, 15, 0]},
{'height': 320, 'width': 20},
{'height': 375, 'width': 50, 'hat': [0, 8, 8]},
{'height': 335, 'width': 100},
{'height': 385, 'width': 63, 'windows': 100, 'ww': 5, 'wh': 10},
{'height': 300, 'width': 10},
{'height': 385, 'width': 20, 'hat': [15, 39, 0]},
{'height': 300, 'width': 10},
{'height': 365, 'width': 60},
{'height': 385, 'width': 100},
{'height': 310, 'width': 20},
{'height': 375, 'width': 30, 'windows': 17, 'ww': 27, 'wh': 3},
{'height': 310, 'width': 30},
];

var b_count = 0;

function addBuilding(div, buildings_json) {
    building_parent = $('<div class="building_parent">').appendTo(div);
    b = buildings_json[b_count];
    building = $('<div class="building">').appendTo(building_parent).css({
        'width':b.width,
        'height':b.height
        })
    building_parent.css('padding-top', 400 - b.height);

    if(b.hat) {
        $('<div class="hat">').css({
            'border-width': '0 ' + b.hat[0] + 'px ' + b.hat[1] + 'px',
            'margin':'0px ' + b.hat[2] + 'px'
            }).insertBefore(building);
    }

    b_count++;
    if(b_count >= buildings_json.length) b_count = 0;

    if(b.windows > 0) {
        for(var i = 1; i <= b.windows; i++){
            $('<div class="window">').appendTo(building).css({
                'width':b.ww,
                'height':b.wh
                });
        }
    }
}

function startBall() {

    var start = jQuery('#ball_placement'),
        end = jQuery('#end'),
        start_offset = 0,
        end_offset = 0,
        inside = false,
        first_run = true,
        window_height = 0,
        ball_height = jQuery('#nye_ball').height(),
        list_elements = $('.content ul li'),
        list_elements_offset = {},
        current = 0,
        ball_offset = 0,
        ball_offset_middle = 0,
        animate_number = false,
        number_balls = $('#number div.number_on div'),
        number_balls_length = number_balls.length;

    function regeneratePositions(){
        start_offset = start.offset()['top'];
        end_offset = end.offset()['top'];
        window_height = $(window).height();

        list_elements_offset = {};

        $.each(list_elements, function(k, v) {
            list_elements_offset[k] = $(this).offset()['top'];
        });

        $('#nye_container').css({left:start.offset()['left']});

        // Resize the bar
        $('.bar').each(function(){  $(this).css('height', $(this).parent().height())});
    }


    regeneratePositions();

    jQuery(document).unbind("scroll").bind("scroll", function () {

        function highlightElement(){
            // Figure out which one to light up
            var window_scroll = $(window).scrollTop();

            ball_offset_middle = ball_offset + (ball_height / 3);

            if(ball_offset_middle < list_elements_offset[current] - window_scroll ||
                ball_offset_middle > list_elements_offset[current + 1] - window_scroll) {
                var new_current = 0;
                $.each(list_elements_offset, function(i, element_offset){
                    if(element_offset - window_scroll > ball_offset_middle) {
                        return false;
                    }
                    new_current = i;
                });
                $(list_elements[current]).removeClass('nye_on');
                current = parseInt(new_current);
                $(list_elements[current]).addClass('nye_on');
            }
        };

        var top_offset = start_offset - $(this).scrollTop();
        //console.log(top_offset);

        inside = inside || first_run;

        if (top_offset <= 0) {

            ball_offset = 0;

            ball_top = 0;
            ball_bottom = window_height - ball_height;

            ball_offset = ((top_offset * -1) / (end_offset - window_height - start_offset)) * ball_bottom;

            if (ball_offset > ball_bottom && inside) { /* Reached bottom, pop it out */
                inside = false;
                jQuery('#nye_ball').appendTo('body').css({
                    'position': 'absolute',
                    'top': end_offset - ball_height,
                    'left': $('#nye_container').offset()['left'],
                    'z-index': 1000
                });
                $('#number').addClass('on');

                var count_interval = 0;
                animate_number = setInterval(function(){
                    count_interval++;
                    if(count_interval > 1000) clearInterval(animate_number);
                    $($(number_balls)[Math.floor(Math.random() * number_balls_length)]).attr('class', 'number_on_' + Math.floor(Math.random() * 4));
                }, 10);

                highlightElement();

            } else if(ball_offset <= ball_bottom && ball_offset <= ball_bottom) {
                if (!inside) {
                    jQuery('#nye_ball').appendTo('#nye_container').css({
                        'position': 'absolute',
                        'top': 0,
                        'left': 0,
                        'z-index': 1000
                    });
                    inside = true;
                }
                jQuery('#nye_ball').css({
                    'top': ball_offset
                });

                highlightElement();
                $('#number').removeClass('on');
                clearInterval(animate_number);
            }
        } else if (top_offset > 0 && inside) {
            jQuery('#nye_ball').appendTo('body').css({
                'position': 'absolute',
                'top': start_offset,
                'left': $('#nye_container').offset()['left'],
                'z-index': 1000
            });
            inside = false;
            $('#number').removeClass('on');
            clearInterval(animate_number);
            highlightElement();
        }
        first_run = false;
    }).trigger('scroll');

}