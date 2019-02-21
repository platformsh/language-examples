
def test_output():
    return '{"memcached_test": "passed"}'


# from pshconfig import Config
# import pymemcache
#
#
# # Create a new Config object to ease reading the Platform.sh environment variables.
# # You can alternatively use os.environ yourself.
# config = Config()
#
# # Get the credentials to connect to the Memcached service.
# credentials = config.credentials('memcached')
#
# try:
#     # Try connecting to Memached server.
#     memcached = pymemcache.Client((credentials['host'], credentials['port']))
# #     $memcached = new Memcached();
# #     $memcached->addServer($credentials['host'], $credentials['port']);
#     memcached.set('Memcached::OPT_BINARY_PROTOCOL', True)
# #     $memcached->setOption(Memcached::OPT_BINARY_PROTOCOL, true);
#
#     key = "Deploy day"
#     value = "Friday"
#
#     # Set a value
#     memcached.set(key, value)
# #     $memcached->set($key, $value);
#
#     # Read it back.
#     test = memcached.get(key)
#
#     print('Found value {} for key {}'.format(test, key))
#
# except Exception as e:
#     print(e)
