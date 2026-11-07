from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Booking:
    booking_id: str
    room: str
    start: datetime
    end: datetime


class RoomScheduler:
    def __init__(self):
        self._rooms = {}
        self._ids = set()

    def add_booking(self, bid, room, start, end):
        if not isinstance(bid, str) or not bid.strip():
            raise ValueError("booking id cannot be empty")
        if not isinstance(room, str) or not room.strip():
            raise ValueError("room name cannot be empty")
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("start and end must be datetime")

        bid = bid.strip()
        room = room.strip()

        if end <= start:
            return {"accepted": False, "reason": "End must be after start", "conflicts": []}
        if bid in self._ids:
            return {"accepted": False, "reason": "Duplicate booking id", "conflicts": []}

        conflicts = [b for b in self._rooms.get(room, [])
                     if start < b.end and b.start < end]
        if conflicts:
            return {"accepted": False, "reason": "Time overlaps another booking",
                    "conflicts": conflicts}

        b = Booking(bid, room, start, end)
        self._rooms.setdefault(room, []).append(b)
        self._rooms[room].sort(key=lambda x: x.start)
        self._ids.add(bid)
        return {"accepted": True, "reason": "Booked", "conflicts": []}

    def get_schedule(self, room):
        return list(self._rooms.get(room.strip(), []))


def main():
    sched = RoomScheduler()

    def at(h, m=0):
        return datetime(2026, 11, 7, h, m)

    reqs = [
        ("B1", "Room A", at(9), at(10)),
        ("B2", "Room A", at(10), at(11)),
        ("B3", "Room A", at(9, 30), at(10, 30)),
        ("B4", "Room B", at(9, 30), at(10, 30)),
        ("B5", "Room A", at(12), at(11)),
        ("B1", "Room B", at(14), at(15)),
    ]
    for bid, room, start, end in reqs:
        res = sched.add_booking(bid, room, start, end)
        line = f"{bid} {room} {start:%H:%M}-{end:%H:%M}: {res['reason']}"
        if res["conflicts"]:
            line += " -> " + ", ".join(c.booking_id for c in res["conflicts"])
        print(line)

    print("Room A schedule:", [(b.booking_id, f"{b.start:%H:%M}-{b.end:%H:%M}")
                               for b in sched.get_schedule("Room A")])


if __name__ == "__main__":
    main()