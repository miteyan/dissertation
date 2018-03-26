package Mnist;

import Mnist.MNIST_Library.MnistImageFile;
import Mnist.MNIST_Library.MnistLabelFile;
import Network.*;

import java.io.File;
import java.io.IOException;
import java.util.Random;

public class Mnist {
//    each pixel in the 28x28 image is a feature
    static int NO_FEATURES = 784;
//    numbers 0-9 are the labels per image
    static final int NO_CLASSES = 10;

    private static final double TRAIN_SPLIT = 0.6;
    private static final double TEST_SPLIT = 0.2;
    private static final double VALID_SPLIT = 0.2;

    final int DATASET_SIZE = 10000;
    final int TRAIN_SIZE;
    final int TEST_SIZE;
    final int VALID_SIZE;

    Mnist() {
        this.TRAIN_SIZE = (int) (TRAIN_SPLIT*DATASET_SIZE);
        this.TEST_SIZE = (int) (TEST_SPLIT*DATASET_SIZE);
        this.VALID_SIZE = (int) (VALID_SPLIT*DATASET_SIZE);
    }

//    get optimal weights
    public static void hyper_parameter_optimisation() throws IncorrectLayerSizeException {
        Mnist m = new Mnist();

        Dataset trainSet = getDataset(0, 5999);
        Dataset validSet = getDataset(m.TRAIN_SIZE, m.TRAIN_SIZE + m.TEST_SIZE-1);
        double maxAccuracy = 0;
        double bestMinWeight = 0, bestMaxWeight = 0;

        for (int i = 0 ; i < 100; i++) {
            double minWeight = Utils.getRandom(-1, 0);
            double maxWeight = Utils.getRandom(0, 1);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, 70, 35, NO_CLASSES);
            network.train(trainSet, 100, 200);

            double accuracy = Network.test(network, validSet);

            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestMinWeight = minWeight;
                bestMaxWeight = maxWeight;
                System.out.println("New best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
            }
        }
        System.out.println("Best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
    }

    static Dataset getDataset(int start, int end) {
        Dataset set = new Dataset(NO_FEATURES, NO_CLASSES);
        try {
//            use MNIST library to retrieve the correct dataset
            String path = new File("").getAbsolutePath();
            MnistImageFile image = new MnistImageFile(path + "/test/res/train_data", "rw");
            MnistLabelFile label = new MnistLabelFile(path + "/test/res/train_label", "rw");
            for(int i = start; i <= end; i++) {
                double[] input = new double[28 * 28];
                double[] output = new double[10];
                output[label.readLabel()] = 1d;
                for(int j = 0; j < NO_FEATURES; j++){
                    input[j] = (double)image.read() / (double)256;
                }
                set.addData(input, output);
                image.next();
                label.next();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
         return set;
    }
}
