import os
from datetime import datetime

SAMPLE_DIR = "sample_data"


def parse_log_line(line):
    parts = line.split("|", 2)
    if len(parts) != 3:
        return None

    timestamp, level, message = [part.strip() for part in parts]
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    if not level or not message:
        return None

    return timestamp, level.upper(), message


def read_errors(path, stats=None):
    if stats is None:
        stats = {}
    stats["malformed"] = 0

    with open(path, "r", encoding="utf-8", errors="replace") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            if not line.strip():
                continue
            parsed = parse_log_line(line)
            if parsed is None:
                stats["malformed"] += 1
                continue

            timestamp, level, message = parsed
            if level == "ERROR":
                yield line_number, timestamp, message


def summarize_errors(path):
    stats = {}
    errors_by_date = {}

    for line_number, timestamp, message in read_errors(path, stats):
        date = timestamp[:10]
        errors_by_date[date] = errors_by_date.get(date, 0) + 1

    return dict(sorted(errors_by_date.items())), stats.get("malformed", 0)


def create_sample_log(path):
    lines = [
        "2026-11-07 10:30:00 | ERROR | Connection lost",
        "2026-11-07 10:31:12 | INFO | Reconnected",
        "2026-11-07 11:05:44 | ERROR | Disk almost full",
        "this line is broken",
        "2026-11-08 09:00:00 | ERROR | Timeout while saving",
        "2026-13-45 99:99:99 | ERROR | Bad date",
        "2026-11-08 12:00:00 | WARNING | Slow response",
        "",
        "2026-11-08 18:20:10 | ERROR | Payment failed",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    log_path = os.path.join(SAMPLE_DIR, "app.log")
    create_sample_log(log_path)

    for record in read_errors(log_path):
        print(record)

    counts, bad_lines = summarize_errors(log_path)
    print("Errors by date:", counts)
    print("Malformed lines skipped:", bad_lines)


if __name__ == "__main__":
    main()