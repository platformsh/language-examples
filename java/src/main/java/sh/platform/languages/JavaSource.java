package sh.platform.languages;


public class JavaSource {

    private final String source;

    private final String name;

    public JavaSource(String source, String name) {
        this.source = source;
        this.name = name.split("\\.")[0];
    }


    public String getSimpleName() {
        return name;
    }

    public String getName() {
        return "sh.platform.languages." + name;
    }

    public String getJavaSource() {
        return source;
    }


}
