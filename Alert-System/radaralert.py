import sys
import random
import math
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSlider, QComboBox, QGroupBox, QFormLayout, QSpinBox)
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtMultimedia import QSound
import numpy as np
from sklearn.neighbors import KDTree

class RadarAlert(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.radar_data = [[] for _ in range(7)]
        self.crane_position = [400, 300]
        self.crane_arm_length = 200
        self.crane_arm_angle = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        self.zoom_level = 1.0
        self.use_real_data = False

        # Setup logging
        logging.basicConfig(filename='radar_alerts.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s')

        # Load sound for critical alerts
        self.alert_sound = QSound("alert.wav")

    def initUI(self):
        self.setWindowTitle('Port Crane Radar Alert System')
        self.setGeometry(100, 100, 1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Radar visualization
        viz_layout = QVBoxLayout()
        self.canvas = RadarCanvas(self)
        viz_layout.addWidget(self.canvas)

        self.alert_label = QLabel('No alerts')
        self.alert_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(self.alert_label)

        main_layout.addLayout(viz_layout)

        # Control panel
        control_panel = QGroupBox("Control Panel")
        control_layout = QFormLayout()

        self.crane_x_slider = QSlider(Qt.Horizontal)
        self.crane_x_slider.setRange(0, 800)
        self.crane_x_slider.setValue(400)
        self.crane_x_slider.valueChanged.connect(self.update_crane_position)
        control_layout.addRow("Crane X:", self.crane_x_slider)

        self.crane_y_slider = QSlider(Qt.Horizontal)
        self.crane_y_slider.setRange(0, 600)
        self.crane_y_slider.setValue(300)
        self.crane_y_slider.valueChanged.connect(self.update_crane_position)
        control_layout.addRow("Crane Y:", self.crane_y_slider)

        self.crane_angle_slider = QSlider(Qt.Horizontal)
        self.crane_angle_slider.setRange(0, 359)
        self.crane_angle_slider.valueChanged.connect(self.update_crane_angle)
        control_layout.addRow("Crane Angle:", self.crane_angle_slider)

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(10, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        control_layout.addRow("Zoom:", self.zoom_slider)

        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems(["Simulated Data", "Real Data"])
        self.data_source_combo.currentIndexChanged.connect(self.toggle_data_source)
        control_layout.addRow("Data Source:", self.data_source_combo)

        self.update_rate_spin = QSpinBox()
        self.update_rate_spin.setRange(100, 5000)
        self.update_rate_spin.setValue(1000)
        self.update_rate_spin.setSingleStep(100)
        self.update_rate_spin.valueChanged.connect(self.update_timer_interval)
        control_layout.addRow("Update Rate (ms):", self.update_rate_spin)

        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel)

    def update_data(self):
        if self.use_real_data:
            self.radar_data = self.get_real_radar_data()
        else:
            self.simulate_radar_data()

        self.check_alerts()
        self.canvas.update()

    def simulate_radar_data(self):
        for i in range(7):
            self.radar_data[i] = []
            if random.random() < 0.3:
                distance = random.uniform(50, 300)
                angle = random.uniform(0, 360)
                self.radar_data[i].append((distance, angle))

    def get_real_radar_data(self):
        # Placeholder for real radar data input
        # Replace this with your actual implementation
        return [[] for _ in range(7)]

    def check_alerts(self):
        alerts = []
        critical_alert = False
        all_detections = []

        for i, detections in enumerate(self.radar_data):
            for distance, angle in detections:
                x = distance * math.cos(math.radians(angle))
                y = distance * math.sin(math.radians(angle))
                all_detections.append((x, y, distance, angle, i))

        if all_detections:
            tree = KDTree(np.array(all_detections)[:, :2])
            for x, y, distance, angle, radar_id in all_detections:
                indices = tree.query_radius([[x, y]], r=50)[0]
                if len(indices) > 1:
                    alerts.append(f"CRITICAL: Radar {radar_id+1}: Object at {distance:.1f} units, {angle:.1f} degrees")
                    critical_alert = True
                elif distance < 100:
                    alerts.append(f"WARNING: Radar {radar_id+1}: Object at {distance:.1f} units, {angle:.1f} degrees")

        if alerts:
            alert_text = "\n".join(alerts)
            self.alert_label.setText(alert_text)
            self.alert_label.setStyleSheet("background-color: red; color: white;")
            logging.warning(alert_text)
            if critical_alert:
                self.alert_sound.play()
        else:
            self.alert_label.setText("No alerts")
            self.alert_label.setStyleSheet("")

    def update_crane_position(self):
        self.crane_position = [self.crane_x_slider.value(), self.crane_y_slider.value()]
        self.canvas.update()

    def update_crane_angle(self, value):
        self.crane_arm_angle = value
        self.canvas.update()

    def update_zoom(self, value):
        self.zoom_level = value / 100.0
        self.canvas.update()

    def toggle_data_source(self, index):
        self.use_real_data = (index == 1)

    def update_timer_interval(self, value):
        self.timer.setInterval(value)

class RadarCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Apply zoom
        painter.scale(self.parent.zoom_level, self.parent.zoom_level)

        # Draw port area (simplified)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(50, 50, 700, 500)

        # Draw storage tanks (simplified)
        tank_positions = [(200, 200), (400, 200), (600, 200)]
        for x, y in tank_positions:
            painter.setBrush(QBrush(QColor(150, 150, 150)))
            painter.drawEllipse(x-30, y-30, 60, 60)

        # Draw vessel (simplified)
        painter.setBrush(QBrush(QColor(150, 150, 150)))
        painter.drawRect(100, 400, 300, 100)

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
