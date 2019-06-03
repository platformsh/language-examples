package sh.platform.languages;

import com.google.gson.Gson;
import sh.platform.languages.sample.ElasticsearchSample;
import sh.platform.languages.sample.MemcachedSample;
import sh.platform.languages.sample.MongoDBSample;
import sh.platform.languages.sample.MySQLSample;
import sh.platform.languages.sample.PostgreSQLSample;
import sh.platform.languages.sample.RedisSample;
import sh.platform.languages.sample.SolrSample;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.function.Supplier;

public enum SampleCodeType {

    MONGODB(new MongoDBSample(), "MongoDB"),
    MYSQL(new MySQLSample(), "MySQL"),
    POSTGRESQL(new PostgreSQLSample(), "PostgreSQL"),
    REDIS(new RedisSample(), "Redis"),
    MEMCACHED(new MemcachedSample(), "Memcached"),
    ELASTICSEARCH(new ElasticsearchSample(), "Elasticsearch"),
    SORL(new SolrSample(), "Sorl");

    private final Supplier<String> demoClass;
    private final String label;
    private static final String JSON;
    private static final Map<SampleCodeType, SampleCode> SAMPLES;

    static {
        Map<String, String> options = new HashMap<>();
        for (SampleCodeType value : values()) {
            options.put(value.label.toLowerCase(Locale.US), value.label);
        }
        JSON = new Gson().toJson(options);
        SAMPLES = new SampleCodeSupplier().get();
    }

    SampleCodeType(Supplier<String> demoClass, String label) {
        this.demoClass = demoClass;
        this.label = label;
    }


    public String getFile() {
        return demoClass.getClass().getSimpleName() + ".java";
    }

    public Supplier<String> getDemoClass() {
        return demoClass;
    }

    public static String getOptions() {
        return JSON;
    }

    public static Map<SampleCodeType, SampleCode> getSamples() {
        return SAMPLES;
    }

    public static SampleCode getSample(SampleCodeType key) {
        return SAMPLES.get(key);
    }

    public static Optional<SampleCodeType> parse(String sample) {
        for (SampleCodeType value : values()) {
            if (value.name().equals(sample)) {
                return Optional.of(value);
            }
        }
        return Optional.empty();
    }
}
