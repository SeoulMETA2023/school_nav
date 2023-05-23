def find_path(node_map, start, end):
    if start == end:
        return [Path([start, end], 0)]

    paths = _find_path(node_map, end, [start])

    def get_path_cost(path):
        return sum(map(lambda x: node_map.get_cost(path[x], path[x + 1]), range(len(path) - 1)))

    path_cost = list(map(lambda x: Path(x, get_path_cost(x)), paths))
    return sorted(path_cost, key=lambda x: x.cost)


def _find_path(node_map, target, path):
    next_nodes = list(set(node_map[path[-1]].linked) - set(path))
    if not next_nodes:
        return [[]]

    all_paths = []
    for node in next_nodes:
        new_path = path + [node]
        if node == target:
            all_paths.append(new_path)
            continue
        for next_path in _find_path(node_map, target, new_path):
            if not next_path:
                continue
            all_paths.append(next_path)

    return all_paths


class Path:
    def __init__(self, path, cost):
        self.path = path
        self.cost = cost
