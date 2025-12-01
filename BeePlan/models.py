from dataclasses import dataclass, field
from typing import List


@dataclass
class Instructor:
    """Represents an instructor in BeePlan."""
    name: str
    department: str


@dataclass
class Classroom:
    """Represents a classroom (lab or theory)."""
    name: str
    capacity: int
    room_type: str  # "lab" or "theory"


@dataclass
class Course:
    """Represents a course to be scheduled."""
    code: str
    name: str
    year: int
    theory_hours: int
    lab_hours: int
    instructor: Instructor
    is_elective: bool = False


@dataclass
class Timeslot:
    """Represents a day/time interval in the weekly timetable."""
    day: str         # "Mon", "Tue", ...
    start_time: str  # "09:20"
    end_time: str    # "10:10"


@dataclass
class ScheduledCourse:
    """
    A course that has been assigned to a classroom and a timeslot.
    """
    course: Course
    classroom: Classroom
    timeslot: Timeslot


@dataclass
class Schedule:
    """
    Schedule of a single year (1st, 2nd, 3rd, 4th) in BeePlan.
    """
    year: int
    scheduled_courses: List[ScheduledCourse] = field(default_factory=list)

    def add(self, scheduled_course: ScheduledCourse) -> None:
        self.scheduled_courses.append(scheduled_course)
