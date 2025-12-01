package kidtask;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ChildProfile {
    private final String name;
    private int totalPoints;
    private int level;
    private final List<Task> tasks;
    private final List<Wish> wishes;

    public ChildProfile(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name must not be blank");
        }
        this.name = name.trim();
        this.tasks = new ArrayList<>();
        this.wishes = new ArrayList<>();
        recalculateLevel();
    }

    public String getName() {
        return name;
    }

    public int getTotalPoints() {
        return totalPoints;
    }

    public int getLevel() {
        return level;
    }

    public List<Task> getTasks() {
        return Collections.unmodifiableList(tasks);
    }

    public List<Wish> getWishes() {
        return Collections.unmodifiableList(wishes);
    }

    public void addTask(Task task) {
        if (task == null) {
            throw new IllegalArgumentException("Task must not be null");
        }
        tasks.add(task);
    }

    public void addWish(Wish wish) {
        if (wish == null) {
            throw new IllegalArgumentException("Wish must not be null");
        }
        wishes.add(wish);
    }

    public void completeTask(Task task) {
        if (task == null) {
            throw new IllegalArgumentException("Task must not be null");
        }
        if (!tasks.contains(task)) {
            throw new IllegalArgumentException("Task does not belong to this profile");
        }
        if (task.isCompleted()) {
            return;
        }
        task.setCompleted(true);
        totalPoints += task.getPoints();
        recalculateLevel();
    }

    public boolean canClaimWish(Wish wish) {
        if (wish == null) {
            return false;
        }
        return wishes.contains(wish) && wish.isApproved() && !wish.isClaimed() && totalPoints >= wish.getCost();
    }

    public void claimWish(Wish wish) {
        if (wish == null) {
            throw new IllegalArgumentException("Wish must not be null");
        }
        if (!wishes.contains(wish)) {
            throw new IllegalArgumentException("Wish does not belong to this profile");
        }
        if (!wish.isApproved()) {
            throw new IllegalStateException("Wish is not approved");
        }
        if (wish.isClaimed()) {
            throw new IllegalStateException("Wish already claimed");
        }
        if (totalPoints < wish.getCost()) {
            throw new IllegalStateException("Not enough points to claim wish");
        }
        totalPoints -= wish.getCost();
        wish.setClaimed(true);
        recalculateLevel();
    }

    private void recalculateLevel() {
        level = totalPoints / 50 + 1;
    }
}