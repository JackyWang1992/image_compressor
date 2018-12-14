import java.util.LinkedHashMap;
import java.util.Map;

public class Dictionary<K, V> extends LinkedHashMap<K, V> {
    private int max_size;

    public Dictionary(int max_size) {
        super(max_size, 0.75f, true);
        this.max_size = max_size;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > max_size;
    }

    public boolean isFull() {
        return size() == max_size;
    }
}
