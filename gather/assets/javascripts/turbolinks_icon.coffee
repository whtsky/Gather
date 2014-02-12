loading_icon = $("#turbolinks_loading")

$(document).on 'page:load', ->
  loading_icon.hide()

$(document).on 'page:fetch', ->
  loading_icon.css("display","inline-block")
