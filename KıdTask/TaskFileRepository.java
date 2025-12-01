package kidtask;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class TaskFileRepository {
    private static final String FILE_NAME = "Tasks.txt";
    private static final String DELIMITER = ";";

    private final Path filePath;

    public TaskFileRepository() {
        this(Path.of(FILE_NAME));
    }

    public TaskFileRepository(Path filePath) {
        this.filePath = filePath;
    }

    public List<Task> loadTasks() {
        List<Task> tasks = new ArrayList<>();
        if (!Files.exists(filePath)) {
            return tasks;
        }

        try (BufferedReader reader = Files.newBufferedReader(filePath, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                Task task = parseLine(line);
                if (task != null) {
                    tasks.add(task);
                }
            }
        } catch (IOException e) {
            throw new IllegalStateException("Failed to read tasks from " + filePath, e);
        }
        return tasks;
    }

    public void saveTasks(List<Task> tasks) {
        try (BufferedWriter writer = Files.newBufferedWriter(filePath, StandardCharsets.UTF_8)) {
            for (Task task : tasks) {
                writer.write(formatTask(task));
                writer.newLine();
            }
        } catch (IOException e) {
            throw new IllegalStateException("Failed to write tasks to " + filePath, e);
        }
    }

    private Task parseLine(String line) {
        String[] parts = line.split(DELIMITER, -1);
        if (parts.length != 5) {
            return null;
        }
        try {
            String title = parts[0];
            String description = parts[1];
            String deadline = parts[2];
            int points = Integer.parseInt(parts[3]);
            boolean completed = Boolean.parseBoolean(parts[4]);
            return new Task(title, description, deadline, points, completed);
        } catch (NumberFormatException ex) {
            return null;
        }
    }

    private String formatTask(Task task) {
        return String.join(DELIMITER,
                task.getTitle(),
                task.getDescription(),
                task.getDeadline(),
                String.valueOf(task.getPoints()),
                String.valueOf(task.isCompleted()));
    }
}