import java.util.ArrayList;
import java.util.List;

public class DictCompressor {
  private Dictionary<String, Short> dict;
  private int mode;
  private int delete;
  private String input;
  private List<Short> output;
  private String preMatch = "";
  private String curMatch = "";
  private short keyCount;
  private double matchLength;
  private int count;
  private long allLength;
  private double maxMatchLength = 1.0;
  private int DICT_SIZE = 65536;

  DictCompressor(int md, int del, String fileString) {
    this.mode = md;
    this.delete = del;
    initDict();
    output = new ArrayList<>();
    input = fileString;
    keyCount = 256;
  }

  void compress() {
    if (mode == 0) {
      FC();
    } else {
      AP();
    }
  }

  private void AP() {
    int idx = 0;
    while (idx < input.length()) {
      idx = findMatch(idx);
      if (dict.containsKey(curMatch)) {
        for (int i = 1; i <= curMatch.length(); i++) {
          String newKey = preMatch + curMatch.substring(0, i);
          updateDict(newKey);
        }
      } else {
        updateDict(curMatch);
      }
      preMatch = curMatch;
    }
  }

  private void FC() {
    int idx = 0;
    while (idx < input.length()) {
      idx = findMatch(idx);
      if (dict.containsKey(curMatch)) {
        String newKey = preMatch + curMatch.charAt(0);
        updateDict(newKey);
      } else {
        updateDict(curMatch);
      }
      preMatch = curMatch;
    }
  }

  private int findMatch(int idx) {
    StringBuilder check = new StringBuilder();
    while (idx < input.length()) {
      check.append(input.charAt(idx));
      if (!dict.containsKey(check.toString()) && check.length() == 1) {
        curMatch = check.toString();
        output.add((short) curMatch.charAt(0));
        idx++;
        return idx;
      } else if (dict.containsKey(check.toString())) {
        curMatch = check.toString();
      } else {
        break;
      }
      idx++;
    }
    count++;
    allLength += curMatch.length();
    matchLength = allLength / (double) count;
    maxMatchLength = Math.max(maxMatchLength, matchLength);
    output.add(dict.get(curMatch));
    reverseVisit(curMatch);
    return idx;
  }

  private void reverseVisit(String curMatch) {
    for (short j = 0; j < 256; j++) {
      dict.get(String.valueOf((char)j));
    }
    for (int i = curMatch.length(); i >= 1; i--) {
      if (dict.containsKey(curMatch.substring(0, i))) {
        dict.get(curMatch.substring(0, i));
      }
    }
  }

  List<Short> getResult() {
    return output;
  }

  private void initDict() {
    dict = new Dictionary<>(DICT_SIZE);
    for (short i = 0; i < 256; i++) {
      dict.put(String.valueOf((char) i), i);
    }
  }

  private void updateDict(String newKey) {
    if (delete == 0) {
      if (!dict.isFull()) {
        if (!dict.containsKey(newKey)) {
          dict.put(newKey, keyCount);
          keyCount++;
        }
      }
    } else if (delete == 1) {
      if (!dict.isFull()) {
        if (!dict.containsKey(newKey)) {
          dict.put(newKey, keyCount);
          keyCount++;
        }
      } else if (dict.isFull() && maxMatchLength - matchLength > 0.005) {
        initDict();
        keyCount = 256;
        if (!dict.containsKey(newKey)) {
          dict.put(newKey, keyCount);
          keyCount++;
        }
      }
    } else {
        if (!dict.isFull()) {
            if (!dict.containsKey(newKey)) {
                dict.put(newKey, keyCount);
                keyCount++;
            }
        } else {
            if (!dict.containsKey(newKey)) {
                String oldKey = dict.keySet().iterator().next();
                short oldCount = dict.get(oldKey);
                dict.remove(oldKey);
                dict.put(newKey, oldCount);
            }
        }
    }
  }
}
