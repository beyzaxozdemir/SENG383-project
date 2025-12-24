# BeePlan – Department Course Scheduling System

BeePlan is a Python-based desktop application designed to help university departments create weekly course schedules in a structured and conflict-free manner.  
The system considers instructor availability, classroom capacity, and time-slot constraints while generating schedules and visually reports conflicts to the user.


## **Project Purpose

The goal of BeePlan is to:

- Generate weekly department course schedules automatically  
- Prevent time, instructor, and classroom conflicts  
- Validate input data before scheduling  
- Provide clear visual feedback through a graphical interface  
- Apply Object-Oriented Programming principles in a real-world academic project  

---

## **User Roles & Features

BeePlan is designed as a department-level scheduling tool with a single user perspective:

### **Department Scheduler (User)

- Load course, instructor, and classroom data from JSON files  
- Generate weekly schedules based on predefined constraints  
- Detect and visualize scheduling conflicts  
- View generated schedules in tabular format  
- Export validation and conflict reports  

---

## **Main Functionalities

- Course scheduling and time-slot assignment  
- Instructor availability validation  
- Classroom capacity and availability checks  
- Conflict detection (time, instructor, classroom, capacity)  
- Visual schedule representation via GUI  
- Validation report generation  

---

## **How to Run the Project

1. Open the project directory on your local machine  
2. Make sure **Python 3.8 or higher** is installed  
3. Navigate to the `src` folder  
4. Run the application using the following command:

---

## **Object-Oriented Design

The project follows core OOP principles:

- **Encapsulation:**  
  All data models (Course, Instructor, Classroom) use private fields with controlled access  

- **Separation of Concerns:**  
  Scheduling logic, data models, and GUI components are separated into different modules  

- **Modularity:**  
  The Scheduler class operates independently from the GUI and data-loading components  

- **Reusability:**  
  Core scheduling and validation logic can be reused or extended for future enhancements  

---

## **AI Tool Usage

Different AI-powered tools were used responsibly during various stages of the development lifecycle.  
All AI outputs were reviewed, revised, and adapted manually by the developer.

### **DeepSeek / OpenAI

- Used during testing and debugging phases  
- Assisted in identifying logical errors and infinite loop scenarios  
- Helped improve validation and error-handling strategies  

### **GitHub Copilot / Cursor

- Used during the coding phase  
- Provided code scaffolding and refactoring suggestions  
- Assisted with function structure and syntax correction  

### **Canva & Figma

- Used during the design phase  
- Helped create GUI mockups and layout ideas  
- Supported visualization of user workflow before implementation  

### **Claude

- Used during report writing  
- Assisted in structuring explanations and improving academic tone  
- All generated content was manually reviewed and customized  

‼️ All AI tools were used ethically as support mechanisms.  
Final design decisions, algorithms, and implementations reflect the developer’s own effort and understanding.

---

## **Folder & File Descriptions

### **src/**
Contains all source code files.

- `beeplan_app.py` – Main application entry point and GUI logic  
- `scheduler.py` – Scheduling algorithm and conflict detection logic  

### **src/data/**
Stores application input data in JSON format.

- `Courses.json` – Course information  
- `Instructors.json` – Instructor availability data  
- `Classrooms.json` – Classroom capacity and availability data  

### **docs/**
Contains design and documentation files.

- Class Diagram  
- Activity Diagram  
- GUI mockups and final screenshots  

### **video/**
Contains the final presentation and demo video.

---

## **Developer Information

**Name:** Beyza Nur Özdemir- 202228402
**Role:** Student B  
**Course:** SENG 383 – Software Project III  

---

## **Notes

- This project was developed for academic purposes within the SENG 383 course  
- All data is stored locally using JSON files  
- The application is designed as a desktop application using Python and Tkinter  

---

## **Final Status

✔ All core requirements implemented  
✔ AI usage documented transparently  
✔ Ready for final submission  

