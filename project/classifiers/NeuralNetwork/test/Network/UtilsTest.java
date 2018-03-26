package Network;

import org.junit.Test;

import java.util.ArrayList;

/**
 * Created by miteyan on 26/03/2018.
 */
public class UtilsTest {
    @Test
    public void meanSqrt() throws Exception {
        ArrayList<Double> list = new ArrayList<>();
        list.add(1.0);
        list.add(2.0);
        list.add(3.0);
        list.add(4.0);
        list.add(5.0);
        double[] meanVar = Utils.meanVar(list);
        assert  meanVar[0] == 3.0;
        assert  meanVar[1] == 2.0;
    }

}