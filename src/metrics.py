"""Custom simplicity metrics for Petri net evaluation."""

import numpy as np


def simplicity_cnc(net) -> float:
    """
    Coefficient of Network Connectivity, normalised to [0, 1].

    CNC = |arcs| / (|places| + |transitions|), see Carmona et al. (2018).
    A linear net has CNC close to 1, a densely connected net has CNC much
    larger. We return 1 / (1 + CNC) so that higher = simpler.
    """
    n_nodes = len(net.places) + len(net.transitions)
    if n_nodes == 0:
        return 1.0
    cnc = len(net.arcs) / n_nodes
    return 1.0 / (1.0 + cnc)


def simplicity_weighted_place_degree(net) -> float:
    """
    Average in+out degree of places, mapped to [0, 1] as 1 / (1 + mean).

    Places with many incoming and outgoing arcs concentrate routing
    decisions and are the main source of visual clutter in a Petri net.
    Higher score = simpler.
    """
    if len(net.places) == 0:
        return 1.0

    degrees = [len(p.in_arcs) + len(p.out_arcs) for p in net.places]
    return 1.0 / (1.0 + float(np.mean(degrees)))
