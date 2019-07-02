/*
Milan Biswakarma
CSE 4344-002
Assignment# 1
9th March, 2018
*/
package network;


public class Network {
    
    //main function to set up the newwork by starting the server provided:8090
    public static void main(String args[]) {
        Thread listen = new Thread(new WebServer(8090));
        listen.start();
    } 
    
}