import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/* ===== Interface ===== */
interface Billable {
    double calculateTotal();
}

/* ===== Abstract Base Class ===== */
abstract class BaseOrder implements Billable {
    protected int orderId;
    protected String customer;
    protected double amount;

    public BaseOrder(int orderId, String customer, double amount) {
        this.orderId = orderId;
        this.customer = customer;
        this.amount = amount;
    }

    public abstract String getType();

    @Override
    public String toString() {
        return "OrderID=" + orderId +
               ", Customer=" + customer +
               ", Type=" + getType() +
               ", Total=" + calculateTotal();
    }
}

/* ===== Child Classes ===== */
class OnlineOrder extends BaseOrder {

    public OnlineOrder(int id, String customer, double amount) {
        super(id, customer, amount);
    }

    @Override
    public double calculateTotal() {
        return amount + (amount * 0.18); // 18% tax
    }

    @Override
    public String getType() {
        return "Online";
    }
}

class StoreOrder extends BaseOrder {

    public StoreOrder(int id, String customer, double amount) {
        super(id, customer, amount);
    }

    @Override
    public double calculateTotal() {
        return amount + (amount * 0.12); // 12% tax
    }

    @Override
    public String getType() {
        return "Store";
    }
}

/* ===== Logger Runnable ===== */
class OrderLogger implements Runnable {
    private final String message;

    public OrderLogger(String message) {
        this.message = message;
    }

    @Override
    public void run() {
        try (FileWriter fw = new FileWriter("order.log", true)) {
            fw.write(LocalDateTime.now() + " : " + message + "\n");
        } catch (IOException e) {
            System.out.println("Logging failed");
        }
    }
}

/* ===== MAIN CLASS ===== */
public class Order {

    public static void main(String[] args) {

        System.out.println("=== Order Processing Started ===");

        List<BaseOrder> orders = new ArrayList<>();

        // Predefined data (NO INPUT)
        orders.add(new OnlineOrder(101, "Boobesh", 5000));
        orders.add(new StoreOrder(102, "Anand", 8000));
        orders.add(new OnlineOrder(103, "Kumar", 12000));
        orders.add(new StoreOrder(104, "Ravi", 3000));

        ExecutorService executor = Executors.newFixedThreadPool(2);

        double totalRevenue = 0;

        for (BaseOrder order : orders) {
            System.out.println(order);
            totalRevenue += order.calculateTotal();
            executor.execute(new OrderLogger("Processed order " + order.orderId));
        }

        executor.shutdown();

        System.out.println("--------------------------------");
        System.out.println("Total Orders : " + orders.size());
        System.out.println("Total Revenue: " + totalRevenue);
        System.out.println("=== Order Processing Completed ===");
    }
}
