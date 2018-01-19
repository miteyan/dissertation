package uk.cam.ac.uk.mp781.clustering;

import java.io.*;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

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
    static ArrayList<String[]> readString(String fileContents) throws IOException {
        ArrayList<String[]> timeLocations = new ArrayList<>();
        for (String line : fileContents.split("\t")) {
            timeLocations.add(line.split(","));
        }
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

    static String createEdgeList(ArrayList<ClusterNode> clusterNodes) {
        if (clusterNodes.isEmpty()) {
            return "";
        }
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

    static String weightEdges(ArrayList<String> edges) {
        if (edges.isEmpty()) {
            return "";
        }
        Collections.sort(edges, String::compareToIgnoreCase);
        StringBuilder sb = new StringBuilder();
        double currCount = 1.0;
        String currEdge = edges.get(0);
        for (int i = 1; i < edges.size(); i++) {
            if (currEdge.equals(edges.get(i))) {
                currCount++;
            } else {
                sb.append(currEdge);
                sb.append(" ");
                sb.append(currCount);
                sb.append("\n");
                currCount = 1.0;
                currEdge = edges.get(i);
            }
        }
        return sb.toString();
    }

    static void writeFile(String fileName, String edge_list) throws IOException {
        FileOutputStream out = new FileOutputStream(fileName);
        out.write(edge_list.getBytes());
        out.close();
    }

    static String arrayToString(ArrayList<String> stringArrayList) {
        StringBuilder sb = new StringBuilder();
        for (String s : stringArrayList) {
            sb.append(s);
            sb.append("\n");
        }
        return sb.toString();
    }
    public static String cluster(String locations, int minElements, int minDistance) throws IOException, ParseException {
        ArrayList<String[]> timeLocations = readString(locations);
        ArrayList<LatLongTime> locationTimes = getLocations(timeLocations);

        DBSCAN dbscanClusterer = new DBSCAN(locationTimes, minElements, minDistance);
        System.out.println("Creating clusters.");
        ArrayList<ArrayList<LatLongTime>> clusters = dbscanClusterer.performClustering();
        System.out.println("Creating time list.");
        ArrayList<ClusterNode> timeList = getTimeList(clusters);
        System.out.println("Creating edge list.");
        String edgelist = createEdgeList(timeList);
        return edgelist;

    }

    public static void main(String[] args) throws IOException, ParseException {
//        String in_folder = "/var/storage/sandra/mdc_analysis/mdc_data/full_lausanne/nkWeek/week";
//        String out_folder = "/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters";
//        String in_folder = "/var/storage/miteyan/Dissertation/project/cluster/src/clustering/data";
//        System.out.println(out_folder);

        String x = "2018-01-19 16:44:37,40.0637114,-0.6736401\t2018-01-19 16:44:39,40.0637099,-0.6736379\t2018-01-19 16:45:10,40.0637183,-0.6736382\t2018-01-19 16:45:40,40.0637221,-0.6736287\t2018-01-19 16:46:10,40.0637226,-0.6736276\t2018-01-19 16:46:40,40.0637351,-0.6736201\t2018-01-19 16:47:10,40.0637422,-0.6736181\t2018-01-19 16:47:40,40.0637452,-0.6736171\t2018-01-19 16:48:10,40.0637388,-0.6736236\t2018-01-19 16:48:29,40.063738,-0.6736289\t2018-01-19 16:49:08,40.0637335,-0.6736298\t2018-01-19 16:49:50,40.0637347,-0.6736262\t2018-01-19 16:50:40,40.0637374,-0.6736376\t";
        String edgelist = cluster(x, 5, 5);

        System.out.println("Edgelist: " +edgelist);
        //        ArrayList<String[]> timeLocations = readCSV("/Users/miteyan/dissertation/project/cluster/src/clustering/data");
//
//        DistanceMetric distanceMetric = new DistanceMetric();
//        ArrayList<LatLongTime> locationTimes = getLocations(timeLocations);
//        int minElements = 10;
//        int minDistance = 7;
//        DBSCANClusterer dbscanClusterer = new DBSCANClusterer(locationTimes, minElements, minDistance, distanceMetric);
//
//        ArrayList<ArrayList<LatLongTime>> clusters = dbscanClusterer.performClustering();
//        System.out.println(clusters.size());
//        ArrayList<ClusterNode> clusterNodes = getTimeList(clusters);
//        System.out.println(clusterNodes.size());
//        ArrayList<String> edgelist = createEdgeList(clusterNodes);
//        System.out.println(edgelist.size());
//        System.out.println(edgelist);
//        cluster(in_folder, out_folder);
//        System.out.println("done");
//        System.out.println(isSorted(clusterNodes)); true
    }


}
