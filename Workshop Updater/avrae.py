from tkinter import font
from frames import *
class MainWindow(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(self.CenterWindowtoDisplay(width, height))
        self.maxsize(width, height)
        self.minsize(width, height)
        self.title("Avrae Update Pusher")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.collection = getCollection()
        # self.defaultFont.config(size=12)

        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        for F in [SettingsMenu, GVAR, QuickMenu, SnippetSelect, AliasSelect]:
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        if not os.environ.get('AVRAE_TOKEN'):
            messagebox.showerror(title="Missing Secret", message="Missing AVRAE_TOKEN")
            self.destroy()
        elif len(self.collection) > 0:
            self.show_frame('QuickMenu')
        else:
            self.show_frame("SettingsMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.is_topmost = True
        frame.tkraise()


    def CenterWindowtoDisplay(self, width, height):
        # Centers the window to the main display/monitor
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 1.5))
        return f"{width}x{height}+{x}+{y}"


if __name__ == "__main__":
    app = MainWindow(500, 200)
    app.mainloop()