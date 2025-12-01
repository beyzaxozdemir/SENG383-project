package kidtask;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.List;

public class ChildDashboardFrame extends JFrame {
    private static final String[] TABLE_COLUMNS = {"Title", "Deadline", "Points", "Status"};

    private final ChildProfile profile;
    private final TaskFileRepository repository;
    private final DefaultTableModel tableModel;

    private final JLabel pointsLabel = new JLabel();
    private final JLabel levelLabel = new JLabel();
    private final JLabel statusLabel = new JLabel();

    public ChildDashboardFrame(ChildProfile profile, TaskFileRepository repository) {
        this.profile = profile;
        this.repository = repository;
        this.tableModel = new DefaultTableModel(TABLE_COLUMNS, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        setTitle("KidTask Dashboard");
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        setSize(700, 400);
        setLocationRelativeTo(null);

        initUI();
        loadTasksToProfile();
        refreshView();
    }

    private void initUI() {
        JTable taskTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(taskTable);

        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.add(pointsLabel);
        headerPanel.add(levelLabel);
        headerPanel.add(statusLabel);

        JButton addTaskButton = new JButton("Add Task");
        addTaskButton.addActionListener(e -> addTask());

        JButton completeTaskButton = new JButton("Mark as Completed");
        completeTaskButton.addActionListener(e -> markSelectedTask(taskTable.getSelectedRow()));

        JPanel buttonsPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonsPanel.add(addTaskButton);
        buttonsPanel.add(completeTaskButton);

        add(headerPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(buttonsPanel, BorderLayout.SOUTH);
    }

    private void loadTasksToProfile() {
        List<Task> loadedTasks = repository.loadTasks();
        loadedTasks.forEach(profile::addTask);
    }

    private void refreshView() {
        tableModel.setRowCount(0);
        for (Task task : profile.getTasks()) {
            tableModel.addRow(new Object[]{
                    task.getTitle(),
                    task.getDeadline(),
                    task.getPoints(),
                    task.isCompleted() ? "Completed" : "Pending"
            });
        }
        pointsLabel.setText("Total Points: " + profile.getTotalPoints());
        levelLabel.setText("Level: " + profile.getLevel());
        statusLabel.setText(profile.getTotalPoints() >= 100 ? "You're on fire!" : "Keep going!");
    }

    private void addTask() {
        String title = JOptionPane.showInputDialog(this, "Task Title:");
        if (title == null || title.isBlank()) {
            return;
        }
        String description = JOptionPane.showInputDialog(this, "Task Description:");
        if (description == null) {
            return;
        }
        String deadline = JOptionPane.showInputDialog(this, "Deadline:");
        if (deadline == null) {
            return;
        }
        String pointsInput = JOptionPane.showInputDialog(this, "Points:");
        if (pointsInput == null) {
            return;
        }
        int points;
        try {
            points = Integer.parseInt(pointsInput.trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Points must be a number.", "Invalid Input", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Task task = new Task(title.trim(), description.trim(), deadline.trim(), points, false);
        profile.addTask(task);
        repository.saveTasks(profile.getTasks());
        refreshView();
    }

    private void markSelectedTask(int selectedRow) {
        if (selectedRow < 0) {
            JOptionPane.showMessageDialog(this, "Select a task first.", "No Selection", JOptionPane.WARNING_MESSAGE);
            return;
        }
        Task task = profile.getTasks().get(selectedRow);
        profile.completeTask(task);
        repository.saveTasks(profile.getTasks());
        refreshView();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ChildProfile profile = new ChildProfile("Kiddo");
            TaskFileRepository repository = new TaskFileRepository();
            new ChildDashboardFrame(profile, repository).setVisible(true);
        });
    }
}