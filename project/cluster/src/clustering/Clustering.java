package clustering;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * Created by miteyan on 04/01/18.
 */
public class Clustering {

    static ArrayList<String[]> readCSV(String file) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader(file));
        String line = reader.readLine();
        ArrayList<String[]> timeLocations = new ArrayList<>();
        while ((line = reader.readLine()) != null) {
            timeLocations.add(line.split(","));
        }
        //close reader
        reader.close();
        return timeLocations;
    }
    static long dateToUnix(String date) throws ParseException {
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date d = dateFormat.parse(date);
        return d.getTime()/1000;
    }



    static ArrayList<LatLongTime> getLocations(ArrayList<String[]> timeLocations) throws ParseException {
        ArrayList<LatLongTime> ret = new ArrayList<>();
        for (String[] strings: timeLocations) {
            ret.add(new LatLongTime(Double.parseDouble(strings[1]), Double.parseDouble(strings[2]), dateToUnix(strings[0])));
        }
        return ret;
    }

    static ArrayList<ClusterNode> getTimeList(ArrayList<ArrayList<LatLongTime>> clusters) {
        ArrayList<ClusterNode> clusterNodes = new ArrayList<>();
        int clusterNo = 0;
        for (ArrayList<LatLongTime> cluster: clusters) {
            for (LatLongTime location: cluster) {
                clusterNodes.add(new ClusterNode(location.getTime(), clusterNo));
            }
            clusterNo++;
        }
        Collections.sort(clusterNodes, ClusterNode::compareTo);
        return clusterNodes;
    }

    static boolean isSorted(ArrayList<ClusterNode> clusterNodes) {
        long currTime = clusterNodes.get(0).getTime();
        for (ClusterNode clusterNode : clusterNodes) {
            if (currTime > clusterNode.time) {
                return false;
            }
        }
        return true;
    }

    static ArrayList<String> createEdgeList(ArrayList<ClusterNode> clusterNodes) {
        int currCluster = clusterNodes.get(0).getCluster();
        ArrayList<String> edges = new ArrayList<>();
        for (ClusterNode clusterNode : clusterNodes) {
            int cluster = clusterNode.getCluster();
            if (currCluster != cluster) {
                String line = currCluster + " " + cluster;
                edges.add(line);
                currCluster = cluster;
            }
        }
        return weightEdges(edges);
    }

    static ArrayList<String> weightEdges(ArrayList<String> edges) {
        Collections.sort(edges, String::compareToIgnoreCase);
        ArrayList<String> weightedEdges = new ArrayList<>();
        double currCount = 1.0;
        String currEdge = edges.get(0);
        for (int i = 1; i < edges.size(); i++) {
            if (currEdge.equals(edges.get(i))) {
                currCount++;
            } else {
                String weightedEdge = currEdge + " " + currCount;
                weightedEdges.add(weightedEdge);

                currCount = 1.0;
                currEdge = edges.get(i);
            }
        }
        return weightedEdges;
    }

    public static void main(String[] args) throws IOException, ParseException, DBSCANClusteringException {
        ArrayList<String[]> timeLocations = readCSV("/Users/miteyan/dissertation/project/cluster/src/clustering/test.csv");

        DistanceMetric distanceMetric = new DistanceMetric();
        ArrayList<LatLongTime> locationTimes = getLocations(timeLocations);

        DBSCANClusterer dbscanClusterer = new DBSCANClusterer(locationTimes, 2, 1, distanceMetric);
        ArrayList<ArrayList<LatLongTime>> clusters = dbscanClusterer.performClustering();

        ArrayList<ClusterNode> clusterNodes = getTimeList(clusters);

        ArrayList<String> edgelist = createEdgeList(clusterNodes);
        System.out.println(edgelist);

//        System.out.println(isSorted(clusterNodes)); true
    }

}
