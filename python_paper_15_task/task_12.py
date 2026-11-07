class ReversibleRange:
    def __init__(self, start, stop, step=1):
        for v in (start, stop, step):
            if isinstance(v, bool) or not isinstance(v, int):
                raise TypeError("start, stop, step must be integers")
        if step == 0:
            raise ValueError("step cannot be zero")

        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self):
        if self.step > 0:
            n = (self.stop - self.start + self.step - 1) // self.step
        else:
            n = (self.start - self.stop - self.step - 1) // (-self.step)
        return max(0, n)

    def __iter__(self):
        cur = self.start
        if self.step > 0:
            while cur < self.stop:
                yield cur
                cur += self.step
        else:
            while cur > self.stop:
                yield cur
                cur += self.step

    def __reversed__(self):
        n = len(self)
        cur = self.start + (n - 1) * self.step
        while n > 0:
            yield cur
            cur -= self.step
            n -= 1

    def __contains__(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            return False
        if self.step > 0:
            ok = self.start <= value < self.stop
        else:
            ok = self.stop < value <= self.start
        return ok and (value - self.start) % self.step == 0

    def __repr__(self):
        return f"ReversibleRange({self.start}, {self.stop}, {self.step})"


def main():
    r = ReversibleRange(2, 11, 3)
    print(r, "->", list(r), "| reversed:", list(reversed(r)))
    print("len:", len(r), "| 5 in r:", 5 in r, "| 6 in r:", 6 in r)

    down = ReversibleRange(10, 0, -3)
    print(down, "->", list(down), "| reversed:", list(reversed(down)))
    print("len:", len(down), "| 4 in down:", 4 in down, "| 0 in down:", 0 in down)

    empty = ReversibleRange(5, 5)
    print(empty, "->", list(empty), "| len:", len(empty))

    for args in [(0, 10, 1), (0, 10, 3), (10, 0, -1), (10, 0, -4), (3, 1, 1), (1, 3, -1)]:
        mine = ReversibleRange(*args)
        real = range(*args)
        assert list(mine) == list(real)
        assert list(reversed(mine)) == list(reversed(real))
        assert len(mine) == len(real)
    print("Matches python range on all test cases")

    try:
        ReversibleRange(1, 5, 0)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()