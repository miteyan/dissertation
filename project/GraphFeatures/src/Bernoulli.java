import java.util.Random;

/**
 * Created by miteyan on 04/02/2018.
 */
public class Bernoulli {

    private Random r;

    public Bernoulli() {
        r = new Random();
    }

    public boolean bernoulli(double p) {
        if (r.nextDouble() > p) {
            return true;
        }
        return false;
    }
}
