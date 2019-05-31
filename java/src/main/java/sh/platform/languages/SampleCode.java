package sh.platform.languages;

import java.util.function.Supplier;

final class SampleCode {

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
