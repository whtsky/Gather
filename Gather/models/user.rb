class User
  include Mongoid::Document
  include Mongoid::Timestamps # adds created_at and updated_at fields

  # field <name>, :type => <type>, :default => <value>
  field :name, :type => String
  field :email, :type => String
  field :password, :type => String
  field :salt, :type => String
  field :role, :type => String
  field :site, :type => String
  field :info, :type => String
  field :css, :type => String

  has_many :topics
  has_many :replies

  validates_presence_of :name, :email, :salt, :password
  validates_uniqueness_of :name, :email

  def self.create_user hash 
    @p = self.new_password
    @u = self.new(
        name: hash[:name],
        email: hash[:email],
        password: @p[:password],
        salt: @p[:salt],
        role: 'user'
      )
    nil
    @u.id if @u.save
  end

  # You can define indexes on documents using the index macro:
  # index :field <, :unique => true>

  # You can create a composite key in mongoid to replace the default id using the key macro:
  # key :field <, :another_field, :one_more ....>
end
