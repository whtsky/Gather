# Helper methods defined here can be accessed in any controller or view in the application

module Gather
  class App
    module UserHelper
      def signup hash
        if (!User.any_of({name: hash["name"]}, {email: hash["email"]}).exists?) & (hash["username"].to_s.length > 0) & !!((hash["email"] =~ /(.*)\@(.*)\.(.*)/)) & (hash["email"].to_s.length > 0) & (hash["password"].to_s.length <= 32) & true
          u = User.create_user hash
          "fail"
          if !!u.to_s
            session[:user] = u.to_s
            u.to_s
          end
        end
      end
      def login hash
            u = User.auth hash["username"], hash["password"]
            "fail"
            session[:user] = u.to_s if !!u
            u.to_s
      end
      def login_required
        #not as efficient as checking the session. but this inits the fb_user if they are logged in
        if current_user.class != GuestUser
          return true
        else
          session[:return_to] = request.fullpath
          redirect '/login'
          return false
        end
      end
      def guest_required
        if current_user.class == GuestUser || !session[:user]
          return true
        else
          redirect '/'
          return false
        end
      end

      def current_user
        if session[:user]
          User.get(:id => session[:user])
        else
          GuestUser.new
        end
      end
      def logged_in?
        !!session[:user]
      end
      def ajax?
        !request.xhr?
      end
      def use_layout?
        !request.xhr?
      end
    end
    helpers UserHelper
  end
end
