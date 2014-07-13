# Helper methods defined here can be accessed in any controller or view in the application

module Gather
  class App
    module TopicHelper
      def get_topic id
      	@t = Topic.where(id: id).first
      	@t if @t
      end
      def get_new_id id
      	@t = Topic.where(old_id: id.to_i).first
      	@t.id if @t
      end
      def match_topic id 
      	if id.length == 24
      		@t = self.get_topic id
      	else
      		@i = self.get_new_id id
      		@t = (self.get_topic @i) if @i
      	end
      	@t
      end
      def get_reply_count id 
        Reply.where(topic: id).count
      end
      # def simple_helper_method
      # ...
      # end
    end

    helpers TopicHelper
  end
end
