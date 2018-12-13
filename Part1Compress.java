import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Pattern;

class Part1Compress {
  public static void main(String[] args) throws IOException {
    String filename = args[0];
    String content = new String(Files.readAllBytes(Paths.get(filename)), StandardCharsets.ISO_8859_1);
    int mode = Integer.valueOf(args[1]);
    int del = Integer.valueOf(args[2]);
    System.out.println("this is part1 compessor!");
    DictCompressor dc = new DictCompressor(mode, del, content);
    dc.compress();
    List<Short> output = dc.getResult();
    DataOutputStream os = new DataOutputStream(new FileOutputStream(
            filename.split(Pattern.quote("."))[0] + "-" + "compressed.dat"));
    for (short s : output) {
        os.writeShort(s);
    }
    os.close();
    System.out.print(Message.NEW_COMMAND);
    System.out.printf(Message.COMPRESS_FINISH.toString(), filename.split(Pattern.quote("."))[0] + "-" + "compressed.dat");
  }
}
