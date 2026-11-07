def plan_execution(tasks, dependencies):
    if len(set(tasks)) != len(tasks):
        raise ValueError("Task names must be unique")

    next_tasks = {name: set() for name in tasks}
    waiting_for = {name: 0 for name in tasks}
    seen_pairs = set()

    for pair in dependencies:
        if len(pair) != 2:
            raise ValueError(f"Dependency must have two names: {pair}")
        before, after = pair
        for name in (before, after):
            if name not in waiting_for:
                raise ValueError(f"Unknown task name: {name}")
        if (before, after) in seen_pairs:
            continue
        seen_pairs.add((before, after))
        next_tasks[before].add(after)
        waiting_for[after] += 1

    ready = sorted(name for name in tasks if waiting_for[name] == 0)
    order = []

    while ready:
        current = ready.pop(0)
        order.append(current)
        for following in next_tasks[current]:
            waiting_for[following] -= 1
            if waiting_for[following] == 0:
                ready.append(following)
        ready.sort()

    if len(order) != len(tasks):
        stuck = sorted(set(tasks) - set(order))
        raise ValueError(f"Cycle detected, these tasks can never run: {stuck}")

    return order


def main():
    print(plan_execution(["build", "test", "deploy"],
                         [("build", "test"), ("test", "deploy")]))
    print(plan_execution(["c", "a", "b", "d"], [("a", "d"), ("b", "d")]))

    try:
        plan_execution(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    except ValueError as error:
        print("Error:", error)

    try:
        plan_execution(["a", "b"], [("a", "z")])
    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()