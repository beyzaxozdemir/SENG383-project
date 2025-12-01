from typing import List, Dict
from models import Course, Classroom, Schedule


class BeePlanScheduler:
    """
    Skeleton scheduler for BeePlan.

    Week 9 scope:
    - Provide a clean interface for generating and validating schedules.
    - Real algorithm and rule checks will be implemented in later weeks.
    """

    def __init__(self, courses: List[Course], classrooms: List[Classroom]) -> None:
        self.courses = courses
        self.classrooms = classrooms

    def generate_schedule(self) -> List[Schedule]:
        """
        Generate schedules per year.

        Week 9:
        - Only groups courses by year and returns empty schedules.
        - TODO: assign timeslots and classrooms respecting all constraints
          (Friday exam block, lab after theory, capacity, instructor overlaps, etc.)
        """
        schedules_by_year: Dict[int, Schedule] = {}

        for course in self.courses:
            if course.year not in schedules_by_year:
                schedules_by_year[course.year] = Schedule(year=course.year)

            # TODO: create a ScheduledCourse with a proper timeslot and classroom
            # and add it to schedules_by_year[course.year]

        return list(schedules_by_year.values())

    def validate(self, schedules: List[Schedule]) -> List[str]:
        """
        Validate the generated schedules.

        Week 9:
        - Only returns an empty list with TODO comments.
        - TODO rules (for later):
            * Friday exam block must be free.
            * Instructors must not have overlapping courses.
            * Daily theory hour limits for instructors.
            * Classroom capacity and lab/theory room type.
        """
        violations: List[str] = []

        # TODO: implement rule checks in V&V weeks
        return violations
