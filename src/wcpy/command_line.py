# -*- coding: utf-8 -*-
import os, sys, argparse, warnings

# PyQt5
from PyQt5 import QtWidgets

from .mainwindow import MainWindow
    
def main():
    """Command line tool."""
    
    # UI
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')
    # Setup
    main_window = MainWindow()
    # Show
    main_window.show()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', '--name', default=None, 
        help='Name of the input file'
    )
    parser.add_argument(
        '-f', '--format', default=None, 
        help='Format of the input file (`ascii`, `ecsv`, or `fits`).'
    )
    parser.add_argument(
        '-r', '--reverse', action='store_true', default=False, 
        help='Reverse or not.'
    )

    # Parse
    args = parser.parse_args()
    main_window.file_name = args.name
    main_window.file_format = args.format
    main_window.reverse = args.reverse

    # warnings.filterwarnings('error')

    # Load spectrum if ``name`` and ``format`` is provided
    if main_window.file_name is not None:

        main_window.file_name = os.path.abspath(main_window.file_name)

        if main_window.file_format is not None:

            main_window.load(external=True)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()