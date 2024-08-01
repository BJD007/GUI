# Alert-System

## What the GUI Application Does:
The GUI application is a "Port Crane Radar Alert System" designed to monitor and visualize radar data around a port crane. It simulates or receives real radar data, processes this data to detect potential obstacles or objects, and provides visual and auditory alerts if any objects are detected within a critical distance. The application also allows for manual control of the crane's position and arm angle, and it provides a detailed visualization of the port area, including storage tanks and vessels.

## Features of the GUI Application:
- Radar Visualization:
    - Displays radar positions and detections on a canvas.
    - Simulates radar data or uses real radar data input.
    - Visualizes the port area, storage tanks, and vessels.
- Crane Control:
    - Allows manual adjustment of the crane's position (X and Y coordinates) and arm angle using sliders.
    - Visualizes the crane's current position and arm orientation.
- Zoom Functionality:
    - Provides a zoom slider to adjust the zoom level of the visualization.
- Data Source Selection:
    - Allows switching between simulated data and real radar data using a combo box.
- Update Rate Control:
    - Allows adjustment of the update rate (in milliseconds) for data processing and visualization.
- Collision Detection:
    - Implements a sophisticated collision detection algorithm using KDTree for efficient proximity checks.
    - Provides visual alerts if objects are detected within a critical distance (50 units) or a warning distance (100 units).
- Auditory Alerts:
    - Plays a sound alert ("alert.wav") for critical warnings.
- Logging:
    - Logs all alerts to a file ("radar_alerts.log") with timestamps.
- Control Panel:
    - Offers a control panel with sliders, combo boxes, and spin boxes for adjusting various parameters and settings.

## Code Explanation:
- Initialization:
    The RadarAlert class initializes the GUI components and sets up the radar data, crane position, and timer for periodic updates.
- UI Setup:
    The initUI method sets up the main window, radar visualization canvas, alert label, and control panel with various controls.
- Data Update:
    The update_data method updates the radar data (either simulated or real) and checks for alerts.
- Simulated and Real Data:
    The simulate_radar_data method generates random radar detections.
    The get_real_radar_data method is a placeholder for real radar data input.
- Collision Detection:
    The check_alerts method processes radar detections, checks for potential collisions using KDTree, and updates the alert label and logs.
- Crane Control:
    Methods update_crane_position, update_crane_angle, and update_zoom update the crane's position, arm angle, and zoom level based on user input.
- Radar Visualization:
    The RadarCanvas class handles the drawing of the port area, storage tanks, vessel, radar positions, crane, and radar detections.

Created on 2023-04-01