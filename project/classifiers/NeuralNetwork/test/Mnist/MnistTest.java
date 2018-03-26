package Mnist;

import Network.Network;
import Network.Dataset;
import Network.IncorrectLayerSizeException;
import org.junit.Test;

import static Mnist.Mnist.*;

public class MnistTest {

    @Test
    public void testMNIST() throws IncorrectLayerSizeException {
        Mnist m = new Mnist();
        String file = "./test/res/test2.txt";
        Network network = new Network(-0.570855587444868, 0.6441470769429456, NO_FEATURES, 70, 35, NO_CLASSES);
        Dataset set = getDataset(0, m.TRAIN_SIZE);
        Network.train(network, set, 30, 10, 100, file);
        Dataset testSet = getDataset(m.TRAIN_SIZE, m.DATASET_SIZE - 1);
        Network.test(network, testSet);
    }

}