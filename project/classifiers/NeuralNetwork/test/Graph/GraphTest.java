package Graph;

import Network.Dataset;
import Network.Network;
import Network.IncorrectLayerSizeException;
import org.junit.Test;

import java.util.ArrayList;

import static Graph.Graph.createTrainSet;

public class GraphTest {

    @Test
    public void testCreateBalancedTrainSet() throws Exception {
        Graph g = new Graph("/Users/miteyan/ai/MNIST/src/Graph/synthetic.csv");
        Dataset dataset = Graph.createBalancedTrainSet(g.data, g.NO_FEATURES, g.NO_CLASSES, 0, g.TRAIN_SIZE);
        ArrayList<double[][]> data = dataset.getData();
        int count0 = 0;
        int count1 = 0;
        for (double[][] dd: data) {
            if (dd[1][0] == 1) {
                count0++;
            } else if (dd[1][1] == 1) {
                count1++;
            }
        }
        System.out.println(count0);
        System.out.println(count1);
        assert count0 == count1;
    }

    @Test
    public void testGraphClassification() throws Exception, IncorrectLayerSizeException {
        Graph g = new Graph("/Users/miteyan/ai/MNIST/src/Graph/synthetic.csv");
        for (int i = 0 ; i < 5; i++) {
            Network network = new Network(-0.818929550189754, 0.4700354860851955, g.NO_FEATURES, 4, g.NO_CLASSES);
            Dataset trainSet = createTrainSet(g.data, g.NO_FEATURES, g.NO_CLASSES, 0, g.TRAIN_SIZE);
            Dataset testSet = createTrainSet(g.data, g.NO_FEATURES, g.NO_CLASSES, g.TRAIN_SIZE + 1, g.TRAIN_SIZE + g.TEST_SIZE);
            Network.trainData(network, trainSet, 4, 3, g.TRAIN_SIZE / 4);
            Network.testTrainSet(network, testSet);
        }
    }

}