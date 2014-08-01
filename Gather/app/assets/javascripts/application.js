// This is a manifest file that'll be compiled into including all the files listed below.
// Add new JavaScript/Coffee code in separate files in this directory and they'll automatically
// be included in the compiled file accessible from http://example.com/assets/application.js
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
//= require jquery
//= require jquery-ujs
//= require timeago
//= require tagcloud
//= require bin
//= require ali
//= require b64
//= require user
//= require jquery.autoheight
//= require topic
//= require turbolinks
//= require_self



jQuery(document).ready(function() {
  jQuery("abbr.timeago").timeago();
	function RndRgb() {
		return parseInt(Math.random() * (0 - 255 + 1) + 255);
	}
});

$(function() {
   jQuery("abbr.timeago").timeago();
}); $(window).bind('page:change', function() {
  jQuery("abbr.timeago").timeago();
  $("#loading").hide();
})
$(window).bind('page:before-change', function() {
    $("#loading").show();
})
