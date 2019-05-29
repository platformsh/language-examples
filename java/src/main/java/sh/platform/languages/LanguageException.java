package sh.platform.languages;

class LanguageException extends RuntimeException {

    public LanguageException(String message, Throwable e) {
        super(message, e);
    }
}