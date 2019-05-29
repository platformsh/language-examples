package sh.platform.languages;

import com.google.gson.Gson;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public enum SamplesAvailable {
    MONGODB("MongoDBSample.java", "MongoDB"),
    MYSQL("MySQLSample.java", "MySQL"),
    POSTGRESQL("PostgreSQLSample.java", "PostgreSQL"),
    REDIS("RedisSample.java", "Redis");

    private final String file;
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

    SamplesAvailable(String file, String name) {
        this.file = file;
        this.name = name;
    }


    public String getFile() {
        return file;
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