init_at_who = ->
  names = []

  add_name = (ele) ->
    name = $(ele).text()
    if name not in names
      names.push(name)

  for a in $('.user')
    add_name a

  $('textarea').atwho at: '@', data: names
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

gather_page_load = ->
  gather_main()
  _gaq.push(['_trackPageview'])


$(document).on 'page:load', gather_page_load

$(document).ready gather_main
