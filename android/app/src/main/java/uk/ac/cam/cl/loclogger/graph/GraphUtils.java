package uk.ac.cam.cl.loclogger.graph;

import android.content.Context;

import java.io.File;

public class GraphUtils {
    public static void updateGraphFromLogFile(File locationLogFile, Context context) {
        // LocationGraph newGraph = constructGraph(locationLogFile, context);
        // TODO: Load location graph
        // TODO: Update and save location graph
    }

    private static LocationGraph constructGraph(File locationLogFile, Context context) {
        // See TestGraphUtils.java for prototype implementation
        return null;
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
