loading_icon = $("#spinner")

$(document).on 'page:load', ->
  loading_icon.hide()

$(document).ready ->
  loading_icon.hide()

$(document).on 'page:fetch', ->
  loading_icon.css("display","block")
