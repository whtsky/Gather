$ ->
  names = []
  for a in $('.reply_user')
    name = $(a).text()
    if name not in names
      names.push(name)

  $('#content').atWho '@', {data: names}
  return