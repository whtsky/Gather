Gather::App.helpers do
  def icon name
    "<i class=\"fa fa-#{name.to_s}\"></i>"
  end
  def link_icon_to name, text="", target
  	"<a href=\"#{target}\"><i class=\"fa fa-#{name.to_s}\"></i><span>#{text}</span></a>"
  end
  def get_user id
  	User.where(id: id).first
  end
  def avatar_url email, a
  	"//ruby-china.org/avatar/#{Digest::MD5.hexdigest email}.png?s=#{a.to_i.to_s}&d=404"
  end
  def avatar email, a
  	"\<img src=\"" + self.avatar_url(email,a) + "\" \>"
  end
  def timeago time
  	"<abbr class=\"timeago\" title=\"#{time}\"></abbr>"
  end
end

