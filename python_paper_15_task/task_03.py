def values_match(value, target):
    if isinstance(value, bool) or isinstance(target, bool):
        return type(value) is type(target) and value == target
    return value == target


def find_paths(data, target):
    paths = []

    def search(value, path):
        if path != "" and values_match(value, target):
            paths.append(path)

        if isinstance(value, dict):
            for key, inner in value.items():
                new_path = str(key) if path == "" else path + "." + str(key)
                search(inner, new_path)
        elif isinstance(value, list):
            for index, inner in enumerate(value):
                search(inner, path + f"[{index}]")

    search(data, "")
    return paths


def main():
    data = {"a": [{"x": 5}, 5], "b": {"y": 5}}
    print(find_paths(data, 5))
    print(find_paths({"flag": True, "count": 1, "list": [1, True]}, 1))
    print(find_paths({"flag": True, "count": 1}, True))
    print(find_paths({}, 5))


if __name__ == "__main__":
    main()