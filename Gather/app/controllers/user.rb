Gather::App.controllers :user do
  layout :common
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
