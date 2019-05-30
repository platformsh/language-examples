package sh.platform.languages;


import org.eclipse.jetty.server.Connector;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.servlet.ServletHandler;
import org.eclipse.jetty.util.thread.QueuedThreadPool;

import java.util.logging.Logger;

import static java.lang.String.format;
import static java.util.Optional.ofNullable;

class JettyServer {

    private static final Logger LOGGER = Logger.getLogger(JettyServer.class.getName());

    private static final int DEFAULT_MAX_THREADS = 100;
    private static final int DEFAULT_MIN_THREADS = 10;
    private static final int DEFAULT_IDLE = 120;
    private static final int DEFAULT_PORT = 8080;

    private Server server;

    private static final String PORT = "jetty.port";
    private static final String MAX_THREADS = "jetty.max.threads";
    private static final String MIN_THREADS = "jetty.min.threads";
    private static final String IDLE = "jetty.idle";

    void start() throws Exception {

        int maxThreads = getProperty(MAX_THREADS, DEFAULT_MAX_THREADS);
        int minThreads = getProperty(MIN_THREADS, DEFAULT_MIN_THREADS);
        int idleTimeout = getProperty(IDLE, DEFAULT_IDLE);
        int port = getProperty(PORT, DEFAULT_PORT);
        LOGGER.info(format("Starting the Jetty server with  %d max threads, %d min threads, %d idle, %d port",
                maxThreads, minThreads, idleTimeout, port));

        LOGGER.info("Available services: " + SampleCodeType.getOptions());

        QueuedThreadPool threadPool = new QueuedThreadPool(maxThreads, minThreads, idleTimeout);

        server = new Server(threadPool);
        ServerConnector connector = new ServerConnector(server);
        connector.setPort(port);
        server.setConnectors(new Connector[]{connector});

        ServletHandler servletHandler = new ServletHandler();
        server.setHandler(servletHandler);

        servletHandler.addServletWithMapping(SampleServlet.class, "/java/*");
        server.start();
        LOGGER.info("Jetty server ready");
    }

    private Integer getProperty(String key, int defaultValue) {
        return ofNullable(System.getProperty(key)).map(Integer::parseInt).orElse(defaultValue);
    }

    void stop() throws Exception {
        server.stop();
    }
}
