search = ->
  txt = $('.search-query').val()
  if not txt
    return false
  window.open "https://www.google.com/search?q=site:#{domain} #{txt}"
  $('.search-query').val('')
  return false

_ = (msg) ->
  return i18n[msg] if i18n?[msg]?
  return msg

window.notify = () ->
  setTimeout(window.notify, 30000)
  $.ajax
    url: "/api/notifications/new"
    success: (data) ->
      if not data.id?
        return
      last_id = window.localStorage.getItem('last_notify')
      window.localStorage.setItem('last_notify', data.id)
      for notification in data.notifications
        if notification.id == last_id
          return
        $.notifier.notify(notification.avatar, notification.title,
        notification.content, notification.url)
      return

floor_link_page = ->
  floor_link = $(".mention.mention_floor")
  for i in floor_link
    floor_num = new Number(i.href.match(/#reply(\d+)/)[1])
    floor_page = new Number(
      (floor_num + @replies_per_page - 1) / @replies_per_page)
    floor_page = parseInt(floor_page)
    i.href = "?p=#{floor_page}#reply#{floor_num}"
  return

topic_link = ->
  element = $(".mention.mention_topic")
  elements = {}
  for i, num in element
    _id = $(i).attr("_id")
    elements[_id] = {"_id": _id, "object": i}
    $.ajax({
      url: "/api/topic/#{_id}/json",
      cache: false,
      success: (data) ->
        object = elements[data._id].object
        _id = $(object).attr("_id")
        _title = data.title
        _content_short = data.content.slice(0,20)
        object.title = "#{_title}\n\n#{_content_short}"
        return
    })
  return

$ ->
  notify()
  $('time').timeago()
  $('.dangerous').click ->
    if window.confirm(_('Are you sure?'))
      window.location = $(this).data('href')
    return false
  $('.remove').click ->
    $this = $(this)
    url = $this.data('href')
    if window.confirm(_('Are you sure?'))
      type = $this.data('type')
      $.post url, ->
        if type == "topic"
          window.location.href = "/"
        else
          $this.parents(".list").remove()
    return false
  floor_link_page()
  topic_link()
  return
