package kidtask;

public class Wish {
    private String name;
    private int cost;
    private boolean approved;
    private boolean claimed;

    public Wish(String name, int cost, boolean approved, boolean claimed) {
        this.name = name;
        this.cost = cost;
        this.approved = approved;
        this.claimed = claimed;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getCost() {
        return cost;
    }

    public void setCost(int cost) {
        this.cost = cost;
    }

    public boolean isApproved() {
        return approved;
    }

    public void setApproved(boolean approved) {
        this.approved = approved;
    }

    public boolean isClaimed() {
        return claimed;
    }

    public void setClaimed(boolean claimed) {
        this.claimed = claimed;
    }
}