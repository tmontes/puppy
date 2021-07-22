"""
Puppy's entry point and single module.
"""

import os
import pprint
import sys
import tkinter
import tkinter.ttk
import tkinter.filedialog

import importlib_metadata as ilm
import importlib_resources as ilr
import serial
import serial.tools.list_ports



# The serial.Serial object we're connected to, if any.
_serial = None



def _create_window():

    window = tkinter.Tk()

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    w = (screen_w // 2) - 16
    h = (screen_h // 2) - 16
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
    window.minsize(w, h)

    meta = ilm.metadata(__package__)
    name = meta['name']
    version = meta['version']
    window.title(f'{name} {version}')

    return window



def _top_frame_widget(window):

    frame = tkinter.Frame()

    file_path = ilr.files(__package__) / 'logo.png'

    # Must keep reference to PhotoImage, otherwise it doesn't become visible
    _top_frame_widget.img = tkinter.PhotoImage(file=file_path)
    tkinter.Label(
        frame,
        image=_top_frame_widget.img,
    ).pack(
        side='left',
    )

    tkinter.Label(
        frame,
        text='Minimal GUI app to test pup.',
        justify='left',
    ).pack(
        side='left',
        padx=16,
    )

    return frame



def _bottom_frame_widget(window, log_lines):

    frame = tkinter.Frame()

    text_input = tkinter.Entry(frame)
    text_input.pack(side='left', fill='x', expand=True)
    text_input.bind('<Return>', lambda _: _write_to_serial(text_input, log_lines))
    text_input.focus()

    serial_select = tkinter.ttk.Combobox(
        frame,
        state='readonly',
    )
    serial_select.set('[select serial port]')
    serial_select.pack(side='left', padx=(10, 0))
    window.after(1000, lambda: _populate_serial_ports(window, serial_select, log_lines))

    load_button = tkinter.Button(frame, text='Load', padx=10, command=lambda: _load_file(log_lines))
    load_button.pack(side='left', padx=(10, 0))

    save_button = tkinter.Button(frame, text='Save', padx=10, command=lambda: _save_file(log_lines))
    save_button.pack(side='left')

    return frame


def _write_to_serial(text_input, log_lines):

    log = lambda s: log_lines([s])

    if not _serial:
        log('No serial port open.')
        return

    _serial.write(text_input.get().encode('utf8')+b'\r\n')
    text_input.delete(0, 'end')



def _populate_serial_ports(window, serial_select, log_lines):

    serial_devices = [
        port.device
        for port in serial.tools.list_ports.comports()
    ]
    serial_select['values'] = serial_devices
    log_lines([
        'Serial devices:',
        *map(lambda s: f'    {s!r}', serial_devices),
        '',
    ])

    serial_select.bind(
        '<<ComboboxSelected>>',
        lambda _: _select_serial_port(window, serial_select.get(), log_lines),
    )



def _select_serial_port(window, serial_device, log_lines):

    global _serial

    log = lambda s: log_lines([s])

    if _serial:
        log(f'Closing {_serial.name!r}.')
        _serial.close()
    log(f'Opening {serial_device!r}.')
    try:
        _serial = serial.Serial(serial_device, 115200, timeout=0.05)
    except Exception as exc:
        log(f'Failed: {exc}.')
        _serial = None
        return

    log(f'Opened {_serial.name!r}:')
    log('')
    _serial.write(b'\x02')
    window.after(100, lambda: _read_serial_port(window, log))


def _read_serial_port(window, log):

    if _serial:
        line = _serial.readline()
        if line:
            text_line = line.decode('utf8', errors='replace').rstrip('\r\n')
            log(f'| {text_line}')
    window.after(100, lambda: _read_serial_port(window, log))



def _load_file(log_lines):

    log = lambda s: log_lines([s])

    filename = tkinter.filedialog.askopenfilename()
    log(f'Opening {filename!r} in read mode...')
    try:
        with open(filename, 'rb') as f:
            log(f'Reading 128 bytes...')
            payload = f.read(128)
    except OSError as e:
        log(f'Failed: {e}.')
    else:
        log(f'Read {payload!r}.')
    finally:
        log('')


def _save_file(log_lines):

    log = lambda s: log_lines([s])

    filename = tkinter.filedialog.asksaveasfilename()
    log(f'Opening {filename!r} in write mode...')
    payload = b'puppy wrote this file!\n'
    try:
        with open(filename, 'wb') as f:
            log(f'Writing payload...')
            f.write(payload)
    except OSError as e:
        log(f'Failed: {e}.')
    else:
        log(f'Wrote {payload!r}.')
    finally:
        log('')


def _add_widgets(window):

    _top_frame_widget(window).pack(
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
    # log_widget.focus_set()
    log_widget.pack(side='top', fill='both', expand=True, padx=16)

    def log_lines(lines):
        log_widget.configure(state=tkinter.NORMAL)
        for line in lines:
            log_widget.insert('end', f'{line}\n')
        log_widget.yview('end')
        log_widget.configure(state=tkinter.DISABLED)
        window.update()

    _bottom_frame_widget(window, log_lines).pack(
        side='top',
        fill='x',
        padx=16,
        pady=16,
    )

    return log_lines


def main():

    window = _create_window()
    log_lines = _add_widgets(window)

    log_lines([
        'os.getcwd():',
        f'    {os.getcwd()!r}',
        '',
        'sys.path:',
        *map(lambda s: f'    {s!r}', sys.path),
        '',
    ])

    tkinter.mainloop()


if __name__ == '__main__':

    main()
