import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Pattern;


class Part1Decompress{
  public static void main(String[] args) throws IOException {
    String filename = args[0];
    InputStream is = new FileInputStream(filename);
    DataInputStream dis =  new DataInputStream(is);
    List<Short> content = new ArrayList<>();
    while (dis.available() > 0) {
        short s = dis.readShort();
        content.add(s);
    }
    int mode = Integer.valueOf(args[1]);
    int del = Integer.valueOf(args[2]);
    System.out.println("this is part1 decompessor!");
    DictDecompressor dd = new DictDecompressor(mode, del, content);
    dd.decompress();
    String output = dd.getResult();
    try (BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
        new FileOutputStream(filename.split(Pattern.quote("."))[0] + ".csv"), "ISO-8859-15"))) {
        bw.write(output);
    }
    System.out.print(Message.NEW_COMMAND);
    System.out.printf(Message.DECOMPRESS_FINISH.toString(), filename.split(Pattern.quote("."))[0] + ".csv");
  }
}
