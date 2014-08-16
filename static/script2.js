history.navigationMode = 'compatible';
$(document).ready(function() {
    /*$('.loader').bind('pagebeforeshow', function() {
        if (event.originalEvent.persisted) {
            $('.loader, .loader_text_message').hide;
            stop();
        }
    });
    $('.loader').bind('pageshow', function() {
        $(this).page();
    });*/

    var draw = SVG('logo').size(175, 79);
    draw.attr({
        width: "175",
        height: "79"
    });

    var white_back = draw.rect(175, 79);
    white_back.attr({
        fill: "white"
    });

    var white_back2 = draw.rect(175, 79);
    white_back2.attr({
        fill: "white"
    });

    var logo_letter = draw.path("M 294,400.5 C 310.5,401.5 309,422 309,422 C 306.5,442 294,441 294,441 L 294,400.5 z M 241,369 L 234,410.5 L 228,369 L 241,369 z M 114.5,329.5 L 114.5,465.5 L 145.5,465.5 L 156.5,408.5 L 169,465.5 L 199,465.5 L 199,343 L 218.5,465.5 L 249,465.5 L 268,343 L 268,465 L 308.5,465 C 308.5,465 322.5,462.5 329.5,443 L 326.5,465.5 L 351,465.5 L 362.5,395 L 374.5,465 L 443.5,465 L 443.5,439.5 L 423,439.5 L 423,411.5 L 442.5,411.5 L 442.5,383 L 423.5,383 L 423.5,357 L 443.5,357 L 443.5,329.5 L 399,329.5 L 399,460.5 L 376,329.5 L 348.5,329.5 L 334,416.5 C 334,416.5 331.5,392.5 318,381.5 L 335.5,329.5 L 311.5,329.5 L 294.5,375 L 294.5,329.5 L 246,329.5 L 243.5,342.5 L 225,342.5 L 221,329.5 L 175,329.5 L 175,379.5 L 163,329.5 L 150.5,329.5 L 139.5,379 L 139.5,330 L 114.5,329.5 z M 452.5,465.5 L 475.5,465.5 L 475.5,356.5 L 495,356.5 L 495,329 L 452.5,329 L 452.5,465.5 z");
    logo_letter.attr({
        transform: "translate(-40,205) scale(0.42,-0.42)",
        fill: "black"
    });

    var mask = draw.mask();
    mask.add(white_back);
    mask.add(logo_letter);

    var image1 = draw.image('/img/marvel_intro_01.jpg', 175, 79);
    image1.attr({x: "0", y: "0", id: "img1"});
    var image2 = draw.image('/img/marvel_intro_02.jpg', 175, 79);
    image2.attr({x: "0", y: "0", id: "img2"});
    var image3 = draw.image('/img/marvel_intro_03.jpg', 175, 79);
    image3.attr({x: "0", y: "0", id: "img3"});
    var image5 = draw.image('/img/marvel_intro_05.jpg', 175, 79);
    image5.attr({x: "0", y: "0", id: "img5"});
    var image6 = draw.image('/img/marvel_intro_06.jpg', 175, 79);
    image6.attr({x: "0", y: "0", id: "img6"});
    var image7 = draw.image('/img/marvel_intro_07.jpg', 175, 79);
    image7.attr({x: "0", y: "0", id: "img7"});
    var image8 = draw.image('/img/marvel_intro_08.jpg', 175, 79);
    image8.attr({x: "0", y: "0", id: "img8"});
    var image9 = draw.image('/img/marvel_intro_09.jpg', 175, 79);
    image9.attr({x: "0", y: "0", id: "img9"});
    var image10 = draw.image('/img/marvel_intro_10.jpg', 175, 79);
    image10.attr({x: "0", y: "0", id: "img10"});

    image1.hide();
    image2.hide();
    image3.hide();
    image5.hide();
    image6.hide();
    image7.hide();
    image8.hide();
    image9.hide();
    image10.hide();

    var timeoutId0;
    $('#logo').hover(function(){
        if (!timeoutId0) {
            timeoutId0 = window.setTimeout(function() {
                timeoutId0 = null;
                $("#img1").delay(120).fadeIn(200, function() {$("#img1").hide();});
                $("#img2").delay(240).fadeIn(200, function() {$("#img2").hide();});
                $("#img3").delay(360).fadeIn(200, function() {$("#img3").hide();});
                $("#img5").delay(480).fadeIn(200, function() {$("#img5").hide();});
                $("#img6").delay(600).fadeIn(200, function() {$("#img6").hide();});
                $("#img7").delay(720).fadeIn(200, function() {$("#img7").hide();});
                $("#img8").delay(840).fadeIn(200, function() {$("#img8").hide();});
                $("#img9").delay(960).fadeIn(350, function() {$("#img9").hide();});
                $("#img10").delay(1400).fadeIn(200, function() {$("#img10").hide();});
            }, 350);
        }
    },
    function(e) {
        if (timeoutId0) {
            window.clearTimeout(timeoutId0);
            timeoutId0 = null;
        }
    });

    var boundary = draw.rect(175, 79);
    boundary.attr({
        x: "0",
        y: "0",
        fill: "#ea202d"
    });

    boundary.maskWith(mask);

    var timeoutId;
    $('#logo').hover( function(e) {
        if (!timeoutId) {
            timeoutId = window.setTimeout(function() {
                timeoutId = null;
                $('.tooltip_logo2').fadeIn("fast");
            }, 3500);
        }
    },
    function(e) {
        if (timeoutId) {
            window.clearTimeout(timeoutId);
            timeoutId = null;
        }
        else {
            $('.tooltip_logo2').fadeOut("fast");
        }
    });

    $('#logo').click(function(e) {
        $('.tooltip_logo2').fadeOut("fast");
        $('.tooltip_logo2').attr("class", "inactive");
    });

    var reco = $('.reco_header').attr('value');
    if (reco > 0 && reco < 19) {
        $('#carousel_ul li:first').addClass('active');
        $('#carousel_ul li:first').before($('#carousel_ul li:last'));
        $('#carousel_ul li:first').clone(true,true).appendTo($('#carousel_ul'));
        $('#right_scroll').click(function(){
            var item_width = $('#carousel_ul li').outerWidth() + 10;
            var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
            $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                $('#carousel_ul li:first').remove();
                $('#carousel_ul li:first').clone(true,true).appendTo($('#carousel_ul'));
                $('#carousel_ul').css({'left' : '-342px'});
                $('#carousel_ul li').removeClass('active');
                $('#carousel_ul li:eq(1)').addClass('active');
                if ($("#1").hasClass('active')) {
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#2").hasClass('active')) {
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1").html("<img src='marvel_circle_off.png'>");
                }
            });
        });
        $('#left_scroll').click(function(){
            var item_width = $('#carousel_ul li').outerWidth() + 10;
            var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
            $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                $('#carousel_ul li:last').remove();
                $('#carousel_ul li:last').clone(true,true).prependTo($('#carousel_ul'));
                $('#carousel_ul').css({'left' : '-342px'});
                $('#carousel_ul li').removeClass('active');
                $('#carousel_ul li:eq(1)').addClass('active');
                if ($("#1").hasClass('active')) {
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#2").hasClass('active')) {
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1").html("<img src='marvel_circle_off.png'>");
                }
            });
        });
        $("#count1").on("click", function (event) {
            if ($("#1").hasClass('active')) {
            }
            else if ($("#2").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $('#carousel_ul li:last').remove();
                    $('#carousel_ul li:last').clone(true,true).prependTo($('#carousel_ul'));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2").html("<img src='marvel_circle_off.png'>");
                });
            }
        });
        $("#count2").on("click", function (event) {
            if ($("#2").hasClass('active')) {
            }
            else if ($("#1").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $('#carousel_ul li:first').remove();
                    $('#carousel_ul li:first').clone(true,true).appendTo($('#carousel_ul'));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1").html("<img src='marvel_circle_off.png'>");
                });
            }
        });
    }
    else if (reco > 18) {
        $('#carousel_ul li:first').addClass('active');
        $('#carousel_ul li:first').before($('#carousel_ul li:last'));
        $('#right_scroll').click(function(){
            var item_width = $('#carousel_ul li').outerWidth() + 10;
            var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
            $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                $('#carousel_ul li:last').after($('#carousel_ul li:first'))
                $('#carousel_ul').css({'left' : '-342px'});
                $('#carousel_ul li').removeClass('active');
                $('#carousel_ul li:eq(1)').addClass('active');
                if ($("#1").hasClass('active')) {
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2, #count3").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#2").hasClass('active')) {
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count3").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#3").hasClass('active')) {
                    $("#count3").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count2").html("<img src='marvel_circle_off.png'>");
                }
            });
        });
        $('#left_scroll').click(function(){
            var item_width = $('#carousel_ul li').outerWidth() + 10;
            var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
            $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                $('#carousel_ul li:first').before($('#carousel_ul li:last'));
                $('#carousel_ul').css({'left' : '-342px'});
                $('#carousel_ul li').removeClass('active');
                $('#carousel_ul li:eq(1)').addClass('active');
                if ($("#1").hasClass('active')) {
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2, #count3").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#2").hasClass('active')) {
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count3").html("<img src='marvel_circle_off.png'>");
                }
                else if ($("#3").hasClass('active')) {
                    $("#count3").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count2").html("<img src='marvel_circle_off.png'>");
                }
            });
        });
        $("#count1").on("click", function (event) {
            if ($("#1").hasClass('active')) {
            }
            else if ($("#2").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $("#carousel_ul").prepend($("#3"));
                    $("#carousel_ul").append($("#2"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2, #count3").html("<img src='marvel_circle_off.png'>");
                });
            }
            else if ($("#3").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) + 2*item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:1000}, function(){
                    $("#carousel_ul").prepend($("#3"));
                    $("#carousel_ul").append($("#2"));
                    $("#carousel_ul").prepend($("#3"));
                    $("#carousel_ul").append($("#2"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count1").html("<img src='marvel_circle_on.png'>");
                    $("#count2, #count3").html("<img src='marvel_circle_off.png'>");
                });
            }
        });
        $("#count2").on("click", function (event) {
            if ($("#2").hasClass('active')) {
            }
            else if ($("#3").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $("#carousel_ul").prepend($("#1"));
                    $("#carousel_ul").append($("#3"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count3").html("<img src='marvel_circle_off.png'>");
                });
            }
            else if ($("#1").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $("#carousel_ul").prepend($("#1"));
                    $("#carousel_ul").append($("#3"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count2").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count3").html("<img src='marvel_circle_off.png'>");
                });
            }
        });
        $("#count3").on("click", function (event) {
            if ($("#3").hasClass('active')) {
            }
            else if ($("#2").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:500}, function(){
                    $("#carousel_ul").prepend($("#2"));
                    $("#carousel_ul").append($("#1"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count3").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count2").html("<img src='marvel_circle_off.png'>");
                });
            }
            else if ($("#1").hasClass('active')) {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) - 2*item_width;
                $('#carousel_ul').animate({'left' : left_indent, queue:false, duration:1000}, function(){
                    $("#carousel_ul").prepend($("#2"));
                    $("#carousel_ul").append($("#1"));
                    $("#carousel_ul").prepend($("#2"));
                    $("#carousel_ul").append($("#1"));
                    $('#carousel_ul').css({'left' : '-342px'});
                    $('#carousel_ul li').removeClass('active');
                    $('#carousel_ul li:eq(1)').addClass('active');
                    $("#count3").html("<img src='marvel_circle_on.png'>");
                    $("#count1, #count2").html("<img src='marvel_circle_off.png'>");
                });
            }
        });
    }
    else {
        $('#carousel_ul').css({'left' : '0px'});
    }

    var opts = {
        lines: 17, // The number of lines to draw
        length: 30, // The length of each line
        width: 12, // The line thickness
        radius: 54, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 0, // The rotation offset
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: '#000', // #rgb or #rrggbb or array of colors
        speed: 1, // Rounds per second
        trail: 52, // Afterglow percentage
        shadow: true, // Whether to render a shadow
        hwaccel: false, // Whether to use hardware acceleration
        className: 'spinner', // The CSS class to assign to the spinner
        position: "fixed",
        zIndex: 7, // The z-index (defaults to 2000000000)
        top: '50%', // Top position relative to parent
        left: '50%' // Left position relative to parent
    };

    $("#logo, h1, .thumbnails" ).click(function(){
        $('.loader, .loader_text_background').delay(2000).fadeIn(500);
        var target = document.getElementById('spinner');
        var spinner = new Spinner(opts).spin(target);
        spin().delay(500).fadeIn(500);
    });


    // Configure/customize these variables.
    var showChar = 112; // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "more";
    var lesstext = "less";

    $("#series_input").autocomplete({
        source: "http://www.underminer.net/autofill",
        autoFocus: "true",
        minLength: 4,
        appendTo: "#autocomplete_results"
    });

    $('#picture_large, #button').hover(function () {
       $('#button').css('background-color', '#6c6d70');
    },
    function() {
        $('#button').css('background-color', '#9fa2a5');
    });

    $('.thumbnails').hover(function() {
            $('.effekt, .issue_nr', this).show();
            $('.tooltip', this).slideToggle({direction: 'up'}, 100);
    },
    function() {
        $(".effekt, .issue_nr, .tooltip").hide();
    });

    $('#add_character').click(function() {
        $('.crowdsourcing_modal').fadeIn();
        $('.crowdsourcing_modal_inlet').delay(200).fadeIn();
    });

    var timeoutId2;
    $('#add_character').hover( function(e) {
        if (!timeoutId2) {
            timeoutId2 = window.setTimeout(function() {
                timeoutId2 = null;
                $('.tooltip_add_character').fadeIn("fast");
            }, 2000);
        }
    },
    function(e) {
        if (timeoutId2) {
            window.clearTimeout(timeoutId2);
            timeoutId2 = null;
        }
        else {
            $('.tooltip_add_character').fadeOut("fast");
        }
    });

    $('#add_character').bind('mousemove', function(e){
        $('.tooltip_add_character').css({'top':e.pageY+15,'left':e.pageX-220, 'z-index':'1'});
    });

    $(document).bind('keydown',function(e) {
        var keypressed = e.which;
        if ($('.crowdsourcing_modal_inlet').attr('style') != 'display: block;') {
            return true;
        }
        else if ((keypressed >=65 && keypressed <= 90) ||
                (keypressed >=48 && keypressed <= 57) ||
                (keypressed >= 96 && keypressed <= 105) ||
                (keypressed >= 35 && keypressed <= 40) ||
                keypressed === 8 ||
                keypressed === 13 ||
                keypressed === 16 ||
                keypressed === 27 ||
                keypressed === 46 ||
                keypressed === 106 ||
                keypressed === 188) {
                $('#new_char_input').focus();
        }
    });

    $('#send_mail_to_author').click(function() {
        $('.crowdsourcing_modal').fadeIn();
        $('.sendmail_modal_inlet').delay(200).slideToggle();
    });

    $('.crowdsourcing_modal').click(function() {
        $('.sendmail_modal_inlet').slideToggle();
        $('.crowdsourcing_modal, .crowdsourcing_modal_inlet, .sendmail_modal_inlet_sent').delay(200).fadeOut();
    });

    $('#cancel, #cancel_contact, #cancel_contact_sent').click(function() {
        $('.crowdsourcing_modal, .crowdsourcing_modal_inlet, .USG_modal_chars, .sendmail_modal_inlet, .sendmail_modal_inlet_sent').hide();
        $('#new_char_input').val('');
        $('.post_modal_added_char_list').remove();
        $(".wrapper_test").remove();
        $('#name, #email, #subject, #message').val('');
        $('#name, #email, #subject, #message').attr('class', 'valid');
        $('#name, #email, #message').removeAttr('aria-required').removeAttr('aria-invalid').removeAttr('class');
        $('#name, #email').attr('placeholder', '');
        $('#message').attr('placeholder', 'Your message...*');
        $('#disclaimer_post').hide();
        $('.disclaimer').show();
    });

    $('.thumbnails_results').hover(function() {
        $('.effekt_results, .issue_nr_results, .publication_date_results', this).show();
        $('.tooltip_results', this).slideToggle({direction: 'up'}, 100);
    },
    function() {
        $('.effekt_results, .issue_nr_results, .tooltip_results, .publication_date_results', this).hide();
    });

    $('.more').each(function() {
        var content = $(this).html();
        if(content.length > showChar) {
            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);
            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
            $(this).html(html);
        }
    });

    $(".morelink").click(function() {
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        }
        else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });

    $("#button_more").click(function() {
       $(".animate").hide();
       $(".animate2").fadeIn(1000);
    });

    jQuery.validator.setDefaults( {
        debug: true
    });
    $(".search").validate({
        errorClass: "wrong",
        rules: {
            series: {
                required:true }
        },
        messages :{
            series : {
                required: 'Please name a series!'
                }
        },
        submitHandler: function(form) {
            $('.loader, .loader_text_background').show();
            form.submit();
        },
        errorPlacement: function(error, element) {
            error.appendTo( element.parent("td").next("td") );
        }
    });

    $('#name, #email, #subject, #message').focus(function() {
        if ($(this).hasClass("error")) {
            $(this).keyup(function() {
                $(this).addClass('active').removeClass('error');
            });
        }
        else {
            $(this).addClass('active').removeClass('inactive');
        }
    });

    $('#name, #email, #subject, #message').blur(function() {
            if ($(this).hasClass("error")) {
                return true;
            }
            else {
        $(this).addClass('inactive').removeClass('active').removeClass('error');
            }
    });

    $('.send_mail').validate({
        validClass: "valid",
        errorClass: "error",
        onkeyup: false,
        rules: {
            name: {
                required:true},
            email: {
                required:true,
                email: true},
            message: {
                required:true,
                minlength: 4
                }
        },
        messages :{
            name : {
                required: 'Please name yourself!'
            },
            email : {
                required: 'Please enter a valid email address!'
            },
            message : {
                required: 'Please leave a message!'
            }
        },
        errorPlacement: function(error, element) {
            $(element).attr("placeholder", error.text());
            $(element).val('');
        },
        highlight: function(element, errorClass, validClass ) {
            $(element).addClass(errorClass).removeClass(validClass);
        },
        unhighlight: function(element, errorClass, validClass ) {
            $(element).removeClass(errorClass).addClass(validClass);
        },
        submitHandler: function(form) {
            var name = $("#name").val();
            var email = $("#email").val();
            var subject = $("#subject").val();
            var message = $("#message").val();
            var dataString = {"name":name,"email":email,"subject":subject,"message":message};

            $.ajax( {
                type : "POST",
                url : "/sendmail",
                data: JSON.stringify(dataString),
                contentType: 'application/json;charset=UTF-8',
                dataType: 'json',
                success: function() {
                    $(".sendmail_modal_inlet").hide();
                    $(".sendmail_modal_inlet_sent").show();
                }
            });
        }
    });

    $(function() {
        function split( val ) {
            return val.split( /,\s*/ );
        }
        function extractLast( term ) {
            return split( term ).pop();
        }
        $( "#new_char_input" ).bind( "keydown", function( event ) {
            if ( event.keyCode === $.ui.keyCode.TAB && $( this ).data( "ui-autocomplete" ).menu.active ) {
                event.preventDefault();
            }
        })
        .autocomplete({
            appendTo: "#test",
            autoFocus: "true",
            source: function( request, response ) {
                $.getJSON( "http://www.underminer.net/characters", {term: extractLast( request.term )}, response );
            },
            search: function() {
            // custom minLength
                var term = extractLast( this.value );
                if ( term.length < 2 ) {
                    return false;
                }
            },
            focus: function() {
            // prevent value inserted on focus
                return false;
            },
            select: function( event, ui ) {
                var terms = split( this.value );
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push( ui.item.value );
                // add placeholder to get the comma-and-space at the end
                terms.push( "" );
                this.value = terms.join( ", " );
                this.selectionStart = this.selectionEnd = this.value.length;
                return false;
            }
        });
    });

    $('#new_char_input').focus(function() {
        if ($(this).attr("class") === "error warning" || $(this).attr("class") === "ui-autocomplete-input error warning") {
            $(this).css({"border": "2px solid #ea202d", "width": "339px", "height": "32px"});
        }
        else {
            $(this).css({"border": "2px solid #9d9fa2", "width": "339px", "height": "32px"});
            }
    });

    $('#new_char_input').blur(function() {
        $('#new_char_input').css({"border": "1.5px solid #9d9fa2", "width": "341px", "height": "34px"});
        $('#new_char_input').removeClass('error warning');
        $('#new_char_input').removeClass('ui-autocomplete-input error warning');
    });

    $(".new_character").validate({
        rules: {
            new_char_input: {
                required:true,
                minlength: 2 },
            message: {
                required:true }
        },
        messages :{
            new_char_input : {
                required: 'You need to name at least one character!'
            },
        },
        errorPlacement: function(error, element) {
            $(element).attr("placeholder", error.text());
            $(element).addClass('warning');
            $(element).css({"border": "2px solid #ea202d", "width": "339px", "height": "32px"});
            $('#new_char_input').val('');
            $(element).keyup(function() {
                if ($(element).val().length > 1) {
                    $(element).css({"border": "2px solid #9d9fa2", "width": "339px", "height": "32px"});
                    $(element).removeClass('warning');
                    $(element).attr("placeholder", "e.g. Captain America");
                }
            });
        },
        submitHandler: function(form) {
            $('.USG_modal_chars').show();
            $('.disclaimer').hide();
            $('#disclaimer_post').fadeIn('normal');
            if (/,\s/.test($('#new_char_input').val())) {
                if (/,\s$/.test($('#new_char_input').val())) {
                    var char_array = $('#new_char_input').val().split(", ")
                    var i;
                    for (i = 0; i < char_array.length-1; ++i) {
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array[i]+", ")).appendTo($('.added_character_wrapper'));
                    }
                }
                else {
                    var char_array = $('#new_char_input').val().split(", ")
                    var i;
                    for (i = 0; i < char_array.length; ++i) {
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array[i]+", ")).appendTo($('.added_character_wrapper'));
                    }
                }
                $('#new_char_input').val('');
                $('<div class=delete>X</div>').appendTo($('.wrapper_test'));
            }
            else if (/,/.test($('#new_char_input').val())) {
                if (/,$/.test($('#new_char_input').val())) {
                    var char_array = $('#new_char_input').val().split(",")
                    var i;
                    for (i = 0; i < char_array.length-1; ++i) {
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array[i]+", ")).appendTo($('.added_character_wrapper'));
                    }
                }
                else {
                    var char_array = $('#new_char_input').val().split(",")
                    var i;
                    for (i = 0; i < char_array.length; ++i) {
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array[i]+", ")).appendTo($('.added_character_wrapper'));
                    }
                }
                $('#new_char_input').val('');
                $('<div class=delete>X</div>').appendTo($('.wrapper_test'));
            }
            else {
                if (/\s+/g.test($('#new_char_input').val())) {
                    var char_array = $('#new_char_input').val().split(" ")
                    var i;
                    for (i = 0; i < char_array.length; ++i) {
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array[i]+", ")).appendTo($('.added_character_wrapper'));
                    }
                }
                else {
                    var char_array = $('#new_char_input').val()
                        $('<div class ="wrapper_test"></div>').html($('<div class="post_modal_added_char_list"></div>').html(char_array)).appendTo($('.added_character_wrapper'));
                }
                $('#new_char_input').val('');
                $('<div class=delete>X</div>').appendTo($('.wrapper_test'));
            }
        }
    });

    $(".added_character_wrapper").on ( {
            mouseenter: function(){
                $(this).find('.delete').css({'display': 'inline-block', 'opacity': '0.8'});
                $(this).css({'background-color': 'red', 'opacity': '0.6', 'color': 'white', 'padding': '3px 0.5px 1px 1px', 'border': '1px solid #616363', 'box-shadow': '4px 4px 17px 0px rgba(50, 50, 50, 0.75)'});
            },
            mouseleave: function () {
                $(this).find('.delete').css('display', 'none');
                $(this).css({'background-color': 'transparent', 'opacity': '1', 'color': 'black', 'border': 'none', 'box-shadow': 'none', 'padding': '5px 3.5px 1px 0px'});
            }
    }, '.wrapper_test');

    $('.added_character_wrapper').on('click','.wrapper_test',function () {
        if ($('.added_character_wrapper > div').length === 1) {
            $('.USG_modal_chars').fadeOut("normal");
            //$('#new_char_input').css('margin-top', '10px');
            $('#disclaimer_post').hide();
            $('.disclaimer').fadeIn('normal');
        }
        $(this).fadeOut("normal", function() {
            $(this).remove();
        });
    });

    $('#submit').click(function(){
        if ($('.post_modal_added_char_list').length === 0) {
            $('.new_character').valid();
            if ($('#new_char_input').val().length > 1) {
                var issue = $('#series_issue').text();
                var subject = "New character added to " + issue;
                var comic_id = "12";
                var character_list_raw = $.trim($('.crowdsourcing_modal_chars_list').text());
                var character_list = character_list_raw.replace( /\s\s+/g,' ');
                var message = $('#new_char_input').val();
                var dataString = {'subject':subject,'message':message,'character_list':character_list,'issue':issue,'comic_id':comic_id};

                $.ajax( {
                    type : "POST",
                    url : "/sendcharacter",
                    data: JSON.stringify(dataString),
                    contentType: 'application/json;charset=UTF-8',
                    dataType: 'json',
                    success: function() {
                        $(".crowdsourcing_modal_inlet").hide();
                        $(".wrapper_test").remove();
                        $(".sendmail_modal_inlet_sent").show();
                    }
                });
            }
            else {
                $('#new_char_input').val('');
                $('#new_char_input').focus();
            }
        }
        else if ($('.post_modal_added_char_list').length !== 0) {
            var issue = $('#series_issue').text();
            var subject = "New character added to " + issue;
            var comic_id = "12";
            var character_list_raw = $.trim($('.crowdsourcing_modal_chars_list').text());
            var character_list = character_list_raw.replace( /\s\s+/g,' ');
            var message = $('.post_modal_added_char_list').text()+$('#new_char_input').val();
            var dataString = {'subject':subject,'message':message,'character_list':character_list,'issue':issue,'comic_id':comic_id};

            $.ajax( {
                type : "POST",
                url : "/sendcharacter",
                data: JSON.stringify(dataString),
                contentType: 'application/json;charset=UTF-8',
                dataType: 'json',
                success: function() {
                    $(".crowdsourcing_modal_inlet").hide();
                    $(".wrapper_test").remove();
                    $(".sendmail_modal_inlet_sent").show();

                }
            });
        }
    });

    $('#plus').hover(function() {
        $('#add_char_modal_plus').css("background-color", "#90b02a");
    },
    function(){
        $('#add_char_modal_plus').css("background-color", "#9dc02e");
    });
});