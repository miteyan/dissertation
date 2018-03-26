
import java.io.IOException;
import java.io.Writer;
import java.util.List;

public class CSVUtils {


    public static void writeLine(Writer w, String values) throws IOException {
        w.append(values + "\n");
    }

}