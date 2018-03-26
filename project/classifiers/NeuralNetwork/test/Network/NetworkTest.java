package Network;

import org.junit.Test;

import java.util.Arrays;

public class NetworkTest {

    Network network = new Network(3, 2, 2);

    @Test
    public void sigmoid() {
        assert network.sigmoid(0) == 0.5;

        assert network.sigmoid(1) == 0.7310585786300049;

        assert network.sigmoid(-1) == 0.2689414213699951;
    }

    @Test
    public void testDecayLearningRate() {
        double decay = Network.decayLearningRate(0.3, 0.95, 1);
        decay = Network.decayLearningRate(decay, 0.95, 10);
        assert decay == 0.1706400276829379;
        decay = Network.decayLearningRate(decay, 0.95, 100);
        assert decay == 0.0010102792700554361;
    }

    @Test
    public void testFeedForward() throws IncorrectLayerSizeException {
        Network network = new Network(4, 5, 3, 4);
        double[] input = network.feedForward(0.2, 0.9, 0.3, 0.4);
        double[] target = new double[]{0, 1, 0, 0};
        for (int i = 0; i < 1000; i++) {
            network.train(input, target, 0.05);
        }
        double[] o = network.feedForward(input);
        System.out.println(Arrays.toString(o));
    }

    @Test
    public void testNetwork() throws IncorrectLayerSizeException {
        Network network1 = new Network(4, 3, 3, 2);
        Dataset set = new Dataset(4, 2);
        set.addData(new double[]{0.1,0.2,0.3,0.4}, new double[]{0.9,0.1});
        set.addData(new double[]{0.1,0.2,0.3,0.4}, new double[]{0.9,0.1});
        set.addData(new double[]{0.9,0.8,0.7,0.6}, new double[]{0.9,0.1});
        set.addData(new double[]{0.9,0.8,0.7,0.6}, new double[]{0.9,0.1});

        network1.train(set, 100, 4);
        for (int i = 0 ; i<4; i++) {
            System.out.println(Arrays.toString(network1.feedForward(set.getInput(i))));
        }
        double accuracy = network1.test(set);
        assert accuracy == 100.00;
    }
}