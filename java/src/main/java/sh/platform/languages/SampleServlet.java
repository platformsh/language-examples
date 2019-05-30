package sh.platform.languages;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.Optional;

import static java.util.Optional.ofNullable;

public class SampleServlet extends HttpServlet {

    private static final long serialVersionUID = -3462096228274971485L;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        final String pathInfo = ofNullable(request.getPathInfo()).orElse("/");
        switch (pathInfo) {
            case "/":
                response.setContentType("application/json");
                response.setStatus(HttpServletResponse.SC_OK);
                response.getWriter().println(SampleCodeType.getOptions());
                return;
            case "/postgresql":
                showSampleCode(response, SampleCodeType.POSTGRESQL);
                return;
            case "/mysql":
                showSampleCode(response, SampleCodeType.MYSQL);
                return;
            case "/mongodb":
                showSampleCode(response, SampleCodeType.MONGODB);
                return;
            case "/redis":
                showSampleCode(response, SampleCodeType.REDIS);
                return;
            case "/postgresql/output":
                executeCode(response, SampleCodeType.POSTGRESQL);
                return;
            case "/mysql/output":
                executeCode(response, SampleCodeType.MYSQL);
                return;
            case "/mongodb/output":
                executeCode(response, SampleCodeType.MONGODB);
                return;
            case "/redis/output":
                executeCode(response, SampleCodeType.REDIS);
            default:
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.setContentType("text/plain");
                response.getWriter().println("Sorry, no sample code is available.");
        }
    }

    private void showSampleCode(HttpServletResponse response, SampleCodeType key) throws IOException {
        final SampleCode sampleCode = SampleCodeType.getSample(key);
        response.setStatus(HttpServletResponse.SC_OK);
        response.setContentType("text/plain");
        response.getWriter().println(sampleCode.getSource());

    }

    private void executeCode(HttpServletResponse response, SampleCodeType key) throws IOException {
        final SampleCode sampleCode = SampleCodeType.getSample(key);
        response.setContentType("text/plain");
        try {
            String message = sampleCode.execute();
            response.setStatus(HttpServletResponse.SC_OK);
            response.getWriter().println(message);
        } catch (Exception exp) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.getWriter().println(exp.getMessage());
        }
    }
}
