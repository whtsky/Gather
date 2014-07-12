# Connection.new takes host and port.
#
#host = 'localhost'
#port = 27017
#
#database_name = case Padrino.env
#  when :development then 'gather_development'
#  when :production  then 'gather_production'
#  when :test        then 'gather_test'
#end

# Use MONGO_URI if it's set as an environmental variable.
#Mongoid::Config.sessions =
#  if ENV['MONGO_URI']
#    {default: {uri: ENV['MONGO_URI'] }}
#  else
#    {default: {hosts: ["#{host}:#{port}"], database: database_name}}
#  end

# If you want to use a YML file for config, use this instead:
#
Mongoid.load!(File.join(Padrino.root, 'config', 'database.yml'), Padrino.env)
#
# And add a config/database.yml file like this:
#   development:
#     sessions:
#       default:
#         database: gather_development
#         hosts:
#           - localhost:27017
#   production:
#     sessions:
#       default:
#         database: gather_production
#         hosts:
#           - localhost:27017
#   test:
#     sessions:
#       default:
#         database: gather_test
#         hosts:
#           - localhost:27017
#
#
# More installation and setup notes are on http://mongoid.org/en/mongoid/docs/installation.html#configuration
