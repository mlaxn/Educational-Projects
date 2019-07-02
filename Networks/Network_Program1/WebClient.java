package network;

import java.io.*;
import java.net.Socket;
//import java.net.URL;
//import java.nio.file.Files;

//declaration of the runnable for the Web client
public class WebClient implements Runnable {

    Socket conn_socket;

    //constructor for the Webclient
    WebClient(Socket iSock) {
        conn_socket = iSock;
    }

//setting up new thread for each run
    public void run() {
        try {
            main_function(conn_socket);
            return;
        } catch (IOException e) {
            System.out.println(e);
        }
    }

    //Handles the accepted request, parsing the input 
    private void main_function(Socket conn_socket) throws IOException {

        BufferedReader string_input = new BufferedReader(new InputStreamReader(conn_socket.getInputStream()));

        //System.out.println("Just connected to " + usock.getRemoteSocketAddress());
        String main_input, file;
        //reads the given input
        while ((main_input = string_input.readLine()) != null) {
            //breaks if no input
            if (main_input.length() == 0) {
                break;
            }
            if (main_input.contains("GET") || main_input.contains("POST")) {
                file = main_input.substring(4, main_input.length() - 9);
                System.out.println("Receiving data...");
                System.out.println("Check ");
                System.out.println("Requested File: " + file);

                screen_printer(conn_socket, file);
            }
            System.out.println(main_input);
        }
        System.out.println();
        conn_socket.close();
        string_input.close();
    }

    //makes a response by parsing the request and creating an output stream
    private void screen_printer(Socket usock, String request) {
        try {
            PrintWriter output_string = new PrintWriter(usock.getOutputStream());

            switch (request) {
                //in case if index is requested that following data is printed
                case "/index.html":
                    output_string.print("HTTP/1.1 200 OK \r\n");
                    output_string.print("Content Type: text/html\r\n");
                   System.out.println("Successfully received the file. \n");
                    output_string.print("Connection: close\r\n"); 
                    
                    output_string.print("\r\n"); // End of header
                    
                    String indexFile = fulltext_reader("index.html");
                    output_string.print(indexFile);

                    output_string.close();
                    break;
                    
                case "/":
                    output_string.print("HTTP/1.1 301 Moved Permanently \n");
                    output_string.print("Content Type: text/html\r\n"); // The type of data
                    output_string.print("Location: /index.html\r\n");
                    output_string.print("Connection: close\r\n"); // Will close stream
                    output_string.print("\r\n"); // End of header
                    output_string.close();
                    break;
                
                //if file is not found throws HTTP 404 File not found exception                  
                default:
                    output_string.print("HTTP/1.1 404 Not Found \r\n");
                    output_string.print("Content Type: text/html\r\n"); // The type of data
                    output_string.print("Connection: close\r\n"); // Will close stream
                    output_string.print("\r\n"); // End of header
                    output_string.close();
                    break;
            }

        } catch (Exception error) {
            System.err.print("Error: Please Try Again \n");
            System.err.println(error);
        }
    }

    //reads the text and returns the the information
    private String fulltext_reader(String fileName) throws IOException {
        
        InputStream fileStream = getClass().getResourceAsStream(fileName);
        BufferedReader fileLines = new BufferedReader(new InputStreamReader(fileStream));
        String line = fileLines.readLine();
        StringBuilder sb = new StringBuilder();

        while (line != null) {
            sb.append(line).append("\n");
            line = fileLines.readLine();
        }
        String fullFile = sb.toString();
        return fullFile;
    }

}
