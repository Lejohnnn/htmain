package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;

public final class App {
    private App() {
    }

    /**
     * Says hello to the world.
     * @param args The arguments of the program.
     */
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/swimmingorg";
        String user = "postgres";
        String password = "Youngmagic11!!";

        try (Connection connection = DriverManager.getConnection(url, user, password)) {
            if (connection != null) {
                System.out.println("Connected to the database!");

                System.out.println("1 | Name(s) of caretakers who are the primary (main) caretakers of at least two swimmers");
                System.out.println("2 | Name(s) of swimmers who have a caretaker that is also a swimmer");
                System.out.println("3 | Name(s) of swimmers and their phone numbers");
                System.out.println("4 | Quit");

                try (Scanner userinput = new Scanner(System.in)) {
                    System.out.println("Please enter your choice: ");
                    int choice = userinput.nextInt();

                    Statement statement = connection.createStatement();
                    ResultSet result = null;

                    switch (choice) {
                        case 1:
                            String sql1 = "SELECT caretaker_name FROM caretaker WHERE caretaker_id IN (SELECT caretaker_id FROM caretaker_swimmer GROUP BY caretaker_id HAVING COUNT(caretaker_id) >= 2)";
                            result = statement.executeQuery(sql1);

                            while (result.next()) {
                                System.out.println(result.getString("caretaker_name"));
                            }
                            break;

                        case 2:
                            String sql2 = "SELECT swimmer_name FROM swimmer WHERE caretaker_id IN (SELECT caretaker_id FROM caretaker_swimmer WHERE swimmer_id IN (SELECT swimmer_id FROM caretaker_swimmer))";
                            result = statement.executeQuery(sql2);

                            while (result.next()) {
                                System.out.println(result.getString("swimmer_name"));
                            }
                            break;     

                        case 3: 
                            String sql3 = "SELECT swimmer_name, phone_number FROM swimmer";
                            result = statement.executeQuery(sql3);

                            while (result.next()) {
                                System.out.println(result.getString("swimmer_name") + " | " + result.getString("phone_number"));
                            }
                            break;
                    
                        case 4:
                            System.out.println("Goodbye!");
                            break;          
                    }

                    if (result != null) {
                        result.close();
                    }
                    statement.close();
                }
                connection.close();

            } else {
                System.out.println("Failed to make connection!");
            }
        } catch (SQLException e) {
            System.out.println("SQL Exception: " + e.getMessage());
        }
    }
}
