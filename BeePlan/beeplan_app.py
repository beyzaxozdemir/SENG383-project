# beeplan_final.py
# BeePlan - Week 9 (Student B) FINAL (Tkinter)
# Dashboard + Scheduler + Report (single-file, no external GUI libs)

import os
import json
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Optional: XLSX (if you want to load common schedule)
try:
    import openpyxl  # type: ignore
except Exception:
    openpyxl = None


# -----------------------------
# Constants (Timetable)
# -----------------------------
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
TIMES = ["9:20", "10:20", "11:20", "12:20", "13:20", "14:20", "15:20", "16:20"]

# Exam block sample (you can adjust later)
EXAM_BLOCK = {("FRI", "13:20"): "EXAM\nBLOCK\n(13:20-15:10)"}


# -----------------------------
# Data models
# -----------------------------
@dataclass
class Course:
    code: str
    name: str = ""
    year: int = 1
    students: int = 0
    hours: int = 1
    instructor: str = ""  # name/id string


@dataclass
class Instructor:
    name: str
    available: Optional[List[Tuple[str, str]]] = None  # list of (day,time)


@dataclass
class Classroom:
    name: str
    capacity: int = 0


# -----------------------------
# Helpers: flexible key getter
# -----------------------------
def pick(d: dict, *keys: str, default=None):
    """Pick first matching key in dict (case-insensitive + common variants)."""
    if not isinstance(d, dict):
        return default
    lower_map = {str(k).lower(): k for k in d.keys()}
    for k in keys:
        k2 = str(k).lower()
        if k2 in lower_map:
            return d[lower_map[k2]]
    return default


def to_int(x, default=0):
    try:
        return int(float(str(x).strip()))
    except Exception:
        return default


# -----------------------------
# Loaders (JSON/CSV)
# -----------------------------
def load_json_or_csv(path: str) -> List[dict]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # accept either list or {"items":[...]}
        if isinstance(data, dict):
            if "items" in data and isinstance(data["items"], list):
                return data["items"]
            # try common keys
            for k in ["courses", "instructors", "classrooms", "data"]:
                if k in data and isinstance(data[k], list):
                    return data[k]
            # single object -> list
            return [data]
        if isinstance(data, list):
            return data
        return []
    elif ext == ".csv":
        out: List[dict] = []
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                out.append(row)
        return out
    else:
        raise ValueError("Only JSON or CSV supported.")


def parse_courses(rows: List[dict]) -> List[Course]:
    courses: List[Course] = []
    for r in rows:
        code = str(pick(r, "code", "courseCode", "course_code", "CourseCode", default="")).strip()
        if not code:
            # try 'name' as code fallback
            code = str(pick(r, "name", "course", default="")).strip()
        if not code:
            continue
        name = str(pick(r, "title", "courseName", "course_name", "name", default="")).strip()
        year = to_int(pick(r, "year", "classYear", "grade", default=1), 1)
        students = to_int(pick(r, "students", "studentCount", "capacityNeeded", "enrolled", default=0), 0)
        hours = to_int(pick(r, "hours", "duration", "weeklyHours", default=1), 1)
        instructor = str(pick(r, "instructor", "instructorName", "teacher", "lecturer", default="")).strip()
        courses.append(Course(code=code, name=name, year=year, students=students, hours=max(1, hours), instructor=instructor))
    return courses


def parse_instructors(rows: List[dict]) -> List[Instructor]:
    instructors: List[Instructor] = []
    for r in rows:
        name = str(pick(r, "name", "instructor", "instructorName", "teacher", "lecturer", default="")).strip()
        if not name:
            continue
        # optional availability
        avail = pick(r, "available", "availability", "slots", default=None)
        parsed_avail = None
        if isinstance(avail, list):
            tmp = []
            for item in avail:
                if isinstance(item, dict):
                    d = str(pick(item, "day", default="")).upper()
                    t = str(pick(item, "time", default=""))
                    if d and t:
                        tmp.append((d, t))
                elif isinstance(item, str) and "-" in item:
                    # "MON-9:20"
                    parts = item.split("-", 1)
                    tmp.append((parts[0].strip().upper(), parts[1].strip()))
            parsed_avail = tmp if tmp else None

        instructors.append(Instructor(name=name, available=parsed_avail))
    return instructors


