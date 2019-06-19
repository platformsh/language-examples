package sh.platform.languages;

import java.util.function.Supplier;

final class SampleCode {

    private final SampleCodeType type;

    private final String source;

    private final Supplier<String> demoClass;

    SampleCode(SampleCodeType type, String source, Supplier<String> demoClass) {
        this.type = type;
        this.source = source;
        this.demoClass = demoClass;
    }

    public String getSource() {
        return source;
    }

    public String execute() {
        return demoClass.get();
    }

    public SampleCodeType getType() {
        return type;
    }

    public String getLabel() {
        return type.getLabel();
    }
}
