import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
)


class BeePlanApp(QMainWindow):
    """
    BeePlan main window.

    Matches the Week 7 dashboard design:
    - Year selection
    - Load buttons (courses / instructors / classrooms)
    - Generate Schedule / View Report / Export / Reset
    - Loaded Files panel
    - System Summary panel
    - Timetable placeholder at the center
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BeePlan - Department Scheduler")
        self.resize(1100, 650)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # --- Top bar: Year selection + main actions ---
        top_layout = QHBoxLayout()

        year_label = QLabel("Select Year:")
        self.year_combo = QComboBox()
        self.year_combo.addItems(["All Years", "1st Year", "2nd Year", "3rd Year", "4th Year"])

        top_layout.addWidget(year_label)
        top_layout.addWidget(self.year_combo)
        top_layout.addStretch()

        self.btn_load_courses = QPushButton("Load Courses")
        self.btn_load_instructors = QPushButton("Load Instructors")
        self.btn_load_classrooms = QPushButton("Load Classrooms")
        self.btn_generate = QPushButton("Generate Schedule")
        self.btn_view_report = QPushButton("View Report")
        self.btn_export = QPushButton("Export Schedule")
        self.btn_reset = QPushButton("Reset")

        for btn in [
            self.btn_load_courses,
            self.btn_load_instructors,
            self.btn_load_classrooms,
            self.btn_generate,
            self.btn_view_report,
            self.btn_export,
            self.btn_reset,
        ]:
            top_layout.addWidget(btn)

        main_layout.addLayout(top_layout)

        # Connect buttons to stub methods (Week 9: no real logic)
        self.btn_load_courses.clicked.connect(self.on_load_courses)
        self.btn_load_instructors.clicked.connect(self.on_load_instructors)
        self.btn_load_classrooms.clicked.connect(self.on_load_classrooms)
        self.btn_generate.clicked.connect(self.on_generate_schedule)
        self.btn_view_report.clicked.connect(self.on_view_report)
        self.btn_export.clicked.connect(self.on_export_schedule)
        self.btn_reset.clicked.connect(self.on_reset)

        # --- Middle panels: Loaded Files + System Summary ---
        mid_layout = QHBoxLayout()

        loaded_files_group = QGroupBox("Loaded Files")
        loaded_files_layout = QGridLayout()
        self.lbl_courses_status = QLabel("Courses.json: Not loaded")
        self.lbl_instructors_status = QLabel("Instructors.json: Not loaded")
        self.lbl_classrooms_status = QLabel("Classrooms.json: Not loaded")

        loaded_files_layout.addWidget(self.lbl_courses_status, 0, 0)
        loaded_files_layout.addWidget(self.lbl_instructors_status, 1, 0)
        loaded_files_layout.addWidget(self.lbl_classrooms_status, 2, 0)
        loaded_files_group.setLayout(loaded_files_layout)

        summary_group = QGroupBox("System Summary")
        summary_layout = QGridLayout()
        self.lbl_conflict_free = QLabel("Conflict-free: N/A")
        self.lbl_warnings = QLabel("Warnings: N/A")
        self.lbl_scheduled_courses = QLabel("Scheduled Courses: N/A")
        self.lbl_instructors = QLabel("Instructors: N/A")
        self.lbl_classrooms = QLabel("Classrooms: N/A")

        summary_layout.addWidget(self.lbl_conflict_free, 0, 0)
        summary_layout.addWidget(self.lbl_warnings, 1, 0)
        summary_layout.addWidget(self.lbl_scheduled_courses, 2, 0)
        summary_layout.addWidget(self.lbl_instructors, 3, 0)
        summary_layout.addWidget(self.lbl_classrooms, 4, 0)
        summary_group.setLayout(summary_layout)

        mid_layout.addWidget(loaded_files_group)
        mid_layout.addWidget(summary_group)
        main_layout.addLayout(mid_layout)

        # --- Timetable placeholder (center) ---
        self.timetable = QTableWidget()
        self.timetable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        times = ["09:20", "10:20", "11:20", "12:20", "13:20", "14:20", "15:20", "16:20"]

        self.timetable.setColumnCount(len(days))
        self.timetable.setRowCount(len(times))
        self.timetable.setHorizontalHeaderLabels(days)
        self.timetable.setVerticalHeaderLabels(times)

        # Fill cells with empty items (later will show course codes)
        for row in range(len(times)):
            for col in range(len(days)):
                self.timetable.setItem(row, col, QTableWidgetItem(""))

        main_layout.addWidget(self.timetable)

    # ---------- Stub slot methods (no real logic yet) ----------

    def on_load_courses(self) -> None:
        # Week 9: only update label as a placeholder.
        self.lbl_courses_status.setText("Courses.json: Loaded (placeholder)")

    def on_load_instructors(self) -> None:
        self.lbl_instructors_status.setText("Instructors.json: Loaded (placeholder)")

    def on_load_classrooms(self) -> None:
        self.lbl_classrooms_status.setText("Classrooms.json: Loaded (placeholder)")

    def on_generate_schedule(self) -> None:
        # Week 9: no algorithm, just placeholder text.
        self.lbl_conflict_free.setText("Conflict-free: N/A (skeleton)")
        self.lbl_warnings.setText("Warnings: N/A (skeleton)")
        self.lbl_scheduled_courses.setText("Scheduled Courses: N/A (skeleton)")

    def on_view_report(self) -> None:
        # Placeholder: in later weeks this will open a ValidationReport dialog.
        # For now, just change a label so we can see the button works.
        self.lbl_warnings.setText("Warnings: see Validation Report (later)")

    def on_export_schedule(self) -> None:
        # Placeholder for export functionality.
        pass

    def on_reset(self) -> None:
        # Reset labels to default placeholder values.
        self.lbl_courses_status.setText("Courses.json: Not loaded")
        self.lbl_instructors_status.setText("Instructors.json: Not loaded")
        self.lbl_classrooms_status.setText("Classrooms.json: Not loaded")
        self.lbl_conflict_free.setText("Conflict-free: N/A")
        self.lbl_warnings.setText("Warnings: N/A")
        self.lbl_scheduled_courses.setText("Scheduled Courses: N/A")
        self.lbl_instructors.setText("Instructors: N/A")
        self.lbl_classrooms.setText("Classrooms: N/A")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeePlanApp()
    window.show()
    sys.exit(app.exec_())
