// csrf support
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

var Presence = (function(){
    return {
        init: function(){
            $("time.relative").timeago();
            Presence.makeShout();
            Presence.workflowUpdate();
            Presence.initModal();
            Presence.initPlan();
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
            
            
        }, // workflowUpdate

        initModal: function(){
            $('#modal .close-modal').click(function(){
                $('#modal').hide();
            });
        },
        loadInModal: function(url){
            $('#modal .content').load(url, function(){
                modal_width = 400;
                modal_height = 400;
                $('#modal').css({
                    'left': ($(window).width() - modal_width) / 2,
                    'top': ($(window).height() - modal_height) / 2,
                    'width': modal_width,
                    'height': modal_height,
                    'position': 'fixed',
                    'z-index': 10000,
                    'display': 'block'
                });
                // finding form and make it submitable throw ajax
                $('#modal form').live('submit', function(){
                    var form_ = $(this);
                    $.post(
                           form_.attr("action"),
                           form_.serialize(),
                           function(data){
                               if (data['response'] == 'ok') {
                                   $('#modal').hide();
                                   /*
                                    TODO refresh latest activity
                                   */
                               }
                               else {
                                   $('#modal .content').html(data['html']);
                               }
                           }
                    );
                    return false;
                });
            });
        }, // loadInModal
        initPlan: function(){
            $('#plan-link').click(function(){
                Presence.loadInModal('/planning/');
                return false;
            });
        }
    }// main return
})($);

$(document).ready(function(){
    Presence.init();
});