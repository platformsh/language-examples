package sh.platform.languages;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

import static java.util.Optional.ofNullable;

public class SampleServlet extends HttpServlet {

    private static final long serialVersionUID = -3462096228274971485L;

    ;

    @Override
    protected void doGet(HttpServletRequest reqest, HttpServletResponse response)
            throws IOException {

        final String pathInfo = ofNullable(reqest.getPathInfo()).orElse("");
        switch (pathInfo) {
            case "/":
                response.setContentType("application/json");
                response.setStatus(HttpServletResponse.SC_OK);
                response.getWriter().println(SamplesAvailable.getOptions());
                return;
            case "/postgresql":
                showSampleCode(response, SamplesAvailable.POSTGRESQL);
                return;
            case "/mysql":
                showSampleCode(response, SamplesAvailable.MYSQL);
                return;
            case "/mongodb":
                showSampleCode(response, SamplesAvailable.MONGODB);
                return;
            case "/redis":
                showSampleCode(response, SamplesAvailable.REDIS);
                return;
            default:
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.setContentType("text/plain");
                response.getWriter().println("Sorry, no sample code is available.");
        }

    }

    private void showSampleCode(HttpServletResponse response, SamplesAvailable key) throws IOException {
        final SampleCode sampleCode = SamplesAvailable.getSample(key);
        if (sampleCode.executeWithSuccess()) {
            response.setStatus(HttpServletResponse.SC_OK);
            response.setContentType("text/plain");
            response.getWriter().println(sampleCode.getSource());
        } else {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            response.setContentType("text/plain");
            response.getWriter().println("There is an error when execute this service");
        }
    }
}