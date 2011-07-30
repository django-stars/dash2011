var Presence = (function(){
	return {
		init: function(){
			// timeago activation;
			$("time.relative").timeago();
        } // init
    }// main return
})($);

$(document).ready(function(){
    Presence.init();
});