package uk.ac.cam.cl.loclogger.test;

import android.content.Context;
import android.util.Pair;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.LinkedList;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.graph.LocationEdge;
import uk.ac.cam.cl.loclogger.graph.LocationGraph;
import uk.ac.cam.cl.loclogger.graph.LocationNode;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class TestGraphUtils {

    public static LocationGraph constructGraph(Context context) {
        LocationGraph graph = createLocationGraph(context);
        InputStream is = context.getResources().openRawResource(context.getResources()
                .getIdentifier("location_log", "raw", context.getPackageName()));
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
            String line;

            LinkedList<Pair<Double, Double>> currentEdge = new LinkedList<>();
            HashSet<Pair<Double, Double>> currentNode = new HashSet<>();
            LocationNode previousNode = null;
            long currentStartTime = 0;
            long previousTimestamp = 0;

            while ((line = br.readLine()) != null) {
                try {
                    // Set up current point and reference point
                    JSONObject json = new JSONObject(line);
                    double currentLatitude = json.getJSONObject(ApplicationConstants.LOCATION)
                            .getDouble(ApplicationConstants.LOCATION_LATITUDE);
                    double currentLongitude = json.getJSONObject(ApplicationConstants.LOCATION)
                            .getDouble(ApplicationConstants.LOCATION_LONGITUDE);
                    double referenceLatitude;
                    double referenceLongitude;
                    if (!currentNode.isEmpty()) {
                        referenceLatitude = getMeanLatitude(currentNode);
                        referenceLongitude = getMeanLongitude(currentNode);
                    }
                    else {
                        currentStartTime = json.getLong(ApplicationConstants.TIMESTAMP);
                        previousTimestamp = currentStartTime;
                        currentNode.add(new Pair<>(currentLatitude, currentLongitude));
                        continue;
                    }

                    // Distance between this point and the previous one
                    double distance = getHaversineDistance(currentLatitude, currentLongitude,
                            referenceLatitude, referenceLongitude);

                    // If not close enough to centre of current node set, but dwell time was long
                    // enough, make a node out of set and begin new path.
                    if (distance > ApplicationConstants.NEW_LOCATION_DISTANCE_THRESHOLD_METRES) {
                        if (previousTimestamp - currentStartTime >
                                ApplicationConstants.NEW_LOCATION_TIME_THRESHOLD_MS) {

                            // Add node to graph
                            LocationNode newNode =
                                    new LocationNode(referenceLatitude, referenceLongitude);
                            graph.addVertex(newNode);
                            FileLogger.log("New node: (" + referenceLatitude + "," +
                                    referenceLongitude +
                                    ")", context);

                            if (previousNode != null) {
                                // Complete current edge
                                currentEdge.add(new Pair<Double, Double>(referenceLatitude,
                                        referenceLongitude));
                                // Add suitably weighted edge to graph
                                LocationEdge edge = graph.addEdge(previousNode, newNode);
                                graph.setEdgeWeight(edge, computeEdgeWeight(currentEdge));
                                FileLogger.log("New edge: (" + previousNode.getLatitude() + "," +
                                        previousNode.getLongitude() + ")," +
                                        "(" + newNode.getLatitude() + "," + newNode.getLongitude() +
                                        ")", context);
                            }
                            previousNode = newNode;

                        }
                        else {
                            // Otherwise just add centre to current edge
                            currentEdge.add(new Pair<Double, Double>(referenceLatitude,
                                    referenceLongitude));
                        }
                        currentNode.clear();
                        currentStartTime = json.getLong(ApplicationConstants.TIMESTAMP);
                    }
                    previousTimestamp = json.getLong(ApplicationConstants.TIMESTAMP);
                    currentNode.add(new Pair<Double, Double>(currentLatitude, currentLongitude));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return graph;
    }

    private static double computeEdgeWeight(LinkedList<Pair<Double, Double>> currentEdge) {
        double total = 0;
        for (int i = 1; i < currentEdge.size(); i++) {
            Pair<Double, Double> p1 = currentEdge.get(i - 1);
            Pair<Double, Double> p2 = currentEdge.get(i);
            total += getHaversineDistance(p1.first, p1.second, p2.first, p2.second);
        }
        return total;
    }

    private static double getMeanLongitude(HashSet<Pair<Double, Double>> currentNode) {
        double lon = 0;
        for (Pair<Double, Double> p : currentNode) {
            lon += p.second;
        }
        return lon / currentNode.size();
    }

    private static double getMeanLatitude(HashSet<Pair<Double, Double>> currentNode) {
        double lat = 0;
        for (Pair<Double, Double> p : currentNode) {
            lat += p.first;
        }
        return lat / currentNode.size();
    }

    private static double getHaversineDistance(double latitude1, double longitude1, double
            latitude2, double longitude2) {
        final int R = 6371; // Radius of the earth
        double latDistance = Math.toRadians(latitude2 - latitude1);
        double lonDistance = Math.toRadians(longitude2 - longitude1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2) +
                Math.cos(Math.toRadians(latitude1)) * Math.cos(Math.toRadians(latitude2)) *
                        Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        Double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = R * c * 1000; // convert to metres
        distance = Math.pow(distance, 2);
        return Math.sqrt(distance);
    }

    // Create a new, empty LocationGraph
    public static LocationGraph createLocationGraph(Context context) {
        return new LocationGraph(LocationEdge.class);
    }

    private static LocationGraph loadLocationGraph() {
        // TODO: load the current location graph
        return null;
    }

    private static void saveLocationGraph(LocationGraph graph) {
        // TODO: save location graph
    }

}
