Gather::App.controllers :user do
  layout :common
  get :users, :map => '/users' do
    login_required
    render :users
  end
  get :login, :map => '/login' do
    guest_required
    render :login
  end
  get :signup, :map => '/signup' do
    guest_required
    render :signup
  end
  get :settings, :map => "/settings" do
    login_required
    render :settings
  end
  post :settings, :map => "/settings" do
    login_required
    if params[:j]
      begin
        a = JSON.parse(Base64.decode64 params[:j])
        puts a
        css = a["css"]
        info = a["info"]
        site = ""
        info = Sanitize.fragment(info, Sanitize::Config::BASIC)
        site = a["site"] if !!(a["site"] =~ /^(http|https)\:\/\/(.+)\.(.+)$/)
        current_user.update(
            css: css,
            info: info,
            site: site
          )
        "Success!"
      rescue
        "Fail!"
      end
    end
  end
  post :call_sign, :map => '/sign' do
    guest_required
    begin
      @j = params[:j]
      @h = JSON.parse(Base64.decode64(@j))
    rescue
      halt 404
    else
      case @h["method"]
        when "in"
          login @h
        when "up"
          signup @h
        end
    end
  end
  get :logout, :map => '/logout' do
    session[:user] = nil
    redirect to("/")
  end

  get '/:key' do
    @u = User.any_of({id: params[:key]}, name: params[:key])[0]
    render :view
  end

  # get :index, :map => '/foo/bar' do
  #   session[:foo] = 'bar'
  #   render 'index'
  # end

  # get :sample, :map => '/sample/url', :provides => [:any, :js] do
  #   case content_type
  #     when :js then ...
  #     else ...
  # end

  # get :foo, :with => :id do
  #   'Maps to url '/foo/#{params[:id]}''
  # end

  # get '/example' do
  #   'Hello world!'
  # end
  

end
