package uk.ac.cam.cl.loclogger.graph;

public class LocationNode {
    private double longitude;
    private double latitude;

    public LocationNode(double latitude, double longitude) {
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public double getLatitude() {
        return latitude;
    }
}
