import java.util.List;

public class DictDecompressor {
  private Dictionary<Short, String> dict1;
  private Dictionary<String, Short> dict2;
  private int mode;
  private int delete;
  private List<Short> input;
  private StringBuilder output;
  private String preMatch = "";
  private String curMatch = "";
  private short keyCount;
  private double matchLength;
  private int count;
  private long allLength;
  private double maxMatchLength = 1.0;

  DictDecompressor(int md, int del, List<Short> content) {
    this.mode = md;
    this.delete = del;
    initDict();
    input = content;
    output = new StringBuilder();
    keyCount = 256;
  }

  void decompress() {
    if (mode == 0) {
      FC();
    } else {
      AP();
    }
  }

  private void AP() {
    int idx = 0;
    while (idx < input.size()) {
      short key = input.get(idx);
      findMatch(key);
      if (dict2.containsKey(curMatch)) {
          for (int i = 1; i <= curMatch.length(); i++) {
              String newValue = preMatch + curMatch.substring(0, i);
              updateDict(newValue);
          }
      } else {
        updateDict(curMatch);
      }
      preMatch = curMatch;
      idx++;
    }
  }

  private void FC() {
    int idx = 0;
    while (idx < input.size()) {
      short key = input.get(idx);
      findMatch(key);
      if (dict2.containsKey(curMatch)) {
          String newValue = preMatch + curMatch.charAt(0);
          updateDict(newValue);
      } else {
        updateDict(curMatch);
      }
      preMatch = curMatch;
      idx++;
    }
  }

  private void initDict() {
    int DICT_SIZE = 65536;
//    int DICT_SIZE = 258;
    dict1 = new Dictionary<>(DICT_SIZE);
    dict2 = new Dictionary<>(DICT_SIZE);
    for (short i = 0; i < 256; i++) {
      dict1.put(i, String.valueOf((char) i));
      dict2.put(String.valueOf((char) i), i);
    }
  }

  public void findMatch(short key) {
    if (!dict1.containsKey(key)) {
     curMatch = String.valueOf((char)key);
     output.append(curMatch);
     return;
    } else {
      curMatch = dict1.get(key);
      reverseVisit(curMatch);
      output.append(curMatch);
    }
    count++;
    allLength += curMatch.length();
    matchLength = allLength /(double) count;
    maxMatchLength = Math.max(maxMatchLength, matchLength);
  }

  String getResult() {
    return output.toString();
  }

  private void reverseVisit(String curMatch) {
    for (short j = 0; j < 256; j++)  {
      dict2.get(dict1.get(j));
    }
    for (int i = curMatch.length(); i >= 1; i--) {
      if (dict2.containsKey(curMatch.substring(0, i))) {
        dict1.get(dict2.get(curMatch.substring(0, i)));
      }
    }
  }

  private void updateDict(String newKey) {
    if (delete == 0) {
      if (!dict2.isFull()) {
        if (!dict2.containsKey(newKey)) {
          dict2.put(newKey, keyCount);
          dict1.put(keyCount, newKey);
          keyCount++;
        }
      }
    } else if (delete == 1) {
      if (!dict2.isFull()) {
        if (!dict2.containsKey(newKey)) {
          dict2.put(newKey, keyCount);
          dict1.put(keyCount, newKey);
          keyCount++;
        }
      } else if (dict2.isFull() && maxMatchLength - matchLength > 0.005) {
        initDict();
        keyCount = 256;
        if (!dict2.containsKey(newKey)) {
          dict2.put(newKey, keyCount);
          dict1.put(keyCount, newKey);
          keyCount++;
        }
      }
    } else {
      if (!dict2.isFull()) {
        if (!dict2.containsKey(newKey)) {
          dict2.put(newKey, keyCount);
          dict1.put(keyCount, newKey);
          keyCount++;
        }
      } else {
        if (!dict2.containsKey(newKey)) {
          short newKeyCount = dict1.keySet().iterator().next();
          dict2.put(newKey, newKeyCount);
          dict1.put(newKeyCount, newKey);
        }
      }
    }
  }
}
