import wx
import math
import puzzle
from wx.lib.colourdb import getColourList
from random import randint


class GeometricPuzzleFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="Geometric Puzzle Solver", pos=wx.DefaultPosition,
                          size=wx.Size(700, 600))
        wx.EVT_CLOSE(self, self.on_quit)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        wx.EVT_SIZE(self, self.on_size)
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        id_quit = wx.NewId()
        file_menu.Append(id_quit, "&Quit", "Quit Solver")
        wx.EVT_MENU(self, id_quit, self.on_quit)

        menu_bar.Append(file_menu, "&File")

        menu_about = wx.Menu()

        id_info = wx.NewId()
        menu_about.Append(id_info, "&Info", "Shows info")
        wx.EVT_MENU(self, id_info, self.on_info)

        menu_bar.Append(menu_about, "&About")

        self.puzzle = puzzle.Puzzle("../models/simple.model")
        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()
        self.SetStatusText("Ready")

        self.box_width = 0
        self.box_height = 0
        self.rows = 4
        self.cols = 4
        self.grid_size = 0
        self.window_width = 0
        self.window_height = 0
        self.left = 0
        self.border = 0
        self.vertices = []

    def on_quit(self, event):
        self.Destroy()

    def refresh_window(self):
        dc = wx.PaintDC(self)
        dc.BeginDrawing
        dc.DrawRectangle(0, 0, self.window_width, self.window_height)

        # dc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))
        # for row in range(self.rows):
        #     dc.DrawLine(self.vertices[0].x, self.vertices[0].y + self.grid_size * row, self.vertices[1].x,
        #                 self.vertices[0].y + self.grid_size * row)
        #
        # for col in range(self.cols):
        #     dc.DrawLine(self.vertices[0].x + self.grid_size * col, self.vertices[0].y,
        #                 self.vertices[0].x + self.grid_size * col, self.vertices[2].y)

        # dc.SetPen(wx.Pen(wx.BLACK, 1))
        # dc.DrawLines(self.vertices)
        self.draw_puzzle(dc, self.puzzle)


    def draw_puzzle(self, dc, puzzle):

        model = puzzle.get_model()
        for row in range(len(model)):
            for col in range(len(model[row])):
                index = 100 + puzzle.get_color_index(str(model[row][col])) * 25
                dc.SetBrush(wx.Brush(getColourList()[index]))
                dc.DrawRectangle(self.left + self.border + row * self.grid_size, self.top + self.border + col * self.grid_size, self.grid_size, self.grid_size)
                print model[row][col]


    def on_paint(self, event):
        self.refresh_window()

    def on_size(self, event):
        self.compute_size()
        self.refresh_window()

    def compute_size(self):
        border = 25
        width, height = self.GetSizeTuple()
        ratio = self.rows / float(self.cols)

        if width * ratio >= height:
            self.left = (width - height + border) / 2
            self.top = border
            upper_left = wx.Point(self.left + border, border)
            upper_right = wx.Point(height - border, border)
            lower_left = wx.Point(self.left + border, height - self.left - border)
            lower_right = wx.Point(height - border, height - self.left - border)
        else:
            self.left = border
            self.top = (height - width + border) / 2
            upper_left = wx.Point(border, self.top)
            upper_right = wx.Point(width - border, self.top)
            lower_left = wx.Point(border, height - self.top - border)
            lower_right = wx.Point(width - border, height - self.top - border)

        self.window_width = width
        self.window_height = height
        self.box_width = upper_right.x - upper_left.x
        self.box_height = upper_left.y - lower_left.y
        self.vertices = [upper_left, upper_right, lower_right, lower_left, upper_left]
        self.grid_size = self.box_width / self.cols


    def on_info(self, event):

        licence = """GeometricPuzzle is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

Cartographer is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('puzzle.png', wx.BITMAP_TYPE_PNG))
        info.SetName('GeometricPuzzles')
        info.SetVersion('1.0')
        info.SetDescription("GeometricPuzzles is a solver")
        info.SetCopyright('(C) 2014 Andrea Iacono')
        info.SetWebSite('http://www.github.com/andreaiacono')
        info.SetLicence(licence)
        info.AddDeveloper('Andrea Iacono')
        info.AddDocWriter('Andrea Iacono')

        wx.AboutBox(info)


class GeometricPuzzleApplication(wx.App):
    def OnInit(self):
        frame = GeometricPuzzleFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        # self.SetSize(800, 600)
        return True


colors = []

for i in range(255):
    colors.append('%06X' % randint(0, 0xFFFFFF))

app = GeometricPuzzleApplication()
app.MainLoop()
