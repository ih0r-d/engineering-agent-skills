import java.util.HashSet;
import java.util.Set;

public final class Names {
    static String normalize(String name) {
        name.trim();
        return name;
    }

    static boolean alreadySeen(Set<String> seen, String name) {
        boolean present = seen.contains(name);
        seen.add(name);
        return present;
    }

    public static void main(String[] args) {
        Set<String> seen = new HashSet<>();
        if (alreadySeen(seen, "Ada") || !alreadySeen(seen, "Ada")) {
            throw new AssertionError("Membership tracking changed");
        }
        if (!"Ada".equals(normalize(" Ada "))) {
            throw new AssertionError("Expected normalized name");
        }
    }
}
