"""
Puppy's entry point and single module.
"""

import os
import pprint
import sys
import tkinter

import importlib_metadata as ilm
import importlib_resources as ilr



def _create_window():

    window = tkinter.Tk()

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    w = screen_w // 3
    h = screen_h // 3
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
    window.minsize(w, h)

    meta = ilm.metadata(__package__)
    name = meta['name']
    version = meta['version']
    window.title(f'{name} {version}')

    return window


def _add_widgets(window):

    top_frame = tkinter.Frame()

    file_path = ilr.files(__package__) / 'logo.png'

    # Must keep reference to PhotoImage, otherwise it doesn't become visible
    _add_widgets.img = tkinter.PhotoImage(file=file_path)
    tkinter.Label(
        top_frame,
        image=_add_widgets.img,
    ).pack(
        side='left',
    )

    tkinter.Label(
        top_frame,
        text='Minimal GUI app to test pup.',
        justify=tkinter.LEFT,
    ).pack(
        side='left',
        padx=16,
    )

    top_frame.pack(
        side='top',
        fill='x',
        padx=16,
        pady=16,
    )

    log_widget = tkinter.Text(
        window,
        highlightthickness=1,
        highlightcolor='lightgray',
        state=tkinter.DISABLED,
        wrap='none',
        height=1,
        padx=8,
        pady=8,
    )
    log_widget.focus_set()
    log_widget.pack(side='top', fill='both', expand=True, padx=16)

    tkinter.Button(
        window,
        text='Quit',
        pady=8,
        command=window.destroy,
    ).pack(
        side='bottom',
        fill='both',
        padx=16,
        pady=16,
    )

    return log_widget


def _log_lines(window, log_widget, lines):

    log_widget.configure(state=tkinter.NORMAL)
    for line in lines:
        log_widget.insert('end', f'{line}\n')
    log_widget.yview('end')
    log_widget.configure(state=tkinter.DISABLED)

    window.update()


def main():

    window = _create_window()
    log_widget = _add_widgets(window)

    log_lines = lambda l: _log_lines(window, log_widget, l)

    log_lines([
        'os.getcwd():',
        f'    {os.getcwd()!r}',
        '',
        'sys.path:',
        *map(lambda s: f'    {s!r}', sys.path),
    ])

    tkinter.mainloop()


if __name__ == '__main__':

    main()
