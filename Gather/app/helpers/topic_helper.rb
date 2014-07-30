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
      def parse_content c
        @ca = c.each_line
        @rca = []
        @ca.each do |s|
          @sa = []
          s.split(" ").each do |x|
            #Urls and Images
            @x = (escape_html x)
            @t = (escape_html x)
            if !@t.gsub! /(http|https)(.*)(\.jpg|\.png|\.svg|\.gif|\.jpeg|\.bmp)/ , '<img src="\0" / >'
              @t.gsub! /(http|https)(.*)/, '<a href="\0">\0</a>'
            else
              #Emoji
              @t = @x if !@t.gsub("\"", '').gsub(/::(.*)::/, '<img src="/images/emoji/\0.gif" / >')
            end
            @sa << @t
          end
          @rca << '<p>' + (@sa.join ' ') + '</p>' 
        end
        @rca.join
      end
      # def simple_helper_method
      # ...
      # end
    end

    helpers TopicHelper
  end
end
