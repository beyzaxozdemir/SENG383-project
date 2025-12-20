from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMES = ["09:20", "10:20", "11:20", "12:20", "13:20", "14:20", "15:20", "16:20"]

# Friday exam block 13:20–15:10 -> block 13:20 and 14:20 slots
BLOCKED = {(4, 4), (4, 5)}  # (day_idx, time_idx)


@dataclass(frozen=True)
class Course:
    code: str
    instructor_id: str
    students: int
    is_lab: bool = False


@dataclass(frozen=True)
class Classroom:
    id: str
    name: str
    capacity: int


@dataclass(frozen=True)
class Instructor:
    id: str
    name: str


@dataclass(frozen=True)
class Placement:
    course_code: str
    instructor_id: str
    room_id: str


def pick_room(course: Course, rooms: List[Classroom]) -> Optional[Classroom]:
    """Pick the smallest room that fits (simple heuristic)."""
    candidates = [r for r in rooms if r.capacity >= course.students]
    candidates.sort(key=lambda r: r.capacity)
    return candidates[0] if candidates else None


def generate_schedule(
    courses: List[Course],
    rooms: List[Classroom],
) -> Tuple[Dict[Tuple[int, int], Placement], List[str], int, int]:
    """
    Greedy deterministic scheduler.
    Returns:
      schedule: (day_idx, time_idx) -> Placement
      report_lines: list of warnings/conflicts
      conflicts_count
      warnings_count
    """
    schedule: Dict[Tuple[int, int], Placement] = {}
    report: List[str] = []
    conflicts = 0
    warnings = 0

    courses_sorted = sorted(courses, key=lambda c: c.code)

    for course in courses_sorted:
        room = pick_room(course, rooms)
        if room is None:
            warnings += 1
            report.append(f"WARNING: Capacity - No room fits {course.code} ({course.students} students).")
            continue

        placed = False

        for time_idx in range(len(TIMES)):
            for day_idx in range(len(DAYS)):
                if (day_idx, time_idx) in BLOCKED:
                    continue

                key = (day_idx, time_idx)

                if key not in schedule:
                    schedule[key] = Placement(course.code, course.instructor_id, room.id)
                    placed = True
                    break
                else:
                    existing = schedule[key]
                    if existing.instructor_id == course.instructor_id:
                        conflicts += 1
                        report.append(
                            f"CONFLICT: Instructor overlap at {DAYS[day_idx]} {TIMES[time_idx]} "
                            f"({existing.course_code} vs {course.code}) instructor={course.instructor_id}"
                        )
                    if existing.room_id == room.id:
                        conflicts += 1
                        report.append(
                            f"CONFLICT: Room overlap at {DAYS[day_idx]} {TIMES[time_idx]} "
                            f"room={room.id} ({existing.course_code} vs {course.code})"
                        )

            if placed:
                break

        if not placed:
            warnings += 1
            report.append(f"WARNING: Unscheduled - Could not place {course.code} (no available slot).")

    if not report:
        report = ["No conflicts or warnings found."]

    return schedule, report, conflicts, warnings