def parse_classrooms(rows: List[dict]) -> List[Classroom]:
    rooms: List[Classroom] = []
    for r in rows:
        name = str(pick(r, "name", "room", "classroom", "id", "roomId", "roomName", default="")).strip()
        if not name:
            continue
        cap = to_int(pick(r, "capacity", "kontenjan", "roomCapacity", "cap", "quota", "size", default=0), 0)
        rooms.append(Classroom(name=name, capacity=cap))
    return rooms


# -----------------------------
# Scheduling (Week 9: simple heuristic)
# - We aim to place courses in free slots
# - Conflicts are counted if slot already used
# -----------------------------
def generate_schedule(courses: List[Course], year_filter: Optional[int] = None) -> Dict:
    # Prepare schedule dict
    schedule: Dict[str, Dict[str, str]] = {d: {t: "" for t in TIMES} for d in DAYS}

    # put exam blocks
    for (d, t), txt in EXAM_BLOCK.items():
        if d in schedule and t in schedule[d]:
            schedule[d][t] = txt

    # Filter courses
    pool = courses
    if year_filter:
        pool = [c for c in courses if c.year == year_filter]

    # Place courses
    conflicts = 0
    placed = 0

    # deterministic order
    pool_sorted = sorted(pool, key=lambda c: (c.year, c.code))

    for c in pool_sorted:
        placed_this = False
        for day in DAYS:
            for time in TIMES:
                # skip exam block
                if schedule[day][time].startswith("EXAM"):
                    continue
                if schedule[day][time] == "":
                    # place
                    label = c.code
                    # show (Lab) if code ends with L or contains LAB
                    if c.code.endswith("L") or "LAB" in c.code.upper():
                        label = f"{c.code}\n(Lab)"
                    schedule[day][time] = label
                    placed += 1
                    placed_this = True
                    break
                else:
                    # already occupied
                    continue
            if placed_this:
                break
        if not placed_this:
            conflicts += 1

    # Create a simple report (Week 9 style)
    rules_total = 6
    rules_passed = max(0, rules_total - conflicts)
    warnings = 1 if placed > 0 else 0
    critical = 1 if conflicts > 0 else 0

    return {
        "schedule": schedule,
        "scheduled_courses": placed,
        "conflicts": conflicts,
        "warnings": warnings,
        "critical": critical,
        "rules_passed": rules_passed,
        "rules_total": rules_total,
    }


