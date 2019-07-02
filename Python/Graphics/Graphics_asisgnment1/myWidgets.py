# Santosh Nepal
# 1001112034
# 02/27/2018

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been somewhat modified and updated by Brian A. Dalio for use
# in CSE 4303 / CSE 5365 in the 2018 Spring semester.

#----------------------------------------------------------------------
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import csv
import sys

#----------------------------------------------------------------------
#import self as self


class cl_widgets :
    def __init__( self, ob_root_window, ob_world = [] ) :
        self.ob_root_window = ob_root_window
        self.ob_world = ob_world
        self.buttons_panel_01 = cl_buttons_panel_01( self )
        #  self.buttons_panel_02 = cl_buttons_panel_02( self )

        self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
        self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )

        self.ob_canvas_frame = cl_canvas_frame( self )
        self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

#----------------------------------------------------------------------
class cl_canvas_frame :
    def __init__( self, master ) :
        self.master = master
        self.canvas = tk.Canvas(master.ob_root_window, width=640, height=480, bg="yellow" )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
        self.canvas.bind( "<Configure>",       self.canvas_resized_callback )
        self.canvas.bind( "<ButtonPress-1>",   self.left_mouse_click_callback )
        self.canvas.bind( "<ButtonRelease-1>", self.left_mouse_release_callback )
        self.canvas.bind( "<B1-Motion>",       self.left_mouse_down_motion_callback )
        self.canvas.bind( "<ButtonPress-3>",   self.right_mouse_click_callback )
        self.canvas.bind( "<ButtonRelease-3>", self.right_mouse_release_callback )
        self.canvas.bind( "<B3-Motion>",       self.right_mouse_down_motion_callback )
        self.canvas.bind( "<Key>",             self.key_pressed_callback )
        self.canvas.bind( "<Up>",              self.up_arrow_pressed_callback )
        self.canvas.bind( "<Down>",            self.down_arrow_pressed_callback )
        self.canvas.bind( "<Right>",           self.right_arrow_pressed_callback )
        self.canvas.bind( "<Left>",            self.left_arrow_pressed_callback )
        self.canvas.bind( "<Shift-Up>",        self.shift_up_arrow_pressed_callback )
        self.canvas.bind( "<Shift-Down>",      self.shift_down_arrow_pressed_callback )
        self.canvas.bind( "<Shift-Right>",     self.shift_right_arrow_pressed_callback )
        self.canvas.bind( "<Shift-Left>",      self.shift_left_arrow_pressed_callback )
        self.canvas.bind( "f",                 self.f_key_pressed_callback )
        self.canvas.bind( "b",                 self.b_key_pressed_callback )

    def key_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Key pressed" )

    def up_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Up arrow pressed" )

    def down_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","Down arrow pressed" )

    def right_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Right arrow pressed" )

    def left_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Left arrow pressed" )

    def shift_up_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Shift up arrow pressed" )

    def shift_down_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Shift down arrow pressed" )

    def shift_right_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Shift right arrow pressed" )

    def shift_left_arrow_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "Shift left arrow pressed" )

    def f_key_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "f key pressed" )

    def b_key_pressed_callback( self, event ) :
        self.master.statusBar_frame.set( "%s", "b key pressed" )

    def left_mouse_click_callback( self, event ) :
        self.master.statusBar_frame.set( "%s",
                                         "LMB clicked. (" + str( event.x ) + ", " + str( event.y ) + ")" )
        self.x = event.x
        self.y = event.y
        self.canvas.focus_set()

    def left_mouse_release_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","LMB released. (" + str( event.x ) + ", "+ str( event.y ) + ")" )
        self.x = None
        self.y = None

    def left_mouse_down_motion_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","LMB down motion. ("+ str( event.x ) + ", "+ str( event.y ) + ")" )
        self.x = event.x
        self.y = event.y

    def right_mouse_click_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","RMB clicked. (" + str( event.x ) + ", " + str( event.y ) + ")" )
        self.x = event.x
        self.y = event.y

    def right_mouse_release_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","RMB released. (" + str( event.x ) + ", " + str( event.y ) + ")" )
        self.x = None
        self.y = None

    def right_mouse_down_motion_callback( self, event ) :
        self.master.statusBar_frame.set( "%s","RMB down motion. (" + str( event.x ) + ", " + str( event.y ) + ")" )
        self.x = event.x
        self.y = event.y

    def canvas_resized_callback( self, event ) :
        self.canvas.config( width = event.width-4, height = event.height-4 )
        self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
        self.master.statusBar_frame.set( "%s",
                                     "Canvas width, height (" + str( self.canvas.cget( "width" ) ) +
                                     ", " + str( self.canvas.cget( "height" ) ) + ")" )

        self.canvas.pack()

        self.master.ob_world.redisplay( self.master.ob_canvas_frame.canvas, event )

