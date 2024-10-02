import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Scanner;

public class MainApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the console application.");
        System.out.println("What would you like to do? (1) Register, (2) Login");
        int option = scanner.nextInt();
        scanner.nextLine();  

        System.out.print("Enter your username: ");
        String username = scanner.nextLine();

        System.out.print("Enter your password: ");
        String password = scanner.nextLine();

        String command = option == 1 ? "register" : "login";

        
        try {
            String[] commandArray = {"python3", "user_management.py", command, username, password};
            Process process = Runtime.getRuntime().exec(commandArray);

            
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            process.waitFor();
        } catch (Exception e) {
            System.out.println("Error interacting with the authentication system.");
            e.printStackTrace();
        }
    }
}
