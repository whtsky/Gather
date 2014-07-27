class User
  include Mongoid::Document
  include Mongoid::Timestamps # adds created_at and updated_at fields

  # field <name>, :type => <type>, :default => <value>
  field :name, :type => String
  field :email, :type => String
  field :hashed_password, :type => String
  field :salt, :type => String
  field :role, :type => String
  field :site, :type => String
  field :info, :type => String
  field :css, :type => String

  has_many :topics
  has_many :replies

  validates_presence_of :name, :email, :salt, :hashed_password
  validates_uniqueness_of :name, :email

  def self.get(hash)
    user = self.where(hash)
    if user.exists?
      user.first
    else
      nil
    end
  end

  def stuff?
    self.role == 'stuff' || self.role == 'admin'
  end
  
  def admin?
    self.role == 'admin'
  end

  def self.create_user hash 
    p = new_password hash["password"]
    u = self.new(
        name: hash["username"],
        email: hash["email"],
        hashed_password: p[:password],
        salt: p[:salt],
        role: 'user'
      )
    puts u
    nil
    u.id if u.save
  end

  def self.auth user, password
    u = self.any_of({name: user}, {email: user})
    nil
    if !!u.first
      p = get_salted_password(password, u.first.salt)
      u.first.id if !!(p == u.first.hashed_password)
    end
  end

  def self.new_password password
    salt = gen_salt
    pass = get_salted_password password, salt
    {salt: salt, password: pass}
  end

  def self.get_salted_password pwd, salt
    PBKDF2.new(:password=> "#{pwd}#{Gather::App.settings.password_srcret}", :salt=>salt, :iterations=>1000, :hash_function => :sha1).hex_string
  end

  def self.gen_salt
    chars = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a
    newpass = ""
    1.upto(8) { |i| newpass << chars[rand(chars.size-1)] }
    newpass
  end



  # You can define indexes on documents using the index macro:
  # index :field <, :unique => true>

  # You can create a composite key in mongoid to replace the default id using the key macro:
  # key :field <, :another_field, :one_more ....>
end
class GuestUser
  def guest?
    true
  end

  def role
    "guest"
  end

  # current_user.admin? returns false. current_user.has_a_baby? returns false.
  # (which is a bit of an assumption I suppose)
  def method_missing(m, *args)
    return false
  end
end
