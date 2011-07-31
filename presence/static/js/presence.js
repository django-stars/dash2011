var Presence = (function(){
    return {
        init: function(){
            $("time.relative").timeago();
            Presence.makeShout();
            Presence.workflowUpdate();
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
        }, // makeShout
        
        workflowUpdate: function(){
            $("#workflow label").each(function(){
                var this_ = $(this);
                var form_ = $(this).closest("form");
                var select_ = $("select", form_);
                var controls = $("span.control", form_);

                form_.submit(function(){
                   $.post(
                       form_.attr("action"),
                       form_.serialize(),
                       function(data){
                           controls.hide();
                       }
                    );
                    return false;
                }); //change
                this_.click(function(){
                    if (controls.is(":visible")) {
                        controls.hide();
                    }
                    else {
                        controls.show();
                    }
                }); // click
            }) // each
            
            
        } // workflowUpdate
    }// main return
})($);

$(document).ready(function(){
    Presence.init();
});