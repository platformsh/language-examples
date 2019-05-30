package sh.platform.languages.sample;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import sh.platform.config.Config;
import sh.platform.config.Redis;

import java.util.Set;

public class RedisSample {

    public static void main(String[] args) {
        // Create a new config object to ease reading the Platform.sh environment variables.
        // You can alternatively use getenv() yourself.
        Config config = new Config();
        // The 'database' relationship is generally the name of primary database of an application.
        // It could be anything, though, as in the case here here where it's called "redis".
        Redis database = config.getCredential("redis", Redis::new);
        JedisPool dataSource = database.get();
        // Get a Redis Client
        final Jedis jedis = dataSource.getResource();
        // Set a values
        jedis.sadd("cities", "Salvador");
        jedis.sadd("cities", "London");
        jedis.sadd("cities", "São Paulo");
        // Read it back.
        Set<String> cities = jedis.smembers("cities");
        System.out.println("cities: " + cities);
        jedis.del("cities");
    }
}
