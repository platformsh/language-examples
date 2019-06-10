package sh.platform.languages;

import java.util.function.Supplier;

final class SampleCode {

    private final SampleCodeType type;

    private final String source;

    private final String htmlSource;

    private final Supplier<String> demoClass;

    SampleCode(SampleCodeType type, String source, Supplier<String> demoClass) {
        this.type = type;
        this.source = source;
        this.htmlSource = source.replace(System.lineSeparator(), "<br/>");
        this.demoClass = demoClass;
    }

    public String getSource() {
        return source;
    }

    public String getHtmlSource() {
        return htmlSource;
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
