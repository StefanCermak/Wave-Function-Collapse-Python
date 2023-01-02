from tkinter import *
import os.path
from globals import *


class ClassConfigDialog:
    def __init__(self):
        self.design = DEFAULT_DESIGN
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.pieces_per_col = DEFAULT_PIECES_PER_COL
        self.pieces_per_row = DEFAULT_PIECES_PER_ROW

        self.MainWindow = Tk()

        self.label_screenwidth = Label(self.MainWindow, text="Window Size")
        self.label_design = Label(self.MainWindow, text="Design")
        self.label_parts = Label(self.MainWindow, text="# of Parts")

        self.slider_window_width = Scale(self.MainWindow, from_=100, to=1600, orient=HORIZONTAL, length=240)
        self.slider_window_width.set(self.window_width)

        self.slider_pieces_per_row = Scale(self.MainWindow, from_=3, to=40, orient=HORIZONTAL, length=240)
        self.slider_pieces_per_row.set(self.pieces_per_row)
        self.slider_pieces_per_col = Scale(self.MainWindow, from_=3, to=40, orient=VERTICAL, length=240)
        self.slider_pieces_per_col.set(self.pieces_per_col)

        found_designs = os.listdir('Designes')
        for hide_name in [".DS_Store", ".", ".."]:
            if hide_name in found_designs:
                found_designs.remove(hide_name)

        self.SVar_selected_design = StringVar(self.MainWindow )
        if self.design in found_designs:
            self.SVar_selected_design.set(self.design)
        else:
            self.SVar_selected_design.set(found_designs[0])

        self.option_menu_select_design = OptionMenu(self.MainWindow, self.SVar_selected_design, *found_designs)
        self.SVar_selected_design.trace_add("write", lambda var, index, mode: self.update_preview())

        self.canvas_preview = Canvas(self.MainWindow, width = 240, height = 240)
        if os.path.exists(os.path.join("Designes", self.SVar_selected_design.get(), "symbol.png")):
            self.PhotoImage_preview = PhotoImage(file=os.path.join(os.path.join("Designes", self.SVar_selected_design.get(), "symbol.png")))
            self.canvas_preview.create_image(0, 0, anchor=NW, image=self.PhotoImage_preview)

        self.button_go = Button(self.MainWindow, text="Go", command=self.go)

        self.label_screenwidth.grid(row=0, column=0, columnspan=1, sticky="SE")
        self.slider_window_width.grid(row=0, column=1, columnspan=1, sticky="W")

        self.label_design.grid(row=1, column=0, sticky="E")
        self.option_menu_select_design.grid(row=1, column=1, sticky="W")

        self.label_parts.grid(row=2,column=0, sticky="SE")
        self.slider_pieces_per_row.grid(row=2, column=1)
        self.slider_pieces_per_col.grid(row=3,column=0, rowspan=1, sticky="E")
        self.canvas_preview.grid(row=3, column=1)
        self.button_go.grid(row=4,column=0, columnspan=2)

    def update_preview(self):
        if os.path.exists(os.path.join("Designes", self.SVar_selected_design.get(), "symbol.png")):
            self.PhotoImage_preview = PhotoImage(file=os.path.join(os.path.join("Designes", self.SVar_selected_design.get(), "symbol.png")))
            self.canvas_preview.delete("all")
            self.canvas_preview.create_image(0, 0, anchor=NW, image=self.PhotoImage_preview)
        else:
            self.canvas_preview.delete("all")

    def go(self):

        self.design = self.SVar_selected_design.get()
        self.window_width = self.slider_window_width.get()
        self.pieces_per_col = self.slider_pieces_per_col.get()
        self.pieces_per_row = self.slider_pieces_per_row.get()
        self.MainWindow.destroy()

    def run(self):
        self.MainWindow.mainloop()
