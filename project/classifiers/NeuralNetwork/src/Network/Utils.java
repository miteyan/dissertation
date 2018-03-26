package Network;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Utils {

    public static double[] meanVar(ArrayList<Double> list) {
        double sum = 0;
        double sum2 = 0;
        for (Double aList : list) {
            sum += aList;
            sum2 += aList * aList;
        }
        double mean = sum/list.size();
        double var = sum2/list.size() - mean*mean;
        System.out.println(mean);
        System.out.println(Math.sqrt(var));
        return new double[]{mean, var};
    }

    static double[] randomArray(int size, double l, double h) {
        double[] array = new double[size];
        for (int i = 0; i < size; i++) {
            array[i] = randomValue(l, h);
        }
        return array;
    }

    static double[][] randomArray(int r, int c, double lower, double upper) {
        double[][] array = new double[r][c];
        for (int i =0 ; i < r; i++) {
            array[i] = randomArray(c, lower,upper);
        }
        return array;
    }

    private static double randomValue(double l, double h) {
        return Math.random()*(h - l) + l;
    }

    public static double getRandom(double rangeMin, double rangeMax) {
        Random r = new Random();
        return rangeMin + (rangeMax - rangeMin) * r.nextDouble();
    }
    static Integer[] randomValues(int lowerBound, int upperBound, int amount) {
        Integer[] values = new Integer[amount];
        for(int i = 0; i< amount; i++){
            int n = (int)(Math.random() * (upperBound-lowerBound+1) + lowerBound);
            while(containsValue(values, n)){
                n = (int)(Math.random() * (upperBound-lowerBound+1) + lowerBound);
            }
            values[i] = n;
        }
        return values;
    }

    private static boolean containsValue(Integer[] ar, Integer value){
        for (Integer i : ar) {
            if (i != null) {
                if (i.equals(value)) {
                    return true;
                }
            }
        }
        return false;
    }

    public static int indexOfHighestValue(double[] values){
        int maxIndex = 0;
        for(int i = 1; i < values.length; i++){
            if(values[i] > values[maxIndex]){
                maxIndex = i;
            }
        }
        return maxIndex;
    }
    public static int getClass(double[] twoClasses){
        if (twoClasses[1]>0.5) {
            return 1;
        }
        return 0;
    }

    public static void printConfusion(int tn, int fp, int fn, int tp) {
        System.out.println(tn+ " " + fp);
        System.out.println(fn+ " " + tp);
    }

    private static void printArray(double[][] arr) {
        for (double[] anArr : arr) {
            for (int j = 0; j < arr[0].length; j++) {
                System.out.print(anArr[j]);
            }
            System.out.println();
        }
    }

    //10x784
    public static double[][] initialiseArray(int width, int height) {
        double[][] W = new double[height][width];
        Random rand = new Random();
        for (int y = 0; y < W.length; y++) {
            for (int x = 0; x < W[0].length; x++) {
                W[y][x] = rand.nextDouble();
            }
        }
        return W;
    }

    private static double[][] softmax(double[][] inputs) {
        double[][] outputs = new double[1][10];
        int sum = 0;
        for (int i = 0; i<inputs.length; i++) {
            sum += Math.exp(inputs[0][i]);
        }
        for (int i = 0; i<outputs.length; i++) {
            outputs[0][i] = Math.exp(inputs[0][i])/sum;
        }
        return outputs;
    }

    public static double[][] matrixMult(double[][] x, double[][] y) {
        if (x[0].length != y.length) {
            System.out.println("Incorrect matrix mult sizes");
            return null;
        }
        double[][] result = new double[x.length][y[0].length];

        for (int i = 0; i < x.length; i++) {
            for (int j = 0 ; j < y[0].length; j++) {
                for (int k = 0; k < x[0].length; k++) {
                    result[i][j] += x[i][k] * y[k][j];
                }
            }
        }
        return result;
    }

    public static double[][] matrixAdd(double[][] x, double[][] y) {
        for (int i = 0; i < x.length; i++) {
            for (int j = 0; j< x[0].length; j++) {
                x[i][j] += y[i][j];
            }
        }
        return x;
    }



    public static List<double[]> getData(String fileName) {
        List<double[]> list = new ArrayList<>();
        String line;

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            while ((line = br.readLine()) != null) {
                // use comma as separator
                String[] stringArray = line.split(",");
                double[] doubleA = new double[stringArray.length];
                for (int i = 0; i < stringArray.length; i++) {
                    doubleA[i] = Double.parseDouble(stringArray[i]);
                }
                list.add(doubleA);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return list;
    }

    public static void confusion(String x, String y) {
        String[] xx = x.split(" ");
        String[] yy = y.split(" ");

        int tn = 0;
        int fn = 0;
        int tp = 0;
        int fp = 0;
        int acc = 0;
        for (int i = 0 ; i < xx.length; i++) {
            if (xx[i].equals("0")) {
                if (yy[i].equals("0")) {
                    tn++;
                    acc++;
                } else {
                    fn++;
                }
            }
            if (xx[i].equals("1")) {
                if (yy[i].equals("1")) {
                    tp++;
                    acc++;
                } else {
                    fp++;
                }
            }
        }
        double precision = tp/(1.0*(tp + fp));
        double recall = tp/(1.0*(tp + fn));
        double f1 = 2*precision*recall/(1.0*(precision+ recall));
        System.out.println(precision);
        System.out.println(recall);
        System.out.println(f1);
        System.out.println(acc*1.0/xx.length);
    }


}
