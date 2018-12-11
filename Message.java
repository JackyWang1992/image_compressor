public enum Message {
    WELCOME("Welcome to the dict-compression tool.\n"),
    NEW_COMMAND("> "),
    FILENAME("Please enter the filename you want to process:\n"),
    GOODBYE("Thank you for using the Unix-ish command line. Goodbye!\n"),
    PURPOSE("compress(C) or decompress(D)?\n"),
    MODE("Which mode do you like? FC(0) or AP(1)?\n"),
    QUIT("exit(quit) the tool?\n"),
    DELETION_OPTIONS("FREEZE(0) RESTART(1) LRU(2)?\n"),
    COMPRESS_FINISH("compress finished with name %s! Cheers!\n"),
    DECOMPRESS_FINISH("decompress finished with name %s! Cheers!\n");

    private final String message;

    Message(String message) {
        this.message = message;
    }

    public String toString() {
        return this.message;
    }
}
