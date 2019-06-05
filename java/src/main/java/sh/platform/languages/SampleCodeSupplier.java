package sh.platform.languages;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.Supplier;
import java.util.logging.Logger;
import java.util.stream.Collectors;

public class SampleCodeSupplier implements Supplier<Map<SampleCodeType, SampleCode>> {

    private static final Logger LOGGER = Logger.getLogger(SampleCodeSupplier.class.getName());

    private final Map<SampleCodeType, SampleCode> cached = new EnumMap<>(SampleCodeType.class);

    {
        LOGGER.info("Starting the loading SampleCodeType process");
        for (SampleCodeType available : SampleCodeType.values()) {
            final String source = convert(available.getFile());
            cached.put(available, new SampleCode(available, source, available.getDemoClass()));
        }
        LOGGER.info("Loading process complete.");

    }

    private String convert(String file) {
        final InputStream stream = SampleCodeSupplier.class.getClassLoader().getResourceAsStream(file);
        try (BufferedReader br = new BufferedReader(new InputStreamReader(stream, StandardCharsets.UTF_8))) {
            return br.lines().collect(Collectors.joining(System.lineSeparator()));
        } catch (IOException e) {
            throw new LanguageException("An error occurred when loading file", e);
        }
    }

    @Override
    public Map<SampleCodeType, SampleCode> get() {
        return cached;
    }
}
