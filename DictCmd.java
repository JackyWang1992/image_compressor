import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Pattern;

public class DictCmd {

    public static void main(String[] args) throws IOException {
	// write your code here
        Scanner sc = new Scanner(System.in);
        System.out.print(Message.WELCOME);
        String quit;
        String source = "";

        do {
            System.out.print(Message.NEW_COMMAND);
            System.out.print(Message.FILENAME);
            System.out.print(Message.NEW_COMMAND);
            String filename = sc.nextLine();
            System.out.print(Message.NEW_COMMAND);
            System.out.print(Message.MODE);
            System.out.print(Message.NEW_COMMAND);
            int mode = sc.nextInt();
            sc.nextLine();
            System.out.print(Message.NEW_COMMAND);
            System.out.print(Message.DELETION_OPTIONS);
            System.out.print(Message.NEW_COMMAND);
            int del = sc.nextInt();
            sc.nextLine();
            System.out.print(Message.NEW_COMMAND);
            System.out.print(Message.PURPOSE);
            System.out.print(Message.NEW_COMMAND);
            String purpose = sc.nextLine();
            if (purpose.equals("C") || purpose.equals("compress")) {
                String content = new String(Files.readAllBytes(Paths.get(filename)), StandardCharsets.ISO_8859_1);
                source = content;
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
            } else {
                InputStream is = new FileInputStream(filename);
                DataInputStream dis =  new DataInputStream(is);
                List<Short> content = new ArrayList<>();
                while (dis.available() > 0) {
                    short s = dis.readShort();
                    content.add(s);
                }
                DictDecompressor dd = new DictDecompressor(mode, del, content);
                dd.decompress();
                String output = dd.getResult();
                System.out.println(source.equals(output));
                try (BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
                    new FileOutputStream(filename.split(Pattern.quote("."))[0] + "-" + "decompressed.txt"), "ISO-8859-15"))) {
                    bw.write(output);
                }
                System.out.print(Message.NEW_COMMAND);
                System.out.printf(Message.DECOMPRESS_FINISH.toString(), filename.split(Pattern.quote("."))[0] + "-" + "decompressed.txt");
            }
            System.out.print(Message.NEW_COMMAND);
            System.out.print(Message.QUIT);
            System.out.print(Message.NEW_COMMAND);
            quit = sc.nextLine();
        } while (!quit.equals("quit"));
        System.out.print(Message.GOODBYE);
    }
}
