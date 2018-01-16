package clustering;

import java.io.*;
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
        clusterNodes.sort(ClusterNode::compareTo);
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
        edges.sort(String::compareToIgnoreCase);
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

    private static void cluster(String inFolder, String outFolder) throws IOException, ParseException {
        File dir = new File(inFolder);
        File[] directoryListing = dir.listFiles();

        int minElements = 5;
        int minDistance = 5;//metres

        if (directoryListing != null) {
            for (File file : directoryListing) {
                String filename = new StringBuilder().append(outFolder).append("/").append(file.getName().substring(0, file.getName().length()-4)).toString();
                File f = new File(filename);
                // if file exists:
                if (!f.exists() && !f.getName().equals("60250_2009_45.csv")) {

                    System.out.println(file.getName());
                    ArrayList<String[]> timeLocations = readCSV(file.getAbsolutePath());
                    ArrayList<LatLongTime> locationTimes = getLocations(timeLocations);
                    DBSCAN dbscanClusterer = new DBSCAN(locationTimes, minElements, minDistance);

                    String edgelist = createEdgeList(
                            getTimeList(
                                    dbscanClusterer.performClustering()));
                    if (!edgelist.isEmpty()) {
                        writeFile(filename, edgelist);
                    }
                } else {
                    System.out.println("skipping: "+ filename);

                }
            }
        }
    }

    public static void main(String[] args) throws IOException, ParseException {
        String in_folder = "/var/storage/sandra/mdc_analysis/mdc_data/full_lausanne/nkWeek/week";
        String out_folder = "/var/storage/miteyan/Dissertation/project/cluster/src/clustering/week_clusters";
//        String in_folder = "/var/storage/miteyan/Dissertation/project/cluster/src/clustering/data";
        System.out.println(out_folder);
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

        cluster(in_folder, out_folder);
        System.out.println("done");
//        System.out.println(isSorted(clusterNodes)); true
    }


}
