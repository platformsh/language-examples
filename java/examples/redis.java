import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import sh.platform.config.Config;
import sh.platform.config.Redis;

public class RedisSample {

    public static void main(String[] args) {
        Config config = new Config();
        Redis database = config.getCredential("database", Redis::new);
        JedisPool jedisPool = database.get();
        Jedis jedis = jedisPool.getResource();
    }
}
