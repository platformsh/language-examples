package sh.platform.languages;

import java.lang.reflect.Method;
import java.util.logging.Level;
import java.util.logging.Logger;

final class SampleCode {

    private static final Logger LOGGER = Logger.getLogger(SampleCode.class.getName());

    private static final Class[] ARG = new Class[]{String[].class};
    private static final Object NO_ARGS = new String[0];

    private final String source;

    private final Object intance;

    private final Method mainMethod;

    SampleCode(String source, Object intance) throws NoSuchMethodException {
        this.source = source;
        this.intance = intance;
        this.mainMethod = intance.getClass().getDeclaredMethod("main", ARG);
    }

    public String getSource() {
        return source;
    }

    public Object getIntance() {
        return intance;
    }

    public boolean executeWithSuccess() {
        try {
            mainMethod.invoke(null, NO_ARGS);
            return true;
        } catch (Exception exp) {
            LOGGER.log(Level.SEVERE, "an error happened when executing the demo code", exp);
            return false;
        }


    }
}
