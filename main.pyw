
import sys

from PyQt5.QtWidgets import QApplication

import hyundai_progress



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = hyundai_progress.HyundaiProgress()
    main_window.show()
    sys.exit(app.exec_())