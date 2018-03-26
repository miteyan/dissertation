package Network;

import java.io.*;
import java.util.ArrayList;
import static Network.Utils.printConfusion;

public class Network implements Serializable{

//    can be learnt using hyper parameter optimisation
    private double LEARNING_RATE = 0.03;
    private final int[] NETWORK_LAYER_SIZES;
    private final int INPUT_SIZE;
    private final int OUTPUT_SIZE;
    private final int NETWORK_SIZE;

//    Network layers and nodes
    private double[][] outputs;
    private double[][][] weights;
    private double[][] bias;
    //Backpropogation
    private double[][] deltas;
    private double[][] output_derivates;

    Network(int... NETWORK_LAYER_SIZES) {
        this.NETWORK_LAYER_SIZES = NETWORK_LAYER_SIZES;
        this.INPUT_SIZE = NETWORK_LAYER_SIZES[0];
        this.NETWORK_SIZE = NETWORK_LAYER_SIZES.length;
        this.OUTPUT_SIZE = NETWORK_LAYER_SIZES[NETWORK_SIZE - 1];

        this.outputs = new double[NETWORK_SIZE][];
        this.weights = new double[NETWORK_SIZE][][];
        this.bias = new double[NETWORK_SIZE][];
        this.deltas = new double[NETWORK_SIZE][];
        this.output_derivates = new double[NETWORK_SIZE][];

        for (int i = 0; i < NETWORK_SIZE; i++) {
            this.outputs[i] = new double[NETWORK_LAYER_SIZES[i]];

            this.deltas[i] = new double[NETWORK_LAYER_SIZES[i]];
            this.output_derivates[i] = new double[NETWORK_LAYER_SIZES[i]];

//            initialize bias and weights to random values between -1,1. Wont work well without hyperparameter optimisation to find weights prior per problem.
            this.bias[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], -1,1);
            if (i > 0) {
                weights[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], NETWORK_LAYER_SIZES[i - 1], -1,1);
            }
        }
    }

    public Network(double weight1, double weight2, int... NETWORK_LAYER_SIZES) {
        this.NETWORK_LAYER_SIZES = NETWORK_LAYER_SIZES;
        this.INPUT_SIZE = NETWORK_LAYER_SIZES[0];
        this.NETWORK_SIZE = NETWORK_LAYER_SIZES.length;
        this.OUTPUT_SIZE = NETWORK_LAYER_SIZES[NETWORK_SIZE - 1];

        this.outputs = new double[NETWORK_SIZE][];
        this.weights = new double[NETWORK_SIZE][][];
        this.bias = new double[NETWORK_SIZE][];
        this.deltas = new double[NETWORK_SIZE][];
        this.output_derivates = new double[NETWORK_SIZE][];

        for (int i = 0; i < NETWORK_SIZE; i++) {
            this.outputs[i] = new double[NETWORK_LAYER_SIZES[i]];

            this.deltas[i] = new double[NETWORK_LAYER_SIZES[i]];
            this.output_derivates[i] = new double[NETWORK_LAYER_SIZES[i]];

//            initialize bias and weights to random values between 0.3,0.7
            this.bias[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], weight1, weight2);
            if (i > 0) {
                weights[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], NETWORK_LAYER_SIZES[i - 1], weight1, weight2);
            }
        }
    }

    public Network(double weight1, double weight2, double learning_rate, int... NETWORK_LAYER_SIZES) {
        this.NETWORK_LAYER_SIZES = NETWORK_LAYER_SIZES;
        this.INPUT_SIZE = NETWORK_LAYER_SIZES[0];
        this.NETWORK_SIZE = NETWORK_LAYER_SIZES.length;
        this.OUTPUT_SIZE = NETWORK_LAYER_SIZES[NETWORK_SIZE - 1];

        this.outputs = new double[NETWORK_SIZE][];
        this.weights = new double[NETWORK_SIZE][][];
        this.bias = new double[NETWORK_SIZE][];
        this.deltas = new double[NETWORK_SIZE][];
        this.output_derivates = new double[NETWORK_SIZE][];
        this.LEARNING_RATE = learning_rate;

        for (int i = 0; i < NETWORK_SIZE; i++) {
            this.outputs[i] = new double[NETWORK_LAYER_SIZES[i]];

            this.deltas[i] = new double[NETWORK_LAYER_SIZES[i]];
            this.output_derivates[i] = new double[NETWORK_LAYER_SIZES[i]];

//            initialize bias and weights to random values between 0.3,0.7
            this.bias[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], weight1, weight2);
            if (i > 0) {
                weights[i] = Utils.randomArray(NETWORK_LAYER_SIZES[i], NETWORK_LAYER_SIZES[i - 1], weight1, weight2);
            }
        }
    }

    public void train(double[] input, double[] target, double learningRate) throws IncorrectLayerSizeException {
        if (input.length != INPUT_SIZE || target.length != OUTPUT_SIZE) {
            throw new IncorrectLayerSizeException("Input and output layer sizes do not match.");
        }
        feedForward(input);
        backPropogationError(target);
        updateWeights(learningRate);
    }

    public double test(Dataset set) {
        int correct = 0;
        int truePos = 0, trueNeg = 0,  falsePos = 0, falseNeg = 0;
        for(int i = 0; i < set.size(); i++) {
            double[] lastLayer = this.feedForward(set.getInput(i));
            double highest = Utils.getClass(lastLayer);
            double actualHighest = Utils.indexOfHighestValue(set.getOutput(i));
//            System.out.println("highest: " + highest + " actual highest: " + actualHighest);
            if (highest == actualHighest)
                correct ++;
            if (highest == 0) {
                if (actualHighest == 0) {
                    trueNeg += 1;
                } else {
                    falseNeg += 1;
                }
            }
            if (highest == 1) {
                if (actualHighest == 1) {
                    truePos += 1;
                } else {
                    falsePos += 1;
                }
            }
        }
        printConfusion(trueNeg, falseNeg, falsePos, truePos);
        double accuracy = 100*(double)correct / (double)set.size();
        System.out.println("Test Accuracy " + correct + " / " + set.size()+ " = " + accuracy +"%");
        return accuracy;
    }

    public static double decayLearningRate(double learningRate0, double decayRate, int currStep) {
        return Math.pow(decayRate, (double)currStep)*learningRate0;
    }

    public void train(Dataset set, int loops, int batch_size) throws IncorrectLayerSizeException {
        if (set.INPUT_SIZE != INPUT_SIZE || set.OUTPUT_SIZE != OUTPUT_SIZE) return;
        Dataset batch = set.extractBatch(batch_size);
        for (int i = 0 ;i<loops; i++) {
            for (int b = 0; b < batch_size; b++) {
                this.train(batch.getInput(b), batch.getOutput(b), LEARNING_RATE);
            }
            if (i == loops-1) {
                System.out.print(MSE(batch)+",");
            }
        }
    }

    public double MSE(double[] input, double[] target) {
        if (input.length != INPUT_SIZE || target.length !=OUTPUT_SIZE) {
            return 0;
        }
        feedForward(input);
        double mse = 0;
        for (int i =0 ; i<target.length; i++) {
            mse += (target[i]-outputs[NETWORK_SIZE-1][i]) * (target[i] - outputs[NETWORK_SIZE-1][i]);
        }
        return mse/(target.length);
    }

    public double MSE(Dataset set) {
        double mse = 0;
        for (int i= 0; i<set.size(); i++) {
            mse += MSE(set.getInput(i), set.getOutput(i));
        }
        return mse/set.size();
    }

    private void backPropogationError(double[] target) {
        for (int neuron = 0; neuron < NETWORK_LAYER_SIZES[NETWORK_SIZE-1]; neuron++) {
            deltas[NETWORK_SIZE-1][neuron] = (outputs[NETWORK_SIZE-1][neuron] - target[neuron])
                    *output_derivates[NETWORK_SIZE-1][neuron];
        }
        //last hidden layer back to first/ input --> back prop
        for (int layer = NETWORK_SIZE - 2; layer > 0; layer--) {
            // for neurons in current layer
            for (int neuron = 0; neuron < NETWORK_LAYER_SIZES[layer]; neuron++) {
                double sum = 0;
                // set delta to derivative...
                for (int nextNeuron = 0 ; nextNeuron < NETWORK_LAYER_SIZES[layer+1] ; nextNeuron++) {
                    sum += weights[layer+1][nextNeuron][neuron] * deltas[layer+1][nextNeuron];
                }
                this.deltas[layer][neuron] = sum * output_derivates[layer][neuron];
            }
        }
    }

    private void updateWeights(double learningRate) {
        for (int layer = 1; layer < NETWORK_SIZE; layer++) {
            for (int neuron = 0 ; neuron<NETWORK_LAYER_SIZES[layer]; neuron++) {
                for (int prevNeuron = 0; prevNeuron < NETWORK_LAYER_SIZES[layer-1]; prevNeuron++) {
//                    bias and weights update by backpropogation.
                    weights[layer][neuron][prevNeuron] += -learningRate * outputs[layer-1][prevNeuron] * deltas[layer][neuron];

                }
                bias[layer][neuron] += - learningRate*deltas[layer][neuron];
            }
        }
    }
