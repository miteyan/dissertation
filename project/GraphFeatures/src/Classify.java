import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.xml.XMLClassifier;
import weka.core.*;
import weka.core.converters.ArffLoader;

import java.io.*;

public class Classify {

    private static final String TRAINING_DATA_SET_FILENAME="./src/emotion.arff";
    private static final String TESTING_DATA_SET_FILENAME="./src/emotion.arff";

    public static Instances getDataSet(String fileName) throws IOException {
        int classIdx = 0;
        ArffLoader loader = new ArffLoader();
        loader.setSource(new File(fileName));
        Instances dataSet = loader.getDataSet();
        dataSet.setClassIndex(classIdx);
        return dataSet;
    }

    public static void process() throws Exception {
        Instances trainingDataSet = getDataSet(TRAINING_DATA_SET_FILENAME);
        Instances testingDataSet = getDataSet(TESTING_DATA_SET_FILENAME);
        RandomForest forest = new RandomForest();
//        {'criterion': 'entropy', 'max_depth': 12, 'bootstrap': True, 'max_features': 12, 'n_estimators': 40}
        forest.setNumTrees(40);
        forest.buildClassifier(trainingDataSet);
        Evaluation eval = new Evaluation(trainingDataSet);
        eval.evaluateModel(forest, testingDataSet);
        /* Print the algorithm summary */
        System.out.println("** Decision Tress Evaluation with Datasets **");
        System.out.println(eval.toSummaryString());
        System.out.print(" the expression for the input data as per algorithm is ");
        System.out.println(forest);
        System.out.println(eval.toMatrixString());
        System.out.println(eval.toClassDetailsString());
        System.out.println(testingDataSet.firstInstance().toString());

        SerializationHelper.write(new FileOutputStream("./forest.model"), forest);
//        XMLClassifier xmlcls = new XMLClassifier();
//        ObjectOutputStream oos = new ObjectOutputStream(
//                new FileOutputStream("./trained.xml"));
//        xmlcls.clear();
//        oos.flush();
//        oos.close();
    }

    public static Instance getInstanceFromFeature(Features f) throws IOException {
        //Declaring attributes
        Attribute d1 = new Attribute("d1");
        Attribute d2 = new Attribute("d2");
        Attribute d3 = new Attribute("d3");
        Attribute d4 = new Attribute("d4");
        Attribute d5 = new Attribute("d5");
        Attribute d6 = new Attribute("d6");
        Attribute d7 = new Attribute("d7");
        Attribute d8 = new Attribute("d8");
        Attribute d9 = new Attribute("d9");
        Attribute d10 = new Attribute("d10");
        Attribute d11 = new Attribute("d11");
        Attribute d12 = new Attribute("d12");
        Attribute d13 = new Attribute("d13");
        Attribute d14 = new Attribute("d14");
        Attribute d15 = new Attribute("d15");
        Attribute d16 = new Attribute("d16");
        Attribute d17 = new Attribute("d17");
        Attribute d18 = new Attribute("d18");
        Attribute d19 = new Attribute("d19");
        Attribute d20 = new Attribute("d20");

        // Declare the class attribute along with its values contains two nominal values yes and no using FastVector. "ScheduledFirst" is the name of the class attribute
        FastVector fvClassVal = new FastVector(2);
        fvClassVal.addElement("1");
        fvClassVal.addElement("0");
        Attribute Class = new Attribute("ScheduledFirst", fvClassVal);
        // Declare the feature vector
        FastVector fvWekaAttributes = new FastVector(20);
        // Add attributes
        fvWekaAttributes.addElement(d1);
        fvWekaAttributes.addElement(d2);
        fvWekaAttributes.addElement(d3);
        fvWekaAttributes.addElement(d4);
        fvWekaAttributes.addElement(d5);
        fvWekaAttributes.addElement(d6);
        fvWekaAttributes.addElement(d7);
        fvWekaAttributes.addElement(d8);
        fvWekaAttributes.addElement(d9);
        fvWekaAttributes.addElement(d10);
        fvWekaAttributes.addElement(d11);
        fvWekaAttributes.addElement(d12);
        fvWekaAttributes.addElement(d13);
        fvWekaAttributes.addElement(d14);
        fvWekaAttributes.addElement(d15);
        fvWekaAttributes.addElement(d16);
        fvWekaAttributes.addElement(d17);
        fvWekaAttributes.addElement(d18);
        fvWekaAttributes.addElement(d19);
        fvWekaAttributes.addElement(d20);
        fvWekaAttributes.addElement(Class);
        Instances dataset = new Instances("graph_features", fvWekaAttributes, 0);
        //Creating a double array and defining values
        double[] attValues = new double[dataset.numAttributes()];
        attValues[0] = f.getNodes();
        attValues[1] = f.getEdges();
        attValues[2] = f.getMaxDegree();
        attValues[3] = f.getDensity();
        attValues[4] = f.getDiameter();
        attValues[5] = f.getRadius();
        attValues[6] = f.getCentreSize();
        attValues[7] = f.getMeanEccentricity();
        attValues[8] = f.getVarEccentricity();
        attValues[9] = f.getMeanClusteringCoefficient();
        attValues[10] = f.getVarClusteringCoefficient();
        attValues[11] = f.getMeanNodeBetweennessCentrality();
        attValues[12] = f.getVarNodeBetweennessCentrality();
        attValues[13] = f.getMeanShortestPathLength();
        attValues[14] = f.getVarShortestPathLength();
        attValues[15] = f.getMeanEdgeBetweenessCentrality();
        attValues[16] = f.getVarEdgeBetweenessCentrality();
        attValues[18] = f.getMeanPagerank();
        attValues[19] = f.getVarPagerank();
        //Create the new instance i1
        Instance i1 = new Instance(1.0, attValues);
        //Add the instance to the dataset (Instances) (first element 0)
        dataset.add(i1);
        //Define class attribute position
        dataset.setClassIndex(dataset.numAttributes()-1);
        return dataset.firstInstance();
    }

    public static void main(String[] args) throws Exception {
        process();
        Classifier cls = (Classifier) SerializationHelper.read("./forest.model");
//        ois.readObject();
//        ois.close();
        Instance i = getInstanceFromFeature(FeatureExtraction.getFeaturesFromDirectory("/Users/miteyan/dissertation/GraphFeatures/src/graphs/").get(0));
        System.out.println(i.toString());
        System.out.println(cls.classifyInstance(i));
    }

}
