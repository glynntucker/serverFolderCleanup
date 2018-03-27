import os

import tkinter as tk
from tkinter import filedialog, ttk

from rename import rename_duplicates_in_tree, rename_dupes_in_directory


class DirectoryEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        self.run_button = kwargs.pop('run_button')
        super().__init__(*args, **kwargs)

        self.vcmd = self.register(self._validate)
        self['validate'] = 'all'
        self['validatecommand'] = self.vcmd, '%P',

    def _validate(self, value):
        if os.path.exists(value):
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)
        return True


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Rename Duplicate Names')

        self.directory_name = tk.StringVar(value=os.getcwd())

        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.button_run = ttk.Button(
            self.frame,
            text='Run',
            command=self.run_rename
        )

        self.entry_box = DirectoryEntry(
            self.frame,
            textvariable=self.directory_name,
            run_button=self.button_run
        )
        # need to validate path before running rename
        # self.entry_box.bind('<Return>', self.run_rename)
        self.button_browse = ttk.Button(self.frame, text='Browse', command=self.get_directory)

        self.sub_dirs_to_be_done = tk.BooleanVar(value=True)
        self.checkbutton_do_subdirectories = ttk.Checkbutton(
            self.frame,
            text="Check to deduplicate entries in subdirectories as well",
            variable=self.sub_dirs_to_be_done,
            onvalue=True,
            offvalue=False
        )

        self.entry_box.grid(row=0, column=0, sticky=(tk.E + tk.W))
        self.button_browse.grid(row=0, column=1, sticky=tk.E)
        self.checkbutton_do_subdirectories.grid(row=1, column=0, sticky=tk.W)
        self.button_run.grid(row=1, column=1, sticky=tk.E)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5, )

        for row in range(2):
            tk.Grid.rowconfigure(self.frame, row, weight=1)
        for column in range(2):
            tk.Grid.columnconfigure(self.frame, column, weight=1)

    def get_directory(self):
        directory_name = filedialog.askdirectory()
        if directory_name:
            self.directory_name.set(directory_name)
            self.button_run.config(state=tk.NORMAL)

    def run_rename(self):
        if self.sub_dirs_to_be_done:
            rename_duplicates_in_tree(self.directory_name)
        else:
            rename_dupes_in_directory(self.directory_name)


if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    root.mainloop()
