package sh.platform.languages;

import com.google.gson.Gson;
import sh.platform.languages.sample.MongoDBSample;
import sh.platform.languages.sample.MySQLSample;
import sh.platform.languages.sample.PostgreSQLSample;
import sh.platform.languages.sample.RedisSample;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public enum SamplesAvailable {

    MONGODB(MongoDBSample.class, "MongoDB"),
    MYSQL(MySQLSample.class, "MySQL"),
    POSTGRESQL(PostgreSQLSample.class, "PostgreSQL"),
    REDIS(RedisSample.class, "Redis");

    private final Class<?> demoClass;
    private final String name;
    private static final String JSON;
    private static final Map<SamplesAvailable, SampleCode> SAMPLES;

    static {
        Map<String, String> options = new HashMap<>();
        for (SamplesAvailable value : values()) {
            options.put(value.name.toLowerCase(Locale.US), value.name);
        }
        JSON = new Gson().toJson(options);
        SAMPLES = new SampleCodeSupplier().get();
    }

    SamplesAvailable(Class<?> demoClass, String name) {
        this.demoClass = demoClass;
        this.name = name;
    }


    public String getFile() {
        return demoClass.getSimpleName() + ".java";
    }

    public Class<?> getDemoClass() {
        return demoClass;
    }

    public static String getOptions() {
        return JSON;
    }

    public static Map<SamplesAvailable, SampleCode> getSamples() {
        return SAMPLES;
    }

    public static SampleCode getSample(SamplesAvailable key) {
        return SAMPLES.get(key);
    }
}