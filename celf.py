def lazyForward(G, R, c, B, _type):
    V, E = G  # G is a graph with nodes V and edges E
    A = set()  # Initialize A as an empty set
    delta = {s: float('inf') for s in V}  # Set delta to +∞ for each node s in V

    # Main loop to check if there's an s in V \ A where c(A ∪ {s}) ≤ B
    while any(c(A | {s}) <= B for s in V - A):
        curs = {s: False for s in V - A}  # Initialize curs for each s ∈ V \ A

        while True:
            # Choose s* based on type
            if _type == "uc":
                # Select s* as the max deltas for nodes where cost c(A ∪ {s}) ≤ B
                s_star = max((s for s in V - A if c(A | {s}) <= B), key=lambda s: delta[s], default=None)
            elif _type == "cb":
                # Select s* as the max deltas / c(s) for nodes where cost c(A ∪ {s}) ≤ B
                s_star = max((s for s in V - A if c(A | {s}) <= B), key=lambda s: delta[s] / c(s), default=None)

            if s_star is None:
                break  # No valid s* found, exit loop

            if curs[s_star]:
                A.add(s_star)  # Add s* to A
                break
            else:
                delta[s_star] = R(A | {s_star}) - R(A)  # Update deltas
                curs[s_star] = True

    return A


def celf(G, R, c, B):
    # Run lazyForward twice for UC and CB types
    a_uc = lazyForward(G, R, c, B, "uc")
    a_cb = lazyForward(G, R, c, B, "cb")

    # Return the one with the maximum R value
    return max(a_uc, a_cb, key=lambda A: R(A))
