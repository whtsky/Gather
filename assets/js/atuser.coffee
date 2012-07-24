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

  $('#content').atWho '@', {data: names}
  return