package sh.platform.languages.sample;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import sh.platform.config.Config;
import sh.platform.config.Redis;

import java.util.Set;

public class RedisSample {

    public static void main(String[] args) {
        Config config = new Config();
        Redis database = config.getCredential("redis", Redis::new);
        JedisPool dataSource = database.get();
        final Jedis jedis = dataSource.getResource();
        jedis.sadd("cities", "Salvador");
        jedis.sadd("cities", "London");
        jedis.sadd("cities", "São Paulo");

        Set<String> cities = jedis.smembers("cities");
        System.out.println("cities: " + cities);
        jedis.del("cities");
    }
}
