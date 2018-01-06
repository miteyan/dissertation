package clustering;

/**
 * Interface for the implementation of distance metrics.
 *
 */
public class DistanceMetric {

    public final static double AVERAGE_RADIUS_OF_EARTH_KM = 6371;

    public double calculateDistance(LatLongTime val1, LatLongTime val2) throws DBSCANClusteringException {
        double lat1 = val1.getLatitude();
        double lon1 = val1.getLongitude();
        double lat2 = val2. getLatitude();
        double lon2 = val2.getLongitude();
//        double latDistance = Math.toRadians(userLat - venueLat);
//        double lngDistance = Math.toRadians(userLon - venueLng);
//
//        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
//                + Math.cos(Math.toRadians(userLat)) * Math.cos(Math.toRadians(venueLat))
//                * Math.sin(lngDistance / 2) * Math.sin(lngDistance / 2);
//
//        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//
//        return AVERAGE_RADIUS_OF_EARTH_KM * c / 1000;

//        double distance = Math.sqrt( (lat1-lat2)*(lat1-lat2) + (lon1-lon2)*(lon1-lon2));
        double distance = distFrom(lat1, lon1, lat2, lon2);
        return distance;
    }

    public static double distFrom(double lat1, double lng1, double lat2, double lng2) {
        double earthRadius = 6371000; //meters
        double dLat = Math.toRadians(lat2 - lat1);
        double dLng = Math.toRadians(lng2 - lng1);
        double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLng/2) * Math.sin(dLng/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        double dist = (double) (earthRadius * c);

        return dist;
    }


}