package Network;

import java.util.ArrayList;
import java.util.Arrays;

public class Dataset {
//  input feature size
    public final int INPUT_SIZE;
    // target/output
    public final int OUTPUT_SIZE;

    private ArrayList<double[][]> data = new ArrayList<>();

    public Dataset(int INPUT_SIZE, int OUTPUT_SIZE) {
        this.INPUT_SIZE = INPUT_SIZE;
        this.OUTPUT_SIZE = OUTPUT_SIZE;
    }

    public void addData(double[] in, double[] expected) {
        if(in.length != INPUT_SIZE || expected.length != OUTPUT_SIZE) return;
        data.add(new double[][]{in, expected});
    }

    public ArrayList<double[][]> getData() {
        return data;
    }

    //    extract a randomized batch from the trainset
    public Dataset extractBatch(int size) {
        if(size > 0 && size <= this.size()) {
            Dataset set = new Dataset(INPUT_SIZE, OUTPUT_SIZE);
            Integer[] ids = Utils.randomValues(0,this.size() - 1, size);
            for(Integer i: ids) {
                set.addData(this.getInput(i),this.getOutput(i));
            }
            return set;
        }else {
            System.out.println("ELSE");
            return this;
        }
    }

    public int size() {
        return data.size();
    }

    public double[] getInput(int index) {
        if(index >= 0 && index < size())
            return data.get(index)[0];
        else return null;
    }

    public double[] getOutput(int index) {
        if(index >= 0 && index < size())
            return data.get(index)[1];
        else return null;
    }
}
