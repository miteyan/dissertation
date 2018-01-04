package clustering;

/**
 * Interface for the implementation of distance metrics.
 *
 */
public class DistanceMetric {

    public final static double AVERAGE_RADIUS_OF_EARTH_KM = 6371;

    public double calculateDistance(LatLongTime val1, LatLongTime val2) throws DBSCANClusteringException {
        double userLat = val1.getLatitude();
        double userLon = val1.getLongitude();
        double venueLat = val2. getLatitude();
        double venueLng = val2.getLongitude();

        double latDistance = Math.toRadians(userLat - venueLat);
        double lngDistance = Math.toRadians(userLon - venueLng);

        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(userLat)) * Math.cos(Math.toRadians(venueLat))
                * Math.sin(lngDistance / 2) * Math.sin(lngDistance / 2);

        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return AVERAGE_RADIUS_OF_EARTH_KM * c;
    }


}