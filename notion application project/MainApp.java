import java.io.BufferedReader; 
import java.io.InputStreamReader;
import java.util.Scanner;

public class MainApp {
    public static void main(String[] args) {
        // Using try-with-resources to automatically close the Scanner
        try (Scanner scanner = new Scanner(System.in)) {
            // Welcome message
            System.out.println("Welcome to the console application.");
            // Ask the user if they want to register or log in
            System.out.println("What would you like to do? (1) Register, (2) Login");
            int option = scanner.nextInt();  // Capture the user's choice (1 or 2)
            scanner.nextLine();  // Clear the input buffer after reading the integer

            // Prompt the user to enter their username
            System.out.print("Enter your username: ");
            String username = scanner.nextLine();

            // Prompt the user to enter their password
            System.out.print("Enter your password: ");
            String password = scanner.nextLine();

            // Determine the command to execute based on the chosen option
            String command = option == 1 ? "register" : "login";

            // Build the command to execute the Python script with the given arguments
            String[] commandArray = {"python3", "user_management.py", command, username, password};
            Process process = Runtime.getRuntime().exec(commandArray);  // Execute the external process

            // Read and print the output from the executed process (the Python script)
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);  // Print each line of output from the script
            }

            // Wait for the process to finish
            process.waitFor();
        } catch (Exception e) {
            // Display an error message if something goes wrong with the process
            System.out.println("Error interacting with the authentication system.");
        }
    }
}
