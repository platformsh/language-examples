package sh.platform.languages;

import com.google.gson.Gson;
import sh.platform.languages.sample.MongoDBSample;
import sh.platform.languages.sample.MySQLSample;
import sh.platform.languages.sample.PostgreSQLSample;
import sh.platform.languages.sample.RedisSample;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.function.Supplier;

public enum SampleCodeType {

    MONGODB(new MongoDBSample(), "MongoDB"),
    MYSQL(new MySQLSample(), "MySQL"),
    POSTGRESQL(new PostgreSQLSample(), "PostgreSQL"),
    REDIS(new RedisSample(), "Redis");

    private final Supplier<String> demoClass;
    private final String name;
    private static final String JSON;
    private static final Map<SampleCodeType, SampleCode> SAMPLES;

    static {
        Map<String, String> options = new HashMap<>();
        for (SampleCodeType value : values()) {
            options.put(value.name.toLowerCase(Locale.US), value.name);
        }
        JSON = new Gson().toJson(options);
        SAMPLES = new SampleCodeSupplier().get();
    }

    SampleCodeType(Supplier<String> demoClass, String name) {
        this.demoClass = demoClass;
        this.name = name;
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
            if (value.name.equals(sample)) {
                return Optional.of(value);
            }
        }
        return Optional.empty();
    }
}