# -----------------------------
# UI (Dashboard + Scheduler + Report)
# -----------------------------
class BeePlanFinalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BeePlan - Dashboard (Week 9 Student B Final)")
        self.root.geometry("1200x720")
        self.root.configure(bg="#cfe9ff")

        # loaded data
        self.courses: List[Course] = []
        self.instructors: List[Instructor] = []
        self.classrooms: List[Classroom] = []
        self.common_xlsx_loaded = False

        self.last_result: Optional[Dict] = None
        self.selected_year: Optional[int] = 1  # default 1st year

        self._build_styles()
        self._build_dashboard()

    # -------- Styles ----------
    def _build_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background="#cfe9ff")
        style.configure("Card.TFrame", background="white")
        style.configure("Title.TLabel", font=("Segoe UI", 26, "bold"), foreground="#1665c1", background="#cfe9ff")
        style.configure("Section.TLabel", font=("Segoe UI", 12, "bold"), background="white")
        style.configure("Info.TLabel", font=("Segoe UI", 11), background="white")
        style.configure("Small.TLabel", font=("Segoe UI", 10), background="white")

        style.configure("Year.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8))
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), padding=(16, 14))

    # -------- Dashboard UI ----------
    def _build_dashboard(self):
        # Top title
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=15, pady=(10, 5))

        ttk.Label(header, text="BEEPLAN - DASHBOARD", style="Title.TLabel").pack()

        # Year selector row (1st/2nd/3rd/4th)
        year_row = ttk.Frame(self.root)
        year_row.pack(fill="x", padx=15, pady=(6, 10))

        ttk.Label(year_row, text="Select Year:", font=("Segoe UI", 12, "bold"), background="#cfe9ff").pack(side="left", padx=(0, 10))

        self.year_btns = {}
        for y in [1, 2, 3, 4]:
            b = ttk.Button(year_row, text=f"{y}st Year" if y == 1 else f"{y}nd Year" if y == 2 else f"{y}rd Year" if y == 3 else f"{y}th Year",
                           style="Year.TButton", command=lambda yy=y: self.set_year(yy))
            b.pack(side="left", padx=6)
            self.year_btns[y] = b

        self.set_year(1)

        # Main content row
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=18, pady=10)

        # Left actions card
        left = ttk.Frame(main, style="Card.TFrame")
        left.pack(side="left", fill="y", padx=(0, 18), pady=5)
        left.configure(width=320)

        ttk.Label(left, text="QUICK ACTIONS", style="Section.TLabel").pack(pady=(15, 12))

        self.btn_load_courses = tk.Button(left, text="📄  Load Courses", font=("Segoe UI", 12, "bold"),
                                          bg="#6f35d9", fg="white", relief="flat", height=2,
                                          command=self.on_load_courses)
        self.btn_load_courses.pack(fill="x", padx=25, pady=10)

        self.btn_load_instructors = tk.Button(left, text="👩‍🏫  Load Instructors", font=("Segoe UI", 12, "bold"),
                                              bg="#1f63d7", fg="white", relief="flat", height=2,
                                              command=self.on_load_instructors)
        self.btn_load_instructors.pack(fill="x", padx=25, pady=10)

        self.btn_load_classrooms = tk.Button(left, text="🏫  Load Classrooms", font=("Segoe UI", 12, "bold"),
                                             bg="#f39c12", fg="white", relief="flat", height=2,
                                             command=self.on_load_classrooms)
        self.btn_load_classrooms.pack(fill="x", padx=25, pady=10)

        self.btn_generate = tk.Button(left, text="⚡  Generate Schedule", font=("Segoe UI", 12, "bold"),
                                      bg="#16b879", fg="white", relief="flat", height=2,
                                      command=self.on_generate_schedule)
        self.btn_generate.pack(fill="x", padx=25, pady=10)

        self.btn_view_report = tk.Button(left, text="🧾  View Report", font=("Segoe UI", 12, "bold"),
                                         bg="#1449c8", fg="white", relief="flat", height=2,
                                         command=self.on_view_report)
        self.btn_view_report.pack(fill="x", padx=25, pady=10)

        self.btn_export = tk.Button(left, text="📤  Export Schedule", font=("Segoe UI", 12, "bold"),
                                    bg="#7ec90d", fg="white", relief="flat", height=2,
                                    command=self.on_export_schedule)
        self.btn_export.pack(fill="x", padx=25, pady=10)

        self.btn_reset = tk.Button(left, text="🔁  Reset", font=("Segoe UI", 12, "bold"),
                                   bg="#f24444", fg="white", relief="flat", height=2,
                                   command=self.on_reset)
        self.btn_reset.pack(fill="x", padx=25, pady=(10, 18))

        # Right cards
        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        # Loaded files card
        self.card_files = ttk.Frame(right, style="Card.TFrame")
        self.card_files.pack(fill="x", pady=5, ipadx=10, ipady=10)

        ttk.Label(self.card_files, text="📁  LOADED FILES:", style="Section.TLabel").pack(anchor="w", padx=15, pady=(10, 8))

        self.lbl_file_instructors = tk.Label(self.card_files, text="☐ Instructors.json", font=("Segoe UI", 12, "bold"),
                                             bg="white", fg="#2b2b2b")
        self.lbl_file_instructors.pack(anchor="w", padx=35, pady=3)

        self.lbl_file_courses = tk.Label(self.card_files, text="☐ Courses.json", font=("Segoe UI", 12, "bold"),
                                         bg="white", fg="#2b2b2b")
        self.lbl_file_courses.pack(anchor="w", padx=35, pady=3)

        self.lbl_file_classrooms = tk.Label(self.card_files, text="☐ Classrooms.json", font=("Segoe UI", 12, "bold"),
                                            bg="white", fg="#2b2b2b")
        self.lbl_file_classrooms.pack(anchor="w", padx=35, pady=3)

        self.lbl_file_common = tk.Label(self.card_files, text="☐ CommonSchedule.xlsx", font=("Segoe UI", 12, "bold"),
                                        bg="white", fg="#2b2b2b")
        self.lbl_file_common.pack(anchor="w", padx=35, pady=(3, 10))

        # Last schedule card
        self.card_last = ttk.Frame(right, style="Card.TFrame")
        self.card_last.pack(fill="x", pady=12, ipadx=10, ipady=10)

        ttk.Label(self.card_last, text="⏱  LAST SCHEDULE:", style="Section.TLabel").pack(anchor="w", padx=15, pady=(10, 8))
        self.lbl_last_year = ttk.Label(self.card_last, text="Year: -", style="Info.TLabel")
        self.lbl_last_year.pack(anchor="w", padx=35, pady=2)

        self.lbl_last_status = ttk.Label(self.card_last, text="Status: -", style="Info.TLabel")
        self.lbl_last_status.pack(anchor="w", padx=35, pady=2)

        self.lbl_last_time = ttk.Label(self.card_last, text="Time: -", style="Info.TLabel")
        self.lbl_last_time.pack(anchor="w", padx=35, pady=(2, 10))

    def set_year(self, year: int):
        self.selected_year = year
        # simple highlight
        for y, b in self.year_btns.items():
            if y == year:
                b.configure(state="disabled")
            else:
                b.configure(state="normal")

    # -------- File label updates ----------
    def _set_loaded_label(self, lbl: tk.Label, loaded: bool, filename: str):
        if loaded:
            lbl.config(text=f"✅ {filename}", fg="#1aa84a")
        else:
            lbl.config(text=f"❌ {filename}", fg="#d02727")

    # -------- Actions ----------
    def on_load_courses(self):
        path = filedialog.askopenfilename(title="Select Courses JSON/CSV", filetypes=[("JSON", "*.json"), ("CSV", "*.csv")])
        if not path:
            return
        try:
            rows = load_json_or_csv(path)
            self.courses = parse_courses(rows)
            if not self.courses:
                raise ValueError("No valid course rows found.")
            self._set_loaded_label(self.lbl_file_courses, True, os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Load Courses", str(e))

    def on_load_instructors(self):
        path = filedialog.askopenfilename(title="Select Instructors JSON/CSV", filetypes=[("JSON", "*.json"), ("CSV", "*.csv")])
        if not path:
            return
        try:
            rows = load_json_or_csv(path)
            self.instructors = parse_instructors(rows)
            if not self.instructors:
                raise ValueError("No valid instructor rows found.")
            self._set_loaded_label(self.lbl_file_instructors, True, os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Load Instructors", str(e))

    def on_load_classrooms(self):
        path = filedialog.askopenfilename(title="Select Classrooms JSON/CSV", filetypes=[("JSON", "*.json"), ("CSV", "*.csv")])
        if not path:
            return
        try:
            rows = load_json_or_csv(path)
            self.classrooms = parse_classrooms(rows)
            if not self.classrooms:
                raise ValueError("No valid classroom rows found.")
            self._set_loaded_label(self.lbl_file_classrooms, True, os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Load Classrooms", str(e))

    def on_generate_schedule(self):
        if not self.courses:
            messagebox.showwarning("Missing Data", "Please load Courses first.")
            return

        year = self.selected_year
        result = generate_schedule(self.courses, year_filter=year)

        self.last_result = result
        # update last schedule card
        ytxt = f"{year}st Year" if year == 1 else f"{year}nd Year" if year == 2 else f"{year}rd Year" if year == 3 else f"{year}th Year"
        self.lbl_last_year.config(text=f"Year: {ytxt}")
        status = "Successful" if result["conflicts"] == 0 else "With Issues"
        self.lbl_last_status.config(text=f"Status: {status}")
        self.lbl_last_time.config(text="Time: (now)")

        messagebox.showinfo(
            "Generated",
            "Schedule generated.\n"
            f"Critical: {result['critical']}\n"
            f"Warnings: {result['warnings']}\n"
            f"Rules: {result['rules_passed']}/{result['rules_total']}"
        )

        # ✅ THIS IS THE IMPORTANT PART: OPEN SCHEDULE WINDOW
        self.open_schedule_window(result["schedule"])

    def on_view_report(self):
        if not self.last_result:
            messagebox.showwarning("No Report", "Please generate schedule first.")
            return
        self.open_report_window(self.last_result)

    def on_export_schedule(self):
        if not self.last_result:
            messagebox.showwarning("No Schedule", "Generate schedule first.")
            return
        save_path = filedialog.asksaveasfilename(title="Export Schedule", defaultextension=".txt",
                                                 filetypes=[("Text", "*.txt")])
        if not save_path:
            return
        try:
            sched = self.last_result["schedule"]
            with open(save_path, "w", encoding="utf-8") as f:
                f.write("BeePlan Export\n\n")
                for t in TIMES:
                    f.write(f"{t}: ")
                    row = []
                    for d in DAYS:
                        row.append(f"{d}={sched[d][t] or '-'}")
                    f.write(" | ".join(row) + "\n")
            messagebox.showinfo("Export", f"Exported to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Export", str(e))

    def on_reset(self):
        self.courses = []
        self.instructors = []
        self.classrooms = []
        self.last_result = None
        self.common_xlsx_loaded = False

        self._set_loaded_label(self.lbl_file_instructors, False, "Instructors.json")
        self._set_loaded_label(self.lbl_file_courses, False, "Courses.json")
        self._set_loaded_label(self.lbl_file_classrooms, False, "Classrooms.json")
        self._set_loaded_label(self.lbl_file_common, False, "CommonSchedule.xlsx")

        self.lbl_last_year.config(text="Year: -")
        self.lbl_last_status.config(text="Status: -")
        self.lbl_last_time.config(text="Time: -")

    # -------- Scheduler Window ----------
    def open_schedule_window(self, schedule: Dict[str, Dict[str, str]]):
        win = tk.Toplevel(self.root)
        win.title("BeePlan - Department Scheduler")
        win.geometry("1180x720")
        win.configure(bg="#cfe9ff")

        # Left sidebar (matches your UI feeling)
        sidebar = tk.Frame(win, bg="#cfe9ff", width=240)
        sidebar.pack(side="left", fill="y", padx=(15, 8), pady=15)

        def side_btn(text, cmd):
            b = tk.Button(sidebar, text=text, font=("Segoe UI", 10, "bold"),
                          bg="white", fg="#0b4aa2", relief="flat",
                          activebackground="#e6f2ff", padx=10, pady=10,
                          command=cmd)
            b.pack(fill="x", pady=8)
            return b

        side_btn("📥  Import JSON/CSV", lambda: messagebox.showinfo("Import", "Use Dashboard loaders (Week 9)."))
        side_btn("📤  Export Schedule", self.on_export_schedule)
        side_btn("⚙️  Settings", lambda: messagebox.showinfo("Settings", "Week 9: Settings placeholder."))
        side_btn("📊  Reports", self.on_view_report)
        side_btn("👩‍🏫  Instructor Manager", lambda: messagebox.showinfo("Instructor Manager", "Week 9 placeholder."))
        side_btn("🏫  Classroom Manager", lambda: messagebox.showinfo("Classroom Manager", "Week 9 placeholder."))

        # Status card (bottom-left)
        status_card = tk.Frame(sidebar, bg="white")
        status_card.pack(side="bottom", fill="x", pady=10)

        tk.Label(status_card, text="STATUS", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=12, pady=(10, 8))
        conflicts = self.last_result["conflicts"] if self.last_result else 0
        warnings = self.last_result["warnings"] if self.last_result else 0
        rules_txt = f"{self.last_result['rules_passed']}/{self.last_result['rules_total']} Rules" if self.last_result else "N/A"

        tk.Label(status_card, text=f"{conflicts} Conflict", font=("Segoe UI", 11, "bold"), fg="#d10000", bg="white").pack(anchor="w", padx=12, pady=2)
        tk.Label(status_card, text=f"{warnings} Warnings", font=("Segoe UI", 11, "bold"), fg="#f39c12", bg="white").pack(anchor="w", padx=12, pady=2)
        tk.Label(status_card, text=rules_txt, font=("Segoe UI", 11, "bold"), fg="#1aa84a", bg="white").pack(anchor="w", padx=12, pady=(2, 12))

        # Right main area
        main = tk.Frame(win, bg="#cfe9ff")
        main.pack(side="left", fill="both", expand=True, padx=(8, 15), pady=15)

        top = tk.Frame(main, bg="#cfe9ff")
        top.pack(fill="x")

        tk.Label(top, text="Currently Viewing:", font=("Segoe UI", 11, "bold"), bg="#cfe9ff").pack(side="left", padx=(0, 8))

        year_lbl = f"{self.selected_year}st Year" if self.selected_year == 1 else f"{self.selected_year}nd Year" if self.selected_year == 2 else f"{self.selected_year}rd Year" if self.selected_year == 3 else f"{self.selected_year}th Year"
        tk.Label(top, text=year_lbl, font=("Segoe UI", 10, "bold"), bg="white", fg="#0b4aa2", padx=10, pady=4).pack(side="left")

        tk.Label(top, text="  Week:", font=("Segoe UI", 11, "bold"), bg="#cfe9ff").pack(side="left", padx=(15, 6))
        week_combo = ttk.Combobox(top, values=["1. Week"], width=10, state="readonly")
        week_combo.set("1. Week")
        week_combo.pack(side="left")

        tk.Button(top, text="Generate Schedule", bg="#16b879", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=14, pady=8, command=self.on_generate_schedule).pack(side="right", padx=8)

        tk.Button(top, text="View Report", bg="#1449c8", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=14, pady=8, command=self.on_view_report).pack(side="right", padx=8)

        # Filters row (visual only for Week 9)
        filters = tk.Frame(main, bg="#cfe9ff")
        filters.pack(fill="x", pady=(10, 10))

        tk.Label(filters, text="FILTERS:", font=("Segoe UI", 10, "bold"), bg="#cfe9ff").pack(side="left", padx=(0, 10))
        for txt in ["Year", "Instructor", "Course", "Classroom"]:
            tk.Label(filters, text=f"{txt}: All", font=("Segoe UI", 9, "bold"),
                     bg="white", fg="#0b4aa2", padx=8, pady=3).pack(side="left", padx=6)

        # Timetable grid (blue borders like your UI)
        grid_wrap = tk.Frame(main, bg="#cfe9ff")
        grid_wrap.pack(fill="both", expand=True, pady=(5, 0))

        grid = tk.Frame(grid_wrap, bg="#cfe9ff")
        grid.pack()

        border_color = "#0a49b5"
        cell_bg = "#eaf6ff"

        # header row
        tk.Label(grid, text="", bg="#cfe9ff", width=9).grid(row=0, column=0, padx=2, pady=2)
        for c, day in enumerate(DAYS, start=1):
            tk.Label(grid, text=day, bg=cell_bg, fg="#111",
                     font=("Segoe UI", 10, "bold"),
                     width=14, height=2,
                     highlightbackground=border_color, highlightthickness=2).grid(row=0, column=c, padx=2, pady=2)

        # time rows + cells
        def cell_color(text: str) -> str:
            if text.startswith("EXAM"):
                return "#ffb5b5"
            if "CENG" in text:
                return "#2f86d6"
            if "MATH" in text:
                return "#7a58d6"
            if "SENG" in text:
                return "#f08a1a"
            return cell_bg

        def on_cell_click(day: str, time: str, text: str):
            if not text:
                return
            self.open_detail_card(day, time, text)

        for r, time in enumerate(TIMES, start=1):
            tk.Label(grid, text=time, bg=cell_bg, fg="#111",
                     font=("Segoe UI", 10, "bold"),
                     width=9, height=2,
                     highlightbackground=border_color, highlightthickness=2).grid(row=r, column=0, padx=2, pady=2)

            for c, day in enumerate(DAYS, start=1):
                text = schedule[day][time]
                bg = cell_color(text)
                fg = "white" if bg in ["#2f86d6", "#7a58d6", "#f08a1a"] else "#111"
                if text.startswith("EXAM"):
                    fg = "#d10000"

                lbl = tk.Label(grid, text=text, bg=bg, fg=fg,
                               font=("Segoe UI", 9, "bold"),
                               width=14, height=3,
                               justify="center",
                               highlightbackground=border_color, highlightthickness=2)
                lbl.grid(row=r, column=c, padx=2, pady=2)
                lbl.bind("<Button-1>", lambda e, dd=day, tt=time, tx=text: on_cell_click(dd, tt, tx))

    # -------- Detail Card ----------
    def open_detail_card(self, day: str, time: str, text: str):
        card = tk.Toplevel(self.root)
        card.title("Course Detail")
        card.geometry("420x260")
        card.configure(bg="#cfe9ff")

        box = tk.Frame(card, bg="white")
        box.pack(fill="both", expand=True, padx=18, pady=18)

        title = text.replace("\n", " ")
        tk.Label(box, text=title, font=("Segoe UI", 13, "bold"), bg="white", fg="#0b4aa2").pack(anchor="w", padx=12, pady=(12, 8))
        tk.Label(box, text=f"🕒 Time: {day} {time}", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=4)

        # Try to find course object to show more info
        code = title.split()[0].strip()
        found = None
        for c in self.courses:
            if c.code == code:
                found = c
                break

        if found:
            tk.Label(box, text=f"📌 Name: {found.name or '-'}", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=4)
            tk.Label(box, text=f"👩‍🏫 Instructor: {found.instructor or '-'}", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=4)
            tk.Label(box, text=f"🎓 Year: {found.year}", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=4)
            tk.Label(box, text=f"👥 Students: {found.students}", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=4)
        else:
            tk.Label(box, text="(Details from loaded data not found)", font=("Segoe UI", 11), bg="white").pack(anchor="w", padx=12, pady=8)

    # -------- Report Window ----------
    def open_report_window(self, result: Dict):
        win = tk.Toplevel(self.root)
        win.title("BeePlan - Validation Report")
        win.geometry("900x620")
        win.configure(bg="#cfe9ff")

        box = tk.Frame(win, bg="white")
        box.pack(fill="both", expand=True, padx=18, pady=18)

        tk.Label(box, text="BEEPLAN - VALIDATION REPORT", font=("Segoe UI", 22, "bold"),
                 bg="white", fg="#1665c1").pack(pady=(18, 10))

        summary = tk.Frame(box, bg="white")
        summary.pack(fill="x", padx=20, pady=10)

        tk.Label(summary, text=f"🔴 Critical Issues: {result['critical']}", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#d10000").pack(side="left", padx=10)
        tk.Label(summary, text=f"🟠 Warnings: {result['warnings']}", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#f39c12").pack(side="left", padx=10)
        compliance = int((result["rules_passed"] / max(1, result["rules_total"])) * 100)
        tk.Label(summary, text=f"✅ {compliance}% Compliance", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#1aa84a").pack(side="left", padx=10)

        ttk.Separator(box, orient="horizontal").pack(fill="x", padx=20, pady=15)

        # Issues detail (simple Week 9 placeholder)
        issues = tk.Frame(box, bg="white")
        issues.pack(fill="both", expand=True, padx=25, pady=10)

        tk.Label(issues, text="ISSUES DETAIL", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(0, 10))

        text = tk.Text(issues, height=18, font=("Consolas", 11))
        text.pack(fill="both", expand=True)

        # Fill with something meaningful
        text.insert("end", "CRITICAL ISSUES:\n")
        if result["conflicts"] > 0:
            text.insert("end", f"1) Not enough free slots for all courses. Conflicts={result['conflicts']}\n")
            text.insert("end", "   Solution: Move some courses to other days/times or add more slots.\n\n")
        else:
            text.insert("end", "None\n\n")

        text.insert("end", "WARNINGS:\n")
        text.insert("end", "1) Week 9 prototype uses a simple heuristic.\n")
        text.insert("end", "   Solution: Improve rules and constraints in later weeks.\n\n")

        text.insert("end", f"SUMMARY:\nScheduled Courses: {result['scheduled_courses']}\nRules Passed: {result['rules_passed']}/{result['rules_total']}\n")
        text.configure(state="disabled")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BeePlanFinalApp()
    app.run()