#----------------------------------------------------------------------
class cl_buttons_panel_01 :
    fName = " "
    def __init__( self, master ) :
        self.master = master
        frame = tk.Frame( master.ob_root_window )
        frame.pack()

        self.var_filename = tk.StringVar()
        self.var_filename.set( "" )


        self.clear_button = tk.Button( frame, text = "Clear", fg = "red", command = self.clear_figure )
        self.clear_button.pack( side = tk.LEFT )

        self.load_button = tk.Button( frame, text = "Load", fg = "blue", command = self.load_file )
        self.load_button.pack( side = tk.LEFT )
        self.draw_button = tk.Button( frame, text = "Draw", command= self.draw_file)
        self.draw_button.pack(side = tk.LEFT)




    def load_file( self ) :
        global vertices
        global face
        vertices = 0
        face = 0
        keyword = []
        fName = tk.filedialog.askopenfilename( filetypes = [ ( "allfiles", "*" ), ( "pythonfiles", "*.txt" ) ] )
        if ( len( fName ) == 0 ) :
            msg = "[Enter was cancelled]"
        else :
            self.var_filename.set( fName )
            msg = "Filename is '%s'" % ( self.var_filename.get() )




        #msg = " '%d' Vertices, '%d' faces " %(vertices,face)

        global filename
        filename= self.var_filename.get()
        self.master.statusBar_frame.set( "%s", msg )

    def count_lines(self):

        File2= open(filename,'r')
        lines = 0
        for lines in File2:
            keyword = sys.argv[0]
            if keyword=='v':
                vertices = vertices+1
            elif keyword == 'f':
                face = face+1
            else:
                lines = lines+1
        lines += 1

        print("Vertices = %d, faces= %d"%(vertices,face))







    #Here fName has path for that file.
    #Load that file as draw button is pressed


    def draw_file(self):
        value = 0
        myFile = open(filename,'r')
        global X
        global Y
        global Z
        global P1
        global P2
        global P3

        global WindowData
        global ViewPortData
        X=[]
        Y=[]
        Z=[]
        P1=[]
        P2=[]
        P3=[]

        WindowData =[]
        ViewPortData =[]

        for line in myFile:
            if(line[0]== 'v'):
                temp=line.split(' ')
                X.append(temp[1])
                Y.append(temp[2])
                Z.append(temp[3])


            if(line[0]== 'f'):
                temp=line.split(' ')
                P1.append(temp[1])
                P2.append(temp[2])
                P3.append(temp[3])


            if (line[0] == 'w'):
                temp=line.split(' ')
                WindowData.append(temp[1])
                WindowData.append(temp[2])
                WindowData.append(temp[3])
                WindowData.append(temp[4])

            if(line[0]== 's'):
                temp=line.split(' ')
                ViewPortData.append(temp[1])
                ViewPortData.append(temp[2])
                ViewPortData.append(temp[3])
                ViewPortData.append(temp[4])

            value = value+1
        global  val
        val=1


        self.master.ob_world.create_figure( self.master.ob_canvas_frame.canvas,X,Y,P1,P2,P3,WindowData,ViewPortData )
        self.master.statusBar_frame.set( "Drew %d Vertices, %d Faces" %(len(X),len(P1)) )


    def clear_figure(self):
        self.master.ob_world.delete_file(self.master.ob_canvas_frame.canvas)
        self.master.statusBar_frame.set( "%s", "Cleared the data" )


class cl_statusBar_frame( tk.Frame ) :
    def __init__( self, master ) :

        tk.Frame.__init__( self, master )
        self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
        self.label.pack( fill = tk.X )

    def set( self, formatStr, *args ) :

        self.label.config( text = "(Santosh Nepal)  "+ formatStr % args)
        self.label.update_idletasks()

    def clear( self ) :
        self.label.config( text=" Santosh Nepal" )
        self.label.update_idletasks()

