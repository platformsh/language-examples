package sh.platform.languages;

import sh.platform.languages.compiler.JavaCompilerProvider;

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

public class SampleCodeSupplier implements Supplier<Map<SamplesAvailable, SampleCode>> {

    private static final Logger LOGGER = Logger.getLogger(SampleCodeSupplier.class.getName());

    private final JavaCompilerProvider compiler = new JavaCompilerProvider();

    private final Map<SamplesAvailable, SampleCode> cached = new EnumMap<>(SamplesAvailable.class);

    {
        LOGGER.info("Starting the compilation process");
        for (SamplesAvailable available : SamplesAvailable.values()) {
            final String source = convert(available.getFile());
            final Object instance = compiler.apply(new JavaSource(source, available.getFile()));
            try {
                cached.put(available, new SampleCode(source, instance));
            } catch (NoSuchMethodException e) {
                throw new LanguageException("Error when load sample code", e);
            }
        }
        LOGGER.info("Done the compilation process");

    }

    private String convert(String file) {
        final InputStream stream = SampleCodeSupplier.class.getClassLoader().getResourceAsStream(file);
        try (BufferedReader br = new BufferedReader(new InputStreamReader(stream, StandardCharsets.UTF_8))) {
            return br.lines().collect(Collectors.joining(System.lineSeparator()));
        } catch (IOException e) {
            throw new LanguageException("An error when load files", e);
        }
    }

    @Override
    public Map<SamplesAvailable, SampleCode> get() {
        return cached;
    }
}
