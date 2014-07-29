Gather::App.controllers :topic do
  layout :common
	get :view, :with => :id do
		@t = match_topic params[:id]
    @p = 1
    @p = params[:page] if params[:page]
    if @t
      @r = Reply.where(:topic => @t.id).asc(:created_at).page(params[:page])
  		render :view
    else
      halt 404 
    end
	end
  get "/view/:id/:page" do
    @t = match_topic params[:id]
    @p = params[:page]
    if @t
      @r = Reply.where(:topic => @t.id).asc(:created_at).page(params[:page])
      render :view
    else
      halt 404 
    end
  end
  get "/list" do
    @topics = Topic.desc(:last_replied_at).page(1)
    render :list, :layout => true
  end
	get "/list/:page" do
		@topics = Topic.desc(:last_replied_at).page(params[:page])
		render :list, :layout => true
	end
  get :node, :map => "/node" ,:with => :slug do
    @n = Node.where(slug: params[:slug])
    if !!@n.exists?
      @n = @n.first
      @topics = @n.topics.desc(:last_replied_at).page(params[:page])
      render :list_node
    else
      halt 404
    end
  end
  get :nodes, :map => "/nodes" do
    @n = Node.all
    render :nodes
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
