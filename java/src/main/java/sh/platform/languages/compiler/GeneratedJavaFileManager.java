package sh.platform.languages.compiler;

import javax.tools.FileObject;
import javax.tools.ForwardingJavaFileManager;
import javax.tools.JavaFileManager;
import javax.tools.JavaFileObject;

final class GeneratedJavaFileManager extends ForwardingJavaFileManager<JavaFileManager> {

    private final JavaCompilerClassLoader classLoader;

    public GeneratedJavaFileManager(JavaFileManager fileManager, JavaCompilerClassLoader classLoader) {
        super(fileManager);
        this.classLoader = classLoader;
    }

    @Override
    public JavaFileObject getJavaFileForOutput(Location location, String qualifiedName, JavaFileObject.Kind kind, FileObject sibling) {
        if (kind != JavaFileObject.Kind.CLASS) {
            throw new IllegalArgumentException("Unsupported kind (" + kind + ") for class (" + qualifiedName + ").");
        }
        JavaCompiledStream fileObject = new JavaCompiledStream(qualifiedName);
        classLoader.addJavaFileObject(qualifiedName, fileObject);
        return fileObject;
    }

    @Override
    public ClassLoader getClassLoader(Location location) {
        return classLoader;
    }

}