package sh.platform.languages.compiler;

/**
 * Eclipse JNoSQL tries to optimize access at Getter, Setter,
 * and Constructors to write/read fields at Class. This Exception launch when there is an issue when trying to compile.
 */
class CompilerAccessException extends RuntimeException {

    /**
     * Constructs a new runtime exception with the specified detail message.
     *
     * @param message the message
     */
    CompilerAccessException(String message) {
        super(message);
    }

    /**
     * Constructs a new runtime exception with the specified detail message and cause.
     *
     * @param message the message
     * @param cause   the cause
     */
    CompilerAccessException(String message, Throwable cause) {
        super(message, cause);
    }
}