"""
Puppy's entry point and single module.
"""

import tkinter

import importlib_metadata as ilr



def _create_window():

    window = tkinter.Tk()

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    w = screen_w // 6
    h = screen_h // 6                                                      
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
    window.minsize(w, h)

    meta = ilr.metadata(__package__)
    name = meta['name']
    version = meta['version']
    window.title(f'{name} {version}')

    return window


def _add_widgets(window):

    label = tkinter.Label(
        window,
        text='Minimal GUI app to test pup.',
        padx=32,
        pady=32,
    )
    label.pack()

    button = tkinter.Button(
        window,
        text='Quit',
        padx=32,
        pady=8,
        command=window.destroy,
    )
    button.pack()


def main():

    window = _create_window()
    _add_widgets(window)
    tkinter.mainloop()


if __name__ == '__main__':

    main()
