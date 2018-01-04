package clustering;

/**
 * Created by miteyan on 04/01/18.
 */
public class ClusterNode  implements Comparable<ClusterNode>{
    long time;
    int cluster;

    public long getTime() {
        return time;
    }

    public void setTime(long time) {
        this.time = time;
    }

    public int getCluster() {
        return cluster;
    }

    public void setCluster(int cluster) {
        this.cluster = cluster;
    }

    public ClusterNode(long time, int cluster) {
        this.time = time;
        this.cluster = cluster;
    }

    @Override
    public int compareTo(ClusterNode clusterNode) {
        if (this.time > clusterNode.time) {
            return 1;
        } else if (this.time == clusterNode.time) {
            return 0;
        }
        return -1;
    }

    @Override
    public String toString() {
        return "ClusterNode{" +
                "time=" + time +
                ", cluster=" + cluster +
                '}';
    }
}
