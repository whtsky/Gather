Gather::App.controllers :user do
  layout :common
  get :login, :map => '/login' do
    render :login
  end
  get :signup, :map => '/signup' do
    render :signup
  end
  get :pub, :map => '/get_pk' do
    settings.rsa_pub.to_s
  end
  post :call_sign, :map => '/sign' do
    begin
      @j = params[:j]
      puts @j
      @h = JSON.parse(Base64.decode64(@j))
      puts @h
    rescue
      halt 404
    else
      case @h["method"]
        when "login" then sign('in', @h)
        when "signup" then sign('up', @h)
        end
    end
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
