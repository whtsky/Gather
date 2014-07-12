Gather::App.controllers :topic do
  layout :common
	get :view, :with => :id do
		@t = Topic.any_of({id: params[:id]}, {old_id: params[:id].to_i})[0]
    @r = Reply.where(:topic => @t.id)
		render :view
	end
	get :list, :with => :page do
		@topics = Topic.desc(:last_replied_at).page(params[:page])
		render :list, :layout => true
	end
	get :list_first_page, :map => '/topic/list' do
		redirect to('/topic/list/1')
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