// feed forward
    public double[] feedForward(double... input) {
        if (input.length != INPUT_SIZE) {
            return null;
        }
//        since the first layer is just the input layer in a NN
        this.outputs[0] = input;
         for (int layer = 1; layer < NETWORK_SIZE; layer++) {
            for (int neuron = 0; neuron < NETWORK_LAYER_SIZES[layer]; neuron++) {
//                feedForward the cross product sum for each neuron
                //sum = weights*input + bias
                double sum = bias[layer][neuron];
                for (int prevNeuron = 0; prevNeuron < NETWORK_LAYER_SIZES[layer - 1]; prevNeuron++) {
                    sum += outputs[layer - 1][prevNeuron] * weights[layer][neuron][prevNeuron];
                }
//                apply the activation function (sigmoid).
                outputs[layer][neuron] = sigmoid(sum);
//                for back propogation
                output_derivates[layer][neuron] = outputs[layer][neuron]*(1 - outputs[layer][neuron]);
            }
        }
        return outputs[NETWORK_SIZE - 1];
    }

    public double sigmoid(double x) {
        return 1d / (1 + Math.exp(-x));
    }

    public void saveNetwork(String file) throws IOException {
        File f = new File(file);
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream(f));
        objectOutputStream.writeObject(this);
        objectOutputStream.flush();
        objectOutputStream.close();
    }

    public static Network loadNetwork(String file) throws IOException, ClassNotFoundException {
        File f = new File(file);
        ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream(f));
        Network net = (Network) objectInputStream.readObject();
        objectInputStream.close();
        return net;
    }

    public void hyper_parameter_optimisation_weights(Dataset trainSet, Dataset testSet, int NO_FEATURES, int NO_CLASSES) throws IncorrectLayerSizeException {
    double maxAccuracy = 0;
    double bestMinWeight = 0, bestMaxWeight = 0;

    for (int i = 0 ; i < 1000; i++) {
        double minWeight = Utils.getRandom(-10, -0.2);
        double maxWeight = Utils.getRandom(0.2, 10);
        Network network = new Network(minWeight, maxWeight, NO_FEATURES, 20, 7, NO_CLASSES);
        network.train(trainSet, 200, 500);

        double accuracy = test(testSet);

        if (accuracy > maxAccuracy) {
            maxAccuracy = accuracy;
            bestMinWeight = minWeight;
            bestMaxWeight = maxWeight;
            System.out.println("New best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
        }
    }
    System.out.println("Best weights: [" + bestMinWeight + "," + bestMaxWeight + "]");
}
    public void hyper_parameter_optimisation_size(Dataset trainSet, Dataset testSet, int NO_FEATURES, int NO_CLASSES) throws IncorrectLayerSizeException {
        double minWeight = -4.3501209036059105, maxWeight = -4.3501209036059105;
        double maxAccuracy = 0;
        double bestLayer1 = 0, bestLayer2 = 0;

        for (int i = 0 ; i < 1000; i++) {
            double layer1 = Utils.getRandom(14,26);
            double layer2 = Utils.getRandom(0, 13);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, (int) layer1, (int) layer2, NO_CLASSES);
            network.train(trainSet, 200, 500);

            double accuracy = test(testSet);

            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestLayer1 = layer1;
                bestLayer2 = layer2;
                System.out.println("New best weights: [" + bestLayer1 + "," + bestLayer2 + "]");
            }
        }
        System.out.println("Best weights: [" + bestLayer1 + "," + bestLayer2 + "]");
    }
    public void hyper_parameter_optimisation_learning_rate(Dataset trainSet, Dataset testSet, int NO_FEATURES, int NO_CLASSES) throws IncorrectLayerSizeException {
        double minWeight = -4.3501209036059105, maxWeight = -4.3501209036059105;
        double layer1 = 21, layer2 = 8;

        double maxAccuracy = 0;
        double bestLearningRate = 0;

        for (int i = 0 ; i < 1000; i++) {
            double learningRate = Utils.getRandom(0, 1);
            Network network = new Network(minWeight, maxWeight, NO_FEATURES, (int) layer1, (int) layer2, NO_CLASSES);
            network.train(trainSet, 200, 500);
            double accuracy = test(testSet);
            if (accuracy > maxAccuracy) {
                maxAccuracy = accuracy;
                bestLearningRate = learningRate;
                System.out.println("New best learning rate: " + learningRate);
            }
        }
        System.out.println("Best learning rate: " + bestLearningRate);
    }

    public static double test(Network net, Dataset set) {
        int correct = 0;
        for(int i = 0; i < set.size(); i++) {
            double highest = Utils.indexOfHighestValue(net.feedForward(set.getInput(i)));
            double actualHighest = Utils.indexOfHighestValue(set.getOutput(i));
            if(highest == actualHighest) {
                correct ++;
            }
        }
        double accuracy = 100*((double)correct / (double)set.size());
        System.out.println(accuracy +"%");
        return accuracy;
    }

    public static void train(Network net, Dataset set, int epochs, int loops, int batch_size, String file) throws IncorrectLayerSizeException {
        for(int e = 0; e < epochs; e++) {
            net.train(set, loops, batch_size);
            try {
                net.saveNetwork(file);
            } catch (IOException e1) {
                e1.printStackTrace();
            }
        }
    }

    public static void trainData(Network net, Dataset set, int epochs, int loops, int batch_size) throws IncorrectLayerSizeException {
        for(int e = 0; e < epochs; e++) {
            net.train(set, loops, batch_size);
        }
    }

    private static ArrayList<Double> precisions = new ArrayList<>();
    private static ArrayList<Double> recalls = new ArrayList<>();
    private static ArrayList<Double> f1s = new ArrayList<>();

    public static double testTrainSet(Network net, Dataset set) {
        int correct = 0;
        int truePos = 0, trueNeg = 0,  falsePos = 0, falseNeg = 0;
        for(int i = 0; i < set.size(); i++) {
            double[] lastLayer = net.feedForward(set.getInput(i));
            double highest = Utils.getClass(lastLayer);
            double actualHighest = Utils.indexOfHighestValue(set.getOutput(i));
//            System.out.println("highest: " + highest + " actual highest: " + actualHighest);
            if (highest == actualHighest)
                correct ++;
            if (highest == 0) {
                if (actualHighest == 0) {
                    trueNeg += 1;
                } else {
                    falseNeg += 1;
                }
            }
            if (highest == 1) {
                if (actualHighest == 1) {
                    truePos += 1;
                } else {
                    falsePos += 1;
                }
            }
        }
        double precision = truePos/(1.0*(truePos + falsePos));
        double recall = truePos/(1.0*(truePos + falseNeg));
        double f1 = 2*precision*recall/(1.0*(precision+ recall));
        precisions.add(precision);
        f1s.add(f1);
        recalls.add(recall);
//        printConfusion(trueNeg, falseNeg, falsePos, truePos);
        double accuracy = 100*(double)correct / (double)set.size();
        System.out.println("Test Accuracy " + correct + " / " + set.size()+ " = " + accuracy +"%");
        return accuracy;
    }

}
