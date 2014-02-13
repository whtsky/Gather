init_at_who = ->
  names = []

  add_name = (ele) ->
    name = $(ele).text()
    if name not in names
      names.push(name)

  for a in $('.user-link')
    add_name a

  $('textarea').atWho '@', {data: names}
  return
###, callbacks: {
    remote_filter: (query, callback) ->
      $.ajax {
        url: '/api/user',
        data: ,
        dataType: "json",
        contentType: "application/json",
        success: (data) ->
          names = []
          if !data.objects
            return callback([])
          for account in data.users
            if account.username not in names
              names.push(account.username)
          callback(names)
      }
    }
###


have_textarea = ->
  $("textarea").length

resize = ->
  $("textarea").scroll ->
    $(this).height(this.scrollHeight)

gather_main = ->
  if have_textarea()
    resize()
    init_at_who()
  $("time").timeago(selector: 'time')

  $('.reply_the_floor').click ->
    reply = $(this)
    floor = reply.data('floor')
    user = reply.data('user')

    reply_content = $("#content")
    new_text = "##{floor} @#{user} "
    if reply_content.val().trim().length is 0
      new_text += ''
    else
      new_text = "\n#{new_text}"
    reply_content.focus().val reply_content.val() + new_text
    return false

gather_page_load = ->
  gather_main()
  _gaq.push(['_trackPageview'])


$(document).on 'page:load', gather_page_load

$(document).ready gather_main
