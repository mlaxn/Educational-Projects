/*
Milan Biswakarma
CSE 4344-002
Assignment# 1
9th March, 2018
*/

package network;

//import java.io.BufferedReader;
//import java.io.InputStreamReader;
//import java.io.PrintWriter;
//import java.util.logging.Level;
//import java.util.logging.Logger;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;


//declaration of the runnable for webserver
public class WebServer implements Runnable{
    private ServerSocket sock;
    private Socket conn_socket;
    private int port_number;
    
//seting the constructor for the WebServer 
    WebServer(int iport){port_number = iport;}

//setting up for the theread for each run
    public void run(){
        try{                
            listen_socket_conn();
        }
        catch (Exception e){
            System.out.println(e);
        }
    }
    
    //Listens for the connection from the client and display the message
    public void listen_socket_conn(){        
        try {
            
            sock = new ServerSocket(port_number);
            System.out.println("Ready to Connect... \n");
            wait_Connection();
            sock.close();
        } 
        catch (IOException ex) {
            System.out.println(ex);
        }
        
    }
    //waits and sets up the connection with a new thread
    private void wait_Connection() throws IOException{
        while(true){
                conn_socket = sock.accept();
                Thread handle = new Thread(new WebClient(conn_socket));
                handle.start();
        }           
    }
    
}