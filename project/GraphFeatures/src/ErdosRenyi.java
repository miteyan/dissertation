import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Collections;

public class ErdosRenyi {
    private Bernoulli b = new Bernoulli();

    public String createGraph(int nodes, double p, int minWeight, double weightP) {
        ArrayList<String> edges = new ArrayList<>();
        for (int k = 0; k < 10; k++) {
            for (int i = 0; i < nodes; i++) {
                for (int j = 0; j < nodes; j++) {
                    if (i != j && b.bernoulli(p)) {
                        if (b.bernoulli(0.5)) {
                            String edge = i + " " + j;
                            edges.add(edge);
                        }
                    }
                }
            }
        }
        Collections.sort(edges);
        return runLengthEncoding(edges, minWeight, weightP);
    }

    public String runLengthEncoding(ArrayList<String> list, int minWeight, double p) {
        String ret = "";
        String curr = list.get(0);
        int weight = 1;
        for (int i = 1; i < list.size(); i++) {
            String currEdge = list.get(i);
            if (curr.equals(currEdge)) {
                weight++;
            } else {
                String edgeWeight = curr + " " + weight;
                if (weight <= minWeight) {
//                    keep only half of the edges of weight less than 2
                    if (b.bernoulli(p)) {
                        ret += edgeWeight + "\n";
                    }
                } else {
                    ret += edgeWeight + "\n";
                }
                weight = 1;
                curr = currEdge;
            }
        }
        return ret;
    }

    void createDataset(int number, int nodes, double p, int minNodes, double weightP, String label) throws FileNotFoundException, UnsupportedEncodingException {
        for (int i = 0; i < number; i++) {
            PrintWriter writer = new PrintWriter("/Users/miteyan/dissertation/GraphFeatures/src/graphs"+label+"/"+i);
            ErdosRenyi e = new ErdosRenyi();
            writer.println(e.createGraph(nodes, p, minNodes, weightP));
            writer.close();
        }
    }

    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {
        ErdosRenyi r = new ErdosRenyi();
        r.createDataset(100, 50, 0.1, 5, 0.4, "1");
    }
}