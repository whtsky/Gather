require "mongoid"
require "pg"
require "active_record"
require "pbkdf2"

Mongoid.load!(File.join('./config', 'database.yml'), "production")
ActiveRecord::Base.establish_connection(    
  :adapter  => 'postgresql',     
  :database => 'gather', 
  :username => 'gather',     
  :password => '')   

#This script will migrate your data from Gather v3
#Remind that histories, read contings will be dropped.

module Old
	class Topic < ActiveRecord::Base
		self.table_name = "topic"
	end
	class Node < ActiveRecord::Base
		self.table_name = "node"
	end
	class Reply < ActiveRecord::Base
		self.table_name = "reply"
	end
	class Account < ActiveRecord::Base
		self.table_name = "account"
	end
end
module New
	class Topic
		include Mongoid::Document
		include Mongoid::Attributes::Dynamic
		store_in collection: "topics"
	end
	class Reply
		include Mongoid::Document
		include Mongoid::Attributes::Dynamic
		store_in collection: "replies"
	end
	class Node
		include Mongoid::Document
		include Mongoid::Attributes::Dynamic
		store_in collection: "nodes"
	end
	class User
		include Mongoid::Document
		include Mongoid::Attributes::Dynamic
		store_in collection: "users"
	end
end
nodes = []
users = []
Old::Node.all.each do |x|
	nodes << [x.id.to_s, x.slug]
	New::Node.create(
		:slug => x.slug,
		:name => x.name,
		:description => x.description,
		:icon => x.icon
		)
end
#PBKDF2.new(:password=>pass + pwd_key, :salt=>salt, :iterations=>1000, :hash_function=>OpenSSL::Digest::SHA1.new).hex_string
Old::Account.all.each do |x|
	pass = x.password.split('$')
	@user = New::User.new(
		:name => x.username,
		:email => x.email,
		:hashed_password => pass[2],
		:salt => pass[1],
		:role => x.role,
		:website => x.website,
		:css => x.css,
		:info => x.description,
		:created_at => x.created
		)
	@user.save
	users << [x.id.to_s, @user.id]
end
users = users.to_h
nodes = nodes.to_h
topics = []
Old::Topic.all.each do |x|
	@topic = New::Topic.new(
		:title => x.title,
		:content => x.content,
		:author => users[x.author_id.to_s],
		:node => nodes[x.node_id.to_s],
		:created_at => x.created,
		:updated_at => x.updated,
		:old_id => x.id
	)
	@topic.save
	topics << [x.id.to_s, @topic.id]
end
topics = topics.to_h
Old::Reply.all.each do |x|
	New::Reply.create(
		:content => x.content,
		:topic => topics[x.topic_id.to_s],
		:author => users[x.author_id.to_s],
		:created_at => x.created,
	)
end
New::Topic.all.each do |x| 
	x.update(:last_replied_at => x.updated_at) 
end
New::Reply.all.each do |x| 
	New::Topic.where(id: x.topic)[0].update(:last_replied_at => x.created_at) 
end
puts "Enjoy 0.0"


