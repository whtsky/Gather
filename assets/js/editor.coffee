$ ->
  names = []
  
  add_name = (ele) ->
    name = $(ele).text()
    if name not in names
      names.push(name)

  for a in $('.username')
    add_name a
  for a in $('.reply_user')
    add_name a

  $('#content').elastic().atWho '@', {data: names}

  $('.reply').click ->
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
    
  if not window.localStorage
    return
    
  if $('#title').length != 0
    $('#title').val(window.localStorage.getItem('title')).change ->
      window.localStorage.setItem('title', $(this).val())
      return
    key = 'post'
  else
    key = /\w{24}/.exec(window.location)[0]
  if not key
    return
  $('#content').val(window.localStorage.getItem(key)).change ->
    window.localStorage.setItem(key, $(this).val())
    return
  $('form').submit ->
    window.localStorage.setItem('title', '')
    window.localStorage.setItem(key, '')
    return
    
  