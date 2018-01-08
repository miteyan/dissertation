import clustering.DBSCANClusterer;
import clustering.LatLongTime;

import java.util.ArrayList;

public class DBSCANClustererTest {

    ArrayList<LatLongTime> latLongTimes;
    LatLongTime l1 = new LatLongTime( 51.510357,-0.116773, 1);
    LatLongTime l2 = new LatLongTime( 51.510358,-0.116773, 12);
    LatLongTime l3 = new LatLongTime( 51.510359,-0.116773, 13);
    LatLongTime l4 = new LatLongTime( 51.510355,-0.116773, 14);
    LatLongTime l5 = new LatLongTime( 51.510356,-0.116773, 15);

    LatLongTime l6 = new LatLongTime( 38.889931,-77.009003, 2);
    LatLongTime l7 = new LatLongTime( 38.889935,-77.009003, 3);
    LatLongTime l8 = new LatLongTime( 38.889936,-77.009003, 4);

    DBSCANClusterer test;

    public DBSCANClustererTest() {
        latLongTimes = new ArrayList<>();

        latLongTimes.add(l1);
        latLongTimes.add(l2);
        latLongTimes.add(l3);
        latLongTimes.add(l4);
        latLongTimes.add(l5);
        latLongTimes.add(l6);
        latLongTimes.add(l7);
        latLongTimes.add(l8);
        test = new DBSCANClusterer(latLongTimes, 2,10);

    }

    @org.junit.Test
    public void calculateDistance() {
        double distance = DBSCANClusterer.calculateDistance(l1, l6);
        double answer = 5897658.289;
        assert Math.round(distance) == Math.round(answer);
    }

    @org.junit.Test
    public void performClustering() {
        ArrayList<ArrayList<LatLongTime>> clusters = test.performClustering();
        System.out.println(clusters.size());
        assert clusters.size() == 2;
        assert clusters.get(0).size() == 5;
        assert clusters.get(1).size() == 3;

    }
}
