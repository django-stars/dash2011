var Presence = (function(){
    return {
        init: function(){
            $("time.relative").timeago();
            Presence.makeShout();
        }, // init
        makeShout: function(){
            var top_shout = $("form.shout");
            var text_ = top_shout.find("textarea");
            $("#shout-action").click(function(){
                if (top_shout.is(":visible")){
                    top_shout.slideUp();
                }
                else {
                    top_shout.slideDown();
                    text_.focus();
                }
                return false;
            }); // click
            top_shout.submit(function(){
                var this_ = $(this);
                $.post(
                    this_.attr("action"),
                    this_.serialize(),
                    function(data){
                        if (data.response == "OK"){
                            top_shout.slideUp();
                            text_.val("");
                        }
                        else {
                            alert(data.reason);
                        }
                    }, "json") // post
                return false;
            })
        }
    }// main return
})($);

$(document).ready(function(){
    Presence.init();
});