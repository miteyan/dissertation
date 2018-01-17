package uk.ac.cam.cl.loclogger.graph;

import org.jgrapht.graph.WeightedMultigraph;

import java.util.ArrayList;

public class LocationGraph extends WeightedMultigraph<LocationNode, LocationEdge> {

    public LocationGraph(Class<? extends LocationEdge> edgeClass) {
        super(edgeClass);
    }

    public LocationGraph update(ArrayList<LocationNode> nodes, ArrayList<LocationEdge> edges) {
        // TODO: update graph with nodes and edges
        return this;
    }
}