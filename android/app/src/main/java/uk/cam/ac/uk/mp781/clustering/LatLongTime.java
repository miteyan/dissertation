package uk.cam.ac.uk.mp781.clustering;

/**
 * Created by miteyan on 04/01/18.
 */
public class LatLongTime {
    private double latitude;
    private double longitude;
    private long time;

    public LatLongTime(double latitude, double longitude, long time) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.time = time;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public long getTime() {
        return time;
    }

    public void setTime(long time) {
        this.time = time;
    }
}
