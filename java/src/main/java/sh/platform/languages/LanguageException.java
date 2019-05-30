package sh.platform.languages;

public class LanguageException extends RuntimeException {
    public LanguageException(String message, Throwable exp) {
        super(message, exp);
    }
}
