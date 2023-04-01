import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer

class RadarAlert(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Simulate radar data
        self.radar_data = [[] for _ in range(7)]
        self.crane_position = [400, 300]  # [x, y]
        self.crane_arm_length = 200
        self.crane_arm_angle = 0  # degrees
        
        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every 1 second

    def initUI(self):
        self.setWindowTitle('Port Crane Radar Alert System')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.canvas = RadarCanvas(self)
        layout.addWidget(self.canvas)

        self.alert_label = QLabel('No alerts')
        self.alert_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.alert_label)

    def update_data(self):
        # Simulate radar detections
        for i in range(7):
            self.radar_data[i] = []
            if random.random() < 0.3:  # 30% chance of detection
                distance = random.uniform(50, 300)
                angle = random.uniform(0, 360)
                self.radar_data[i].append((distance, angle))

        # Simulate crane movement
        self.crane_arm_angle = (self.crane_arm_angle + 5) % 360

        self.check_alerts()
        self.canvas.update()

    def check_alerts(self):
        alerts = []
        for i, detections in enumerate(self.radar_data):
            for distance, angle in detections:
                if distance < 100:  # Alert if object is within 100 units
                    alerts.append(f"Radar {i+1}: Object detected at {distance:.1f} units, {angle:.1f} degrees")

        if alerts:
            self.alert_label.setText("\n".join(alerts))
            self.alert_label.setStyleSheet("background-color: red; color: white;")
        else:
            self.alert_label.setText("No alerts")
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
            (100, 100), (700, 100), (400, 300),
            (100, 500), (700, 500), (250, 300), (550, 300)
        ]
        for x, y in radar_positions:
            painter.setPen(QPen(Qt.blue, 2))
            painter.drawEllipse(x-5, y-5, 10, 10)

        # Draw crane
        painter.setPen(QPen(Qt.black, 2))
        x, y = self.parent.crane_position
        painter.drawLine(x, y, 
                         x + self.parent.crane_arm_length * math.cos(math.radians(self.parent.crane_arm_angle)),
                         y + self.parent.crane_arm_length * math.sin(math.radians(self.parent.crane_arm_angle)))

        # Draw radar detections
        painter.setPen(QPen(Qt.red, 2))
        for i, detections in enumerate(self.parent.radar_data):
            radar_x, radar_y = radar_positions[i]
            for distance, angle in detections:
                x = radar_x + distance * math.cos(math.radians(angle))
                y = radar_y + distance * math.sin(math.radians(angle))
                painter.drawLine(radar_x, radar_y, x, y)

def main():
    app = QApplication(sys.argv)
    ex = RadarAlert()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
% Main function
