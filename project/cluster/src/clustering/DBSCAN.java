package clustering;

import java.util.ArrayList;
import java.util.HashSet;

/**
 * Created by miteyan on 04/01/18.
 */
public class DBSCAN{

    private final static double earthRadius = 6371000; //meters
    private double maxDistance;
    private int minClusterSize;
    private ArrayList<LatLongTime> inputValues;
    private HashSet<LatLongTime> visited;

    public DBSCAN(final ArrayList<LatLongTime> inputValues, int minClusterSize, double maxDistance) {
        this.inputValues = inputValues;
        this.minClusterSize = minClusterSize;
        this.maxDistance = maxDistance;
        this.visited = new HashSet<>();
    }

    public static double calculateDistance(LatLongTime val1, LatLongTime val2)  {
        double lat1 = val1.getLatitude();
        double lon1 = val1.getLongitude();
        double lat2 = val2.getLatitude();
        double lon2 = val2.getLongitude();
//        haversine formula
        double dLat = Math.toRadians(lat2 - lat1);
        double dLng = Math.toRadians(lon2 - lon1);
        double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLng/2) * Math.sin(dLng/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return earthRadius * c;
    }

    private ArrayList<LatLongTime> getNearby(LatLongTime point)  {
        ArrayList<LatLongTime> neighbours = new ArrayList<>();
        for (LatLongTime candidate : inputValues) {
            if (calculateDistance(point, candidate) <= maxDistance) {
                neighbours.add(candidate);
            }
        }
        return neighbours;
    }

    private static ArrayList<LatLongTime> merge(ArrayList<LatLongTime> list1, ArrayList<LatLongTime> list2) {
        for (LatLongTime point : list2) {
            if (!list1.contains(point)) {
                list1.add(point);
            }
        }
        return list1;
    }

    public ArrayList<ArrayList<LatLongTime>> performClustering() {
        ArrayList<ArrayList<LatLongTime>> resultList = new ArrayList<>();
        visited.clear();
        ArrayList<LatLongTime> cluster;
        int index = 0;

        while (inputValues.size() > index) {
            LatLongTime p = inputValues.get(index);
            if (!visited.contains(p)) {
                visited.add(p);
                cluster = getNearby(p);

                if (cluster.size() >= minClusterSize) {
                    int i = 0;
                    while (cluster.size() > i) {
                        LatLongTime r = cluster.get(i);
                        if (!visited.contains(r)) {
                            visited.add(r);
                            ArrayList<LatLongTime> individualNeighbours = getNearby(r);
                            if (individualNeighbours.size() >= minClusterSize) {
                                cluster = merge(cluster, individualNeighbours);
                            }
                        }
                        i++;
                    }
                    resultList.add(cluster);
                }
            }
            index++;
        }
        return resultList;
    }

}