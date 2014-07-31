String.prototype.repeat = (num)->
  return new Array(num + 1).join(this)

CSRF_TOKEN = ''

String.prototype.encodeu = ()->
  result = ''
  for x in [0..this.length-1]
    a = this.charCodeAt(x)
    result += "\\u" + a
  return result

configureCSRF = ()->
  $.ajax {
    type: 'GET', url: '/csrf_token',
    async: false,
    cache: false,
    success: (data, textStatus, jqXHR)->
      CSRF_TOKEN = data.csrf
    fail: (data, textStatus, jqXHR)-> 
    	console.log("fail")
  }

self.topic = {
  cloud_find: ->
    $("#cloud-find").keyup ()->
      if this.value != ""
        $("#users_cloud a").hide()
        $("#users_cloud a:contains('".concat(this.value).concat("')")).show()
      else
        $("#users_cloud a").show()

  create_fun: ->
    $.fn.tagcloud.defaults = {
      size: {start: 1, end: 3, unit: 'em'},
      color: {start: '40B16D', end: '#FC5100'}
    }
    $("#new-topic-content").keyup ->
      $("#new-topic-content").autosize()

    $('#users_cloud a').tagcloud()

    $("#new-topic-form").submit (e)->
      e.preventDefault()

    $(".topic-submit").click ->
      if $("#new-topic-title")[0].value.replace(" ", "") == ""
        $("#new-topic-title").css "background", "crimson"
      else
        ->
          $("#users_cloud").slideUp()
        submit_content this.getAttribute("data-node-slug")

    topic.cloud_find()
    submit_content = (node)->
      b64 = new Base64()
      dataa = {
          title: emoji.replace_colons(emoji.replace_unified($("#new-topic-title")[0].value)),
          content: ali.replace_colons(emoji.replace_colons(emoji.replace_unified($("#new-topic-content")[0].value))),
          node: node
        }
      data = b64.encode(JSON.stringify dataa)
      configureCSRF()
      $.post("/topic/create", {j: data, authenticity_token: CSRF_TOKEN}, (result)->
        window.location.href="/topic/view/" + result
      ).fail ->
          alert "Try again~"
          $("#users_cloud").slideDown()

  reply_fun: ->
    $("#new-reply-content").keyup ->
      $("#new-reply-content").autosize()

    $("#new-reply-form").submit (e)->
      e.preventDefault()
      submit_reply()

    submit_reply = ()->
      b64 = new Base64()
      dataa = {
          topic: $(".topic-content")[0].getAttribute("data-id"),
          content: ali.replace_colons(emoji.replace_colons(emoji.replace_unified($("#new-reply-content")[0].value)))
        }
      data = b64.encode(JSON.stringify dataa)
      configureCSRF()
      $("#new-reply-form").slideUp()
      $.post "/topic/reply", {j: data, authenticity_token: CSRF_TOKEN}, (result)->
          window.location = "/topic/view/" + $(".topic-content").data("id")
      $("#new-reply-form").slideDown()
}
