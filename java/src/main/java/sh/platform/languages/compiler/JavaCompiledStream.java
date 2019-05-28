package sh.platform.languages.compiler;


import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import javax.tools.SimpleJavaFileObject;

final class JavaCompiledStream extends SimpleJavaFileObject {

    private ByteArrayOutputStream classOutputStream;

    public JavaCompiledStream(String fullClassName) {
        super(URI.create("bytes:///" + fullClassName), Kind.CLASS);
    }

    @Override
    public InputStream openInputStream() {
        return new ByteArrayInputStream(getClassBytes());
    }

    @Override
    public OutputStream openOutputStream() {
        classOutputStream = new ByteArrayOutputStream();
        return classOutputStream;
    }

    public byte[] getClassBytes() {
        return classOutputStream.toByteArray();
    }

}