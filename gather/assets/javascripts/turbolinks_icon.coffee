$(document).on 'page:load', ->
  $("#spinner").hide()

$(document).on 'page:fetch', ->
  $("#spinner").show()

$(document).ready ->
  $("#spinner").hide()
