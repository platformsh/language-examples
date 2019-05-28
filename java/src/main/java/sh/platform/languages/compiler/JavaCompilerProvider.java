package sh.platform.languages.compiler;

import sh.platform.languages.JavaSource;

import java.util.function.Function;

public class JavaCompilerProvider implements Function<JavaSource, Object> {

    private JavaCompilerFacade facade = new JavaCompilerFacade(JavaCompilerProvider.class.getClassLoader());

    @Override
    public Object apply(JavaSource source) {

        try {

            return facade.apply(source).getDeclaredConstructors()[0].newInstance();
        } catch (Exception exp) {
            throw new RuntimeException(exp);
        }
    }
}
