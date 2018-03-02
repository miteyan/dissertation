package uk.cam.ac.uk.mp781.feature_extraction;

import org.apache.commons.collections15.Transformer;
import org.apache.commons.collections15.functors.MapTransformer;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import edu.uci.ics.jung.algorithms.metrics.Metrics;
import edu.uci.ics.jung.algorithms.scoring.BetweennessCentrality;
import edu.uci.ics.jung.algorithms.scoring.PageRank;
import edu.uci.ics.jung.algorithms.shortestpath.DijkstraShortestPath;
import edu.uci.ics.jung.graph.DirectedSparseGraph;

public class FeatureExtraction {


    public static double getMean(int[] list) {
        Double sum = 0.0;
        for (int d : list) {
            sum += d;
        }
        return sum/list.length;
    }

    public static double getVariance(int[] list, double mean) {
        Double sum2 = 0.0;
        for (int d : list) {
            sum2 += d*d;
        }
        return sum2/list.length - mean*mean;
    }

    public static Features getFeaturesFromEdgeList(String edgeList) throws IOException {
        String[] edges = edgeList.split("\n");
        HashMap<Integer, Integer> map = new HashMap<>();
        DirectedSparseGraph<Integer, Integer> g = new DirectedSparseGraph();

        int count = 0;
        for (String edge : edges) {
            System.out.println(edge);
            String[] nodes = edge.split(" ");
            map.put(count, (int) Double.parseDouble(nodes[2]));
            g.addEdge(count, Integer.parseInt(nodes[0]), Integer.parseInt(nodes[1]));
            count++;
        }
        Features f = new Features();
        int edgeCount = g.getEdgeCount();
        f.setEdges(edgeCount);
        int nodeCount = g.getVertexCount();
        f.setNodes(nodeCount);
        f.setDensity();
        int maxDegree = -1;

        Transformer edge_weights = MapTransformer.getInstance(map); //Key Step!
        PageRank<Integer, Integer> pageRanks = new PageRank<Integer, Integer>(g, edge_weights, 0.85);
        pageRanks.evaluate();

        DijkstraShortestPath<Integer, Integer> dijkstraShortestPath
                = new DijkstraShortestPath<>(g, edge_weights);
        int[][] shortestPaths = new int[nodeCount][nodeCount];

        int[] eccentricities = new int[nodeCount];
        int radius = Integer.MAX_VALUE;
        int diameter = -1;

        int sum = 0;
        int sum2 = 0;
        int numPaths = 0;
        for (int r = 0; r < shortestPaths[0].length; r++) {
            int eccentricity = 0;
            for (int c = 0; c < shortestPaths.length; c++) {
                shortestPaths[r][c] = dijkstraShortestPath.getPath(r, c).size();
                eccentricity = Math.max(eccentricity, shortestPaths[r][c]);
                sum += shortestPaths[r][c];
                sum2 += shortestPaths[r][c] * shortestPaths[r][c];
                if (shortestPaths[r][c] != 0) {
                    numPaths++;
                }
            }
            eccentricities[r] = eccentricity;
            if (eccentricity > 1) {
                radius = Math.min(radius, eccentricity);
            }
            diameter = Math.max(diameter, eccentricity);
        }
        double meanShortestPath = sum / numPaths;
        double varShortestPath = sum2 / numPaths - meanShortestPath * meanShortestPath;
        f.setMeanShortestPathLength(meanShortestPath);
        f.setVarShortestPathLength(varShortestPath);

        Map<Integer, Double> clustering = Metrics.clusteringCoefficients(g);
        double[] meanVarClustering = getMeanVar(clustering);
        f.setMeanClusteringCoefficient(meanVarClustering[0]);
        f.setVarClusteringCoefficient(meanVarClustering[1]);

        BetweennessCentrality betweennessCentrality = new BetweennessCentrality(g);

        f.setRadius(radius);
        f.setDiameter(diameter);
        int centreSize = 0;
        for (int e : eccentricities) {
            if (e == radius) {
                centreSize++;
            }
        }
        f.setCentreSize(centreSize);
        double meanEccentricity = getMean(eccentricities);
        f.setMeanEccentricity(meanEccentricity);
        f.setVarEccentricity(getVariance(eccentricities, meanEccentricity));

        double pageRankSum = 0;
        double pageRankSum2 = 0;
        double nodeCentralitySum = 0;
        double nodeCentralitySum2 = 0;
        double edgeCentralitySum = 0;
        double edgeCentralitySum2 = 0;

        for (int i = 0; i < nodeCount; i++) {
            maxDegree = Math.max(maxDegree, g.inDegree(i) + g.outDegree(i));
            pageRankSum += pageRanks.getVertexScore(i);
            pageRankSum2 += pageRanks.getVertexScore(i) * pageRanks.getVertexScore(i);
            nodeCentralitySum += betweennessCentrality.getVertexScore(i);
            nodeCentralitySum2 += betweennessCentrality.getVertexScore(i) * betweennessCentrality.getVertexScore(i);
            edgeCentralitySum += betweennessCentrality.getEdgeScore(i);
            edgeCentralitySum2 += betweennessCentrality.getEdgeScore(i) * betweennessCentrality.getEdgeScore(i);
        }

        double meanPageRank = pageRankSum / nodeCount;
        f.setMeanPagerank(meanPageRank);
        f.setVarPagerank(pageRankSum2 / nodeCount - meanPageRank * meanPageRank);
        f.setMaxDegree(maxDegree);
        double meanNodeCentrality = nodeCentralitySum / nodeCount;
        double meanEdgeCentrality = edgeCentralitySum / nodeCount;
        f.setMeanNodeBetweennessCentrality(meanNodeCentrality);
        f.setMeanEdgeBetweenessCentrality(meanEdgeCentrality);
        f.setVarNodeBetweennessCentrality(nodeCentralitySum2 / nodeCount - meanNodeCentrality * meanNodeCentrality);
        f.setVarEdgeBetweenessCentrality(edgeCentralitySum2 / nodeCount - meanEdgeCentrality * meanEdgeCentrality);
        return f;
    }


    private static double[] getMeanVar(Map<Integer, Double> map) {
        double sum = 0;
        double sum2 = 0;
        for (Map.Entry<Integer, Double> entry: map.entrySet()) {
            sum+=entry.getValue();
            sum2+=entry.getValue()*entry.getValue();
        }
        double[] ret = new double[2];
        ret[0] = sum/map.size();
        ret[1] = sum2/map.size() - sum*sum;
        return ret;
    }
}
