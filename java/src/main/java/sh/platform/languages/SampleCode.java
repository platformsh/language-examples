package sh.platform.languages;

import java.util.function.Supplier;
import java.util.logging.Logger;

/**
 * It is the result of the compiled demo code in memory.
 * From this class, it will both execute the demo compiled demo code and show the Java demo source.
 * The Sample code class will execute the public <b>static void main method</b> on each demo compiled class.
 */
final class SampleCode {
    private static final Logger LOGGER = Logger.getLogger(SampleCode.class.getName());

    private final String source;

    private final Supplier<String> demoClass;

    SampleCode(String source, Supplier<String> demoClass)  {
        this.source = source;
        this.demoClass = demoClass;
    }

    public String getSource() {
        return source;
    }

    public String execute() {
        return demoClass.get();
    }
}
