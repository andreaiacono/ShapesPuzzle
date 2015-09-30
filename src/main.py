import wx
import math
import puzzle
from wx.lib.colourdb import getColourList
from random import randint
import solver


class GeometricPuzzleFrame(wx.Frame):
    def __init__(self):

        self.puzzle = puzzle.Puzzle("../models/default.model")

        self.box_width = 0
        self.box_height = 0
        self.rows = len(self.puzzle.get_model()[0])
        self.cols = self.rows
        self.grid_size = 0
        self.window_width = 0
        self.window_height = 0
        self.left = 0
        self.top = 0
        self.border = 0
        self.vertices = []

        self.solver = solver.Solver(self.puzzle)

        wx.Frame.__init__(self, parent=None, id=-1, title="Geometric Puzzle Solver", pos=wx.DefaultPosition,
                          size=wx.Size(700, 600))
        wx.EVT_CLOSE(self, self.on_quit)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        wx.EVT_SIZE(self, self.on_size)
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        id_open = wx.NewId()
        file_menu.Append(id_open, "&Open", "Open model")
        wx.EVT_MENU(self, id_open, self.loadFile)

        id_quit = wx.NewId()
        file_menu.Append(id_quit, "&Quit", "Quit Solver")
        wx.EVT_MENU(self, id_quit, self.on_quit)

        menu_bar.Append(file_menu, "&File")

        solve_menu = wx.Menu()
        id_solve = wx.NewId()
        solve_menu.Append(id_solve, "&Next solution", "Next solution")
        wx.EVT_MENU(self, id_solve, self.next_solution)
        menu_bar.Append(solve_menu, "&Solve")

        menu_about = wx.Menu()
        id_info = wx.NewId()
        menu_about.Append(id_info, "&Info", "Shows info")
        wx.EVT_MENU(self, id_info, self.on_info)

        menu_bar.Append(menu_about, "&About")

        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()
        self.SetStatusText("Ready")

    def loadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "Python files (*.model)|*.model", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        filename = openFileDialog.GetPath()
        openFileDialog.Destroy()
        self.puzzle = puzzle.Puzzle(filename)
        self.refresh_window()

    def next_solution(self, event):
        self.solver.next()

    def on_quit(self, event):
        self.Destroy()

    def refresh_window(self):
        dc = wx.PaintDC(self)
        dc.BeginDrawing
        dc.SetBrush(wx.Brush(wx.LIGHT_GREY))
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))
        dc.DrawRectangle(0, 0, self.window_width, self.window_height)

        dc.SetPen(wx.Pen(wx.BLACK, 1))

        # grid
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
                color_index = puzzle.get_color_index(model[row][col]) * 21
                dc.SetBrush(wx.Brush(getColourList()[color_index]))
                dc.DrawRectangle(self.left + row * self.grid_size, self.top + col * self.grid_size, self.grid_size, self.grid_size)
                # dc.DrawLines(self.vertices)

    def on_paint(self, event):
        self.refresh_window()

    def on_size(self, event):
        self.compute_size()
        self.refresh_window()

    def compute_size(self):
        border = 20
        width, height = self.GetClientSizeTuple()
        # ratio = self.rows / float(self.cols)

        if width >= height:
            self.left = (width - height + border) / 2
            self.top = border
            upper_left = wx.Point(self.left, self.top)
            upper_right = wx.Point(self.left + height - border*2, self.top)
            lower_left = wx.Point(self.left, height - self.top)
            lower_right = wx.Point(self.left + height - border*2, height - self.top)
        else:
            self.left = border
            self.top = (height - width + border) / 2
            upper_left = wx.Point(self.left, self.top)
            upper_right = wx.Point(width - self.left, self.top)
            lower_left = wx.Point(self.left, height - self.top - self.left)
            lower_right = wx.Point(width - self.left, height - self.top - self.left)

        self.window_width = width
        self.window_height = height
        self.box_width = upper_right.x - upper_left.x
        self.box_height = lower_left.y - upper_left.y
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

        info.SetIcon(wx.Icon('../img/puzzle.png', wx.BITMAP_TYPE_PNG))
        info.SetName('GeometricPuzzles')
        info.SetVersion('1.0')
        info.SetDescription("GeometricPuzzles is a solver for geometric puzzles.")
        info.SetCopyright('Written by Andrea Iacono')
        info.SetWebSite('http://www.github.com/andreaiacono/GeometricPuzzle')
        info.SetLicence(licence)
        info.AddDeveloper('Andrea Iacono')
        info.AddDocWriter('Andrea Iacono')

        wx.AboutBox(info)


class GeometricPuzzleApplication(wx.App):
    def OnInit(self):
        frame = GeometricPuzzleFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = GeometricPuzzleApplication()
app.MainLoop()
