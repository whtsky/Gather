Gather::App.controllers :user do
  layout :common
  get :login, :map => '/login' do
    guest_required
    render :login
  end
  get :signup, :map => '/signup' do
    guest_required
    render :signup
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
  get :session, :map => '/session' do
    session[:user].to_s
  end
  get :logout, :map => '/logout' do
    session[:user] = nil
    nil
    "exit!" if ajax?
  end

  get '/:key' do
    @u = User.any_of({id: params[:key]}, name: params[:key])[0]
    @img = "https://ruby-china.org/avatar/#{Digest::MD5.hexdigest @u.email}.png?s=96&d=404"
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
