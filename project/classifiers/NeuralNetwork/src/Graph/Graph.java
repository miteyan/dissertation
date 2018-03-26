package Graph;

import Network.Dataset;
import Network.IncorrectLayerSizeException;
import Network.Network;
import Network.Utils;

import java.util.List;
import java.util.Random;

public class Graph {
    private static final double SPLIT[] = {0.6,0.2,0.2};
    final int NO_CLASSES = 2;

    final int NO_FEATURES;
    private final int DATASET_SIZE;
    final int TRAIN_SIZE;
    final int TEST_SIZE;
    private final int VALID_SIZE;

    List<double[]> data;
    Graph(final String data_file) {
        data = Utils.getData(data_file);

        this.DATASET_SIZE = data.size();
        this.NO_FEATURES = data.get(0).length-1;

        this.TRAIN_SIZE = (int) (SPLIT[0]*DATASET_SIZE);
        this.TEST_SIZE = (int) (SPLIT[1]*DATASET_SIZE);
        this.VALID_SIZE = (int) (SPLIT[2]*DATASET_SIZE);
    }

    private static double getRandom(double rangeMin, double rangeMax) {
        Random r = new Random();
        return rangeMin + (rangeMax - rangeMin) * r.nextDouble();
    }

    public void hyper_parameter_optimisation_weights() throws IncorrectLayerSizeException {
        Dataset trainSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 0, 5499);
        Dataset testSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 5500, 6000);

        double maxAccuracy = 0;
        double bestMinWeight = 0, bestMaxWeight = 0;

        for (int i = 0 ; i < 1000; i++) {
            double minWeight = getRandom(-10, -0.2);
            double maxWeight = getRandom(0.2, 10);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, 20, 7, NO_CLASSES);
            network.train(trainSet, 200, 500);

            double accuracy = Network.testTrainSet(network, testSet);

            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestMinWeight = minWeight;
                bestMaxWeight = maxWeight;
                System.out.println("New best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
            }
        }
        System.out.println("Best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
    }

    public void hyper_parameter_optimisation_size() throws IncorrectLayerSizeException {
        Dataset trainSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 0, 5499);
        Dataset testSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 5500, 6000);
        double minWeight = -4.3501209036059105, maxWeight = -4.3501209036059105;
        double maxAccuracy = 0;
        double bestLayer1 = 0, bestLayer2 = 0;

        for (int i = 0 ; i < 1000; i++) {
            double layer1 = getRandom(14,26);
            double layer2 = getRandom(0, 13);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, (int) layer1, (int) layer2, NO_CLASSES);
            network.train(trainSet, 200, 500);

            double accuracy = Network.testTrainSet(network, testSet);

            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestLayer1 = layer1;
                bestLayer2 = layer2;
                System.out.println("New best weights: [" + bestLayer1 + "," + bestLayer2 + "]");
            }
        }
        System.out.println("Best weights: [" + bestLayer1 + "," + bestLayer2 + "]");
    }

    public void hyper_parameter_optimisation_learning_rate() throws IncorrectLayerSizeException {
        Dataset trainSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 0, 5499);
        Dataset testSet = createBalancedTrainSet(data, NO_FEATURES, NO_CLASSES, 5500, 6000);
        double minWeight = -4.3501209036059105, maxWeight = -4.3501209036059105;
        double layer1 = 21, layer2 = 8;

        double maxAccuracy = 0;
        double bestLearningRate = 0;

        for (int i = 0 ; i < 1000; i++) {
            double learningRate = getRandom(0, 1);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, (int) layer1, (int) layer2, NO_CLASSES);
            network.train(trainSet, 200, 500);

            double accuracy = Network.testTrainSet(network, testSet);

            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestLearningRate = learningRate;
                System.out.println("New best learning rate: " + learningRate);
            }
        }
        System.out.println("Best learning rate: " + bestLearningRate);
    }

    static Dataset createBalancedTrainSet(List<double[]> data, int noFeatures, int noClasses, int start, int end) {
        Dataset set = new Dataset(noFeatures, noClasses);
        try {
            int num0 = 0, num1= 0;
            for (int i = start; i<= end; i++) {
                int o = (int)(data.get(i)[0]);
                if (o==0) {
                    num0++;
                } else {
                    num1++;
                }
            }
            int max = Math.min(num0, num1);
            System.out.println(max);

            int count0 = 0, count1 = 0;
            for(int i = start; i <= end; i++) {
                double[] input = new double[noFeatures];
                double[] output = new double[noClasses];
//                one hot encoding
                int o = (int) (data.get(i)[0]);
                if (o == 0) {
                    count0++;
                    if (count0 <= max) {
                        output[o] = 1d;
                        System.arraycopy(data.get(i), 1, input, 0, noFeatures);
                        set.addData(input, output);
                    }
                } else {
                    count1++;
                    if (count1 <= max) {
                        output[o] = 1d;
                        System.arraycopy(data.get(i), 1, input, 0, noFeatures);
                        set.addData(input, output);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return set;
    }

    static Dataset createTrainSet(List<double[]> data, int noFeatures, int noClasses, int start, int end) {
        Dataset set = new Dataset(noFeatures, noClasses);
        try {
            for(int i = start; i <= end; i++) {
                double[] input = new double[noFeatures];
                double[] output = new double[noClasses];
//                one hot encoding
                int o = (int)(data.get(i)[0]);
                output[o] = 1d;
                System.arraycopy(data.get(i), 1, input, 0, noFeatures);
                set.addData(input, output);
                }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return set;
    }
}
