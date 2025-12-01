package kidtask;

public class Task {
    private String title;
    private String description;
    private String deadline;
    private int points;
    private boolean completed;

    public Task(String title, String description, String deadline, int points, boolean completed) {
        this.title = title;
        this.description = description;
        this.deadline = deadline;
        this.points = points;
        this.completed = completed;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDeadline() {
        return deadline;
    }

    public void setDeadline(String deadline) {
        this.deadline = deadline;
    }

    public int getPoints() {
        return points;
    }

    public void setPoints(int points) {
        this.points = points;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }
}