var Presence = (function(){
    return {
        init: function(){
            $("time.relative").timeago();
            Presence.makeShout();
        }, // init
        makeShout: function(){
            var top_shout = $("form.shout");
            $("#shout-action").click(function(){
                if (top_shout.is(":visible")){
                    top_shout.slideUp();
                }
                else {
                    top_shout.slideDown();
                    top_shout.find("textarea").focus();
                }
                return false;
            }); // click
            top_shout.submit(function(){
                var this_ = $(this);
                $.post(
                    this_.attr("action"),
                    this_.serialize(),
                    function(data){
                        if (data){
                            top_shout.slideUp();
                        }
                    }) // post
                return false;
            })
        }
    }// main return
})($);

$(document).ready(function(){
    Presence.init();
});