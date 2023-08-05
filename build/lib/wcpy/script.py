# -*- coding: utf-8 -*-


import os, sys, argparse

# PyQt5
from PyQt5 import QtWidgets

from .core import MainWindow


def run():
    """Run Wavelength Calibrator from command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', default=None, 
        help='Input file.'
    )
    parser.add_argument(
        '-f', '--format', default=None, choices=['ascii', 'ecsv', 'fits'], 
        help='Format of the input file (`ascii`, `ecsv`, or `fits`).'
    )
    parser.add_argument(
        '-r', '--reverse', action='store_true', default=False, 
        help='Reverse or not.'
    )
    parser.add_argument(
        '-l', '--linelist', default=None, 
        help='Line list.'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, 
        help='Debug mode or not.'
    )

    # UI
    app = QtWidgets.QApplication([])
    # Configuration (RNZ 07/20/2023):
    #   sys.argv can be passed to `QtWidgets.QApplication()`` instead of an empty list, 
    #   which allows configurations through built-in command-line arguments.
    app.setStyle('Windows')

    # Main window
    main_window = MainWindow()
    main_window.show()

    # Parse
    args = parser.parse_args()
    main_window.path_to_file = args.input
    main_window.file_format = args.format
    main_window.reverse = args.reverse
    main_window.path_to_line_list = args.linelist
    main_window.debug = args.debug

    # Load spectrum if ``path_to_file`` and ``file_format`` is provided
    if main_window.path_to_file is not None:

        main_window.path_to_file = os.path.abspath(main_window.path_to_file)

        if main_window.file_format is not None:

            main_window._loadSpectrum()

    # Load line list if ``path_to_line_list`` is provided
    if main_window.path_to_line_list is not None:

        main_window.path_to_line_list = os.path.abspath(main_window.path_to_line_list)

        main_window._loadLineList()

    sys.exit(app.exec_())


if __name__ == '__main__':

    run()