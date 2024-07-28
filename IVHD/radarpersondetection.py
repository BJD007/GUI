import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer

class RadarPersonDetection(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Simulate radar data
        self.radar_data = [[] for _ in range(2)]  # Two radars on the sides
        self.car_position = [400, 300]  # [x, y]
        self.car_size = [200, 100]  # [width, height]
        
        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every 1 second

    def initUI(self):
        self.setWindowTitle('Radar Person Detection System')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.canvas = RadarCanvas(self)
        layout.addWidget(self.canvas)

        self.alert_label = QLabel('No persons detected')
        self.alert_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.alert_label)

    def update_data(self):
        # Simulate radar detections
        for i in range(2):
            self.radar_data[i] = []
            if random.random() < 0.5:  # 50% chance of detection
                num_persons = random.randint(0, 3)
                for _ in range(num_persons):
                    distance = random.uniform(50, 150)
                    angle = random.uniform(-30, 30)
                    self.radar_data[i].append((distance, angle))

        self.check_alerts()
        self.canvas.update()

    def check_alerts(self):
        alerts = []
        for i, detections in enumerate(self.radar_data):
            for distance, angle in detections:
                if distance < 150:  # Alert if object is within 150 units
                    alerts.append(f"Radar {i+1}: Person detected at {distance:.1f} units, {angle:.1f} degrees")

        if alerts:
            self.alert_label.setText("\n".join(alerts))
            self.alert_label.setStyleSheet("background-color: red; color: white;")
        else:
            self.alert_label.setText("No persons detected")
            self.alert_label.setStyleSheet("")

class RadarCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw radar positions
        radar_positions = [
            (100, 300), (700, 300)  # Two radars on the sides
        ]
        for x, y in radar_positions:
            painter.setPen(QPen(Qt.blue, 2))
            painter.drawEllipse(x-5, y-5, 10, 10)

        # Draw car
        painter.setPen(QPen(Qt.black, 2))
        car_x, car_y = self.parent.car_position
        car_width, car_height = self.parent.car_size
        painter.drawRect(car_x - car_width // 2, car_y - car_height // 2, car_width, car_height)

        # Draw radar detections
        painter.setPen(QPen(Qt.red, 2))
        for i, detections in enumerate(self.parent.radar_data):
            radar_x, radar_y = radar_positions[i]
            for distance, angle in detections:
                x = radar_x + distance * math.cos(math.radians(angle))
                y = radar_y + distance * math.sin(math.radians(angle))
                painter.drawLine(radar_x, radar_y, x, y)
                painter.drawEllipse(x-5, y-5, 10, 10)  # Draw detected persons as circles

def main():
    app = QApplication(sys.argv)
    ex = RadarPersonDetection()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
