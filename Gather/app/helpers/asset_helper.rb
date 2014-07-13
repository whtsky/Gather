Gather::App.helpers do
  def icon name
    "<i class=\"fa fa-#{name.to_s}\"></i>"
  end
  def link_icon_to name, text="", target
  	"<a href=\"#{target}\"><i class=\"fa fa-#{name.to_s}\"></i><span>#{text}</span></a>"
  end
end