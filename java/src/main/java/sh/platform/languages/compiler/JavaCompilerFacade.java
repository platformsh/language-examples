package sh.platform.languages.compiler;


import sh.platform.languages.JavaSource;

import javax.tools.DiagnosticCollector;
import javax.tools.JavaCompiler;
import javax.tools.JavaCompiler.CompilationTask;
import javax.tools.JavaFileManager;
import javax.tools.ToolProvider;
import java.io.IOException;
import java.security.PrivilegedAction;
import java.util.Collections;
import java.util.Optional;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.security.AccessController.doPrivileged;

/**
 * Class that converts a {@link JavaSource} to a compiled class
 */
final class JavaCompilerFacade {

    private static final Pattern BREAK_LINE = Pattern.compile("\n");
    private final JavaCompilerClassLoader classLoader;
    private final JavaCompiler compiler;
    private final DiagnosticCollector<javax.tools.JavaFileObject> diagnosticCollector;

    JavaCompilerFacade(ClassLoader loader) {
        this.compiler = Optional.ofNullable(ToolProvider.getSystemJavaCompiler())
                .orElseThrow(() -> new IllegalStateException("Cannot find the system Java compiler"));

        PrivilegedAction<JavaCompilerClassLoader> action = () -> new JavaCompilerClassLoader(loader);
        this.classLoader = doPrivileged(action);
        this.diagnosticCollector = new DiagnosticCollector<>();
    }

    public Class<?> apply(JavaSource source) {
        return compile(source);
    }

    private synchronized Class<?> compile(JavaSource source) {
        JavaFileObject fileObject = new JavaFileObject(source.getSimpleName(), source.getJavaSource());

        JavaFileManager standardFileManager = compiler.getStandardFileManager(diagnosticCollector, null, null);

        try (GeneratedJavaFileManager javaFileManager = new GeneratedJavaFileManager(standardFileManager, classLoader)) {
            CompilationTask task = compiler.getTask(null, javaFileManager, diagnosticCollector,
                    null, null, Collections.singletonList(fileObject));

            if (!task.call()) {
                return createCompilerErrorMessage(source);
            }
        } catch (IOException e) {
            throw new CompilerAccessException("The generated class (" + source.getSimpleName() + ") failed to compile because the "
                    + JavaFileManager.class.getSimpleName() + " didn't close.", e);
        }
        try {
            Class<?> compiledClass = classLoader.loadClass(source.getName());
            return compiledClass;
        } catch (ClassNotFoundException e) {
            throw new CompilerAccessException("The generated class (" + source.getSimpleName()
                    + ") compiled, but failed to load.", e);
        }

    }

    private Class<?> createCompilerErrorMessage(JavaSource source) {
        String compilationMessages = diagnosticCollector.getDiagnostics().stream()
                .map(d -> d.getKind() + ":[" + d.getLineNumber() + "," + d.getColumnNumber() + "] "
                        + d.getMessage(null)
                        + "\n        " + (d
                        .getLineNumber() <= 0 ? "" : BREAK_LINE.splitAsStream(source.getJavaSource())
                        .skip(d.getLineNumber() - 1).findFirst().orElse("")))
                .collect(Collectors.joining("\n"));
        throw new CompilerAccessException("The generated class (" + source.getSimpleName() + ") failed to compile.\n"
                + compilationMessages);
    }
}