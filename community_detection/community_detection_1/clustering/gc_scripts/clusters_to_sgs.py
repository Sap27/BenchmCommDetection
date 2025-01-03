"""
Convert a graph + cluster file to a number of separate subgraphs,
in edge list format

"""
import sys
import argparse
import igraph as ig
import io_functions as io

def names_to_ids(G, cluster):
    # map from vertex name to vertex ID in G
    return [v.index for v in G.vs if v["name"] in cluster]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("network_file", help="Original network input file")
    parser.add_argument("cluster_file", help="A cluster results file")
    parser.add_argument("-n", "--node_list", nargs="?", default=[],
                        help="Optionally specify a list of the nodes in\
                              the graph.")
    parser.add_argument("-o", "--output_prefix", nargs="?", default="",
                        help="Optionally specify a prefix for output files")
    opts = parser.parse_args()

    nodes = io.get_node_list(opts.node_list) if opts.node_list else []
    output_pref = opts.output_prefix if opts.output_prefix else './clusters_'
    G = io.build_ig_graph_from_matrix(opts.network_file, is_directed=False,
                                      node_list=nodes)
    if opts.node_list: G.vs['name'] = nodes
    clusters = io.read_clusters(opts.cluster_file)

    for idx, cluster in enumerate(clusters):
        try:
            output_file = '{}{}.txt'.format(output_pref, idx)
            output_fp = open(output_file, 'w')
        except IOError:
            sys.exit("Could not open file: {}".format(output_file))
        id_cluster = names_to_ids(G, cluster)
        SG = G.subgraph(id_cluster)
        for e in SG.es:
            output_fp.write('{}\t{}\t{}\n'.format(SG.vs[e.source]['name'],
                                                  SG.vs[e.target]['name'],
                                                  e['weight']))
        output_fp.close()


if __name__ == '__main__':
    main()


