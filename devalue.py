import json, sys

SPECIAL = {
    "undefined": None,
    "NaN": float("nan"),
    "Infinity": float("inf"),
    "-Infinity": float("-inf"),
    "-0": 0,
}

def unflatten(values):
    n = len(values)
    out = [None] * n

    # phase 1: pre-create containers
    for i, v in enumerate(values):
        if isinstance(v, list):
            out[i] = []
        elif isinstance(v, dict):
            out[i] = {}
        else:
            out[i] = SPECIAL.get(v, v)

    def ref(x):
        if isinstance(x, int) and 0 <= x < n:
            return out[x]
        return SPECIAL.get(x, x) if isinstance(x, str) else x

    # phase 2: fill
    for i, v in enumerate(values):
        if isinstance(v, list):
            for x in v:
                out[i].append(ref(x))
        elif isinstance(v, dict):
            for k, x in v.items():
                out[i][k] = ref(x)
    return out[0] if n else None

def main(path):
    data = json.load(open(path, encoding="utf-8"))
    out = []
    for ni, node in enumerate(data["nodes"]):
        if not isinstance(node, dict):
            continue
        if node.get("type") == "data":
            out.append((ni, unflatten(node["data"])))
        elif node.get("type") == "redirect":
            print("redirect node", ni, node)
    return out

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    out = main(sys.argv[1])
    for ni, obj in out:
        print("=" * 20, "node", ni)
        print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))
