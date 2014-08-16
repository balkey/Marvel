$(document).ready(function() {
    // Configure/customize these variables.
    var showChar = 112; // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "more";
    var lesstext = "less";


    $('.more').each(function() {
        var content = $(this).html();

        if(content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });

    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });

       $('.thumbnails').hover(
    function(){
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<div class="effekt"></div>').prependTo(this);
        $('.issue_nr', this).css({"display": "block"});
        $('<p class="tooltip"></p>').text(title).prependTo(this).slideToggle({direction: 'up'}, 100);
    },
    function(){
    $(".effekt").remove();
    $(".issue_nr", this).hide();
    $(this).attr('title', $(this).data('tipText'));
    $(".tooltip").remove();
    }
    );
});