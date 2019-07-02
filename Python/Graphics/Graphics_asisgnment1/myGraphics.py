# Santosh Nepal
# 1001112034
#02/27/2018
#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been somewhat modified and updated by Brian A. Dalio for use
# in CSE 4303 / CSE 5365 in the 2018 Spring semester.

#----------------------------------------------------------------------
class cl_world :
    def __init__( self, objects = [], canvases = [] ) :
        self.objects = objects
        self.canvases = canvases

    def add_canvas( self, canvas ) :
        self.canvases.append( canvas )
        canvas.world = self

    def delete_file(self, canvas):
        canvas.delete("all")

    def create_graphic_objects( self, canvas ) :
        # 1. Create a line that goes from the upper left
        #    to the lower right of the canvas.
        self.objects.append( canvas.create_line(
                                                0, 0, canvas.cget( "width" ), canvas.cget( "height" ) ) )


        self.objects.append( canvas.create_line(
            canvas.cget( "width" ), 0, 0, canvas.cget( "height" ) ) )

        # 3. Create an oval that is centered on the canvas and
        #    is 50% as wide and 50% as high as the canvas.
        self.objects.append( canvas.create_oval(
            int( 0.25 * int( canvas.cget( "width" ) ) ),
            int( 0.25 * int( canvas.cget( "height" ) ) ),
            int( 0.75 * int( canvas.cget( "width" ) ) ),
            int( 0.75 * int( canvas.cget( "height" ) ) ) ) )

    def redisplay( self, canvas, event ) :
            if self.objects :
                canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
                canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
                canvas.coords(self.objects[ 2 ],
                              int( 0.25 * int( event.width ) ),
                              int( 0.25 * int( event.height ) ),
                              int( 0.75 * int( event.width ) ),
                              int( 0.75 * int( event.height ) ) )

    #----------------------------------------------------------------------


    def create_figure(self,canvas,X,Y,P1,P2,P3,window,viewportPoints):
        canvas.delete("all")

        self.objects.append(
            canvas.create_polygon(float(viewportPoints[0])*float(canvas.cget("width")), float(viewportPoints[1])*
                                  float(canvas.cget("height")),float(viewportPoints[0])*float(canvas.cget("width")),
                                  float(viewportPoints[3]) *float(canvas.cget("height")),float(viewportPoints[2])*
                                  float(canvas.cget("width")),float(viewportPoints[3])*
                                  float(canvas.cget("height")),float(viewportPoints[2])*float(canvas.cget("width")),
                                  float(viewportPoints[1])*float(canvas.cget("height")),fill='',outline='black'))

        Sx = (float(viewportPoints[2]) - float(viewportPoints[0]))/(float(window[2]) - float(window[0]))
        Sy = (float(viewportPoints[3]) - float(viewportPoints[1]))/(float(window[3]) - float(window[1]))
        height = int(canvas.cget("height"))

        for i in range(len(P1)):
            dx1 = float(X[ int(P1[i])-1]) - float(window[0])
            dy1 =    float(Y[ int(P1[i]) -1]) -float(window[1])

            dx2 =  float(X[ int(P2[i])-1]) -  float(window[0])
            dy2 =  float(Y[ int(P2[i]) -1])  -float(window[1])

            dx3 =  float(X[ int(P3[i])-1]) -  float(window[0])
            dy3 =  float(Y[ int(P3[i]) -1]) -float(window[1])


            X1Prime = (dx1 * Sx) + float(viewportPoints[0])
            Y1Prime = height -(((dy1 * Sy) + float(viewportPoints[1])) * height)
            X2Prime = (dx2 * Sx) + float(viewportPoints[0])
            Y2Prime = height-(((dy2 * Sy) + float(viewportPoints[1])) * height)
            X3Prime = (dx3 * Sx) +  float(viewportPoints[0])
            Y3Prime = height -(((dy3 * Sy) + float(viewportPoints[1])) * height)

            self.objects.append(canvas.create_polygon(X1Prime * int(canvas.cget("width")),Y1Prime,X2Prime * int(canvas.cget("width")),Y2Prime,X3Prime* int(canvas.cget("width")),Y3Prime,fill='white', outline='black'))


