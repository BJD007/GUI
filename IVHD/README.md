# IVHD

The Graphical User Interface (GUI) application represents a Radar Person Detection System. This system is designed to simulate or utilize real radar data to detect people in a specific environment. The GUI provides a visual representation of the radar data and generates alerts for potential safety hazards.

## Breakdown of the functionalities and features of the system:

Components:
- Radar Visualization: This section displays a graphical representation of the environment, including passageway boundaries, radars, and detected persons.
- Alert Label: This label displays critical or warning messages when people are detected within a certain distance of the car. The background color of the label changes to red to indicate a critical alert.
- Control Panel: This panel allows users to control various aspects of the simulation or real-data processing:
- Car Position Sliders: Users can adjust the X and Y coordinates of the car on the screen.
- Car Size Sliders: Users can modify the width and height of the car icon.
- Zoom Slider: This slider allows users to zoom in or out of the radar visualization.
- Data Source Combo Box: This combo box lets users choose between simulated data or real radar data (if available).
- Update Rate Spin Box: This box controls the update interval for the radar data visualization and alerts.

Functionalities:

- Data Simulation: The system can simulate radar data by generating random detections within a specified range around the radars.
- Real Data Support (if available): The system can potentially be configured to work with real radar data input. (The provided code includes a placeholder function for this)
- Person Detection: The system processes the radar data (simulated or real) to identify potential locations of people.
- Alert Generation: The system generates critical or warning alerts based on the proximity of detected people to the car. Critical alerts are triggered when a person is very close to the car, while warnings are issued for people within a larger radius.
- Logging: The system logs critical alerts to a file for record-keeping purposes.
- Sound Alerts: The system can play an audible sound to notify the user of critical alerts.


## To use this application:
- Install PyQt5 if you haven't already: pip install PyQt5
- Run the script.




Created on 2024-03-10