def longest_unique_window(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    last_seen = {}
    window_start = 0
    best_start = 0
    best_length = 0

    for index, char in enumerate(text):
        if char in last_seen and last_seen[char] >= window_start:
            window_start = last_seen[char] + 1
        last_seen[char] = index

        length = index - window_start + 1
        if length > best_length:
            best_length = length
            best_start = window_start

    return text[best_start:best_start + best_length], best_start, best_length


def main():
    for word in ["abcabcbb", "", "bbbbb", "pwwkew", "a b!a b"]:
        print(repr(word), "->", longest_unique_window(word))


if __name__ == "__main__":
    main()