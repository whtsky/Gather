# Helper methods defined here can be accessed in any controller or view in the application

module Gather
  class App
    module UserHelper
      # def simple_helper_method
      # ...
      # end
      def sign method, hash
      	case method
        	when "up"
        		if (!User.any_of({name: hash["name"]}, {email: hash["email"]})) & (hash["name"].to_s.length > 0) & !!((hash["email"] =~ /(.*)\@(.*)\.(.*)/) == 0) & (hash["email"].to_s.length > 0) & (hash["password"].to_s.length <= 32) & true
        			User.create_user hash
            end
        	when "in"
            ''
        	end
      end
    end

    helpers UserHelper
  end
end
