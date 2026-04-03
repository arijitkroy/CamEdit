# CamEdit

CamEdit is a professional Python middleware application designed to enhance live camera feeds through real-time processing and artificial intelligence filters. The application streams the modified video to a virtual driver, enabling its use in various video conferencing platforms such as Zoom, Microsoft Teams, and Discord.

## Core Features

- **Virtual Camera Integration**: Seamlessly broadcast enhanced video to external applications.
- **Auto Face Focus**: Intelligently crops and scales the camera feed to maintain subject centering and zoom, featuring adjustable sensitivity and zoom level.
- **AI Eye Contact**: Real-time gaze redirection utilizing iris tracking and spatial warping to maintain eye contact with the lens.
- **Professional Color Suite**: Detailed control over Brightness, Contrast, and Saturation settings.
- **Image Sharpening**: Dedicated sharpening filters utilizing a custom matrix to enhance edges and output clarity.
- **Dynamic Configuration**: On-the-fly adjustment of camera resolution, target frame rates, and filter parameters.

## System Requirements

### 1. Virtual Camera Driver
The "Virtual Camera" functionality requires a virtual camera driver to be installed on the host system.

- **Recommended**: Download and install [OBS Studio](https://obsproject.com/).
- Upon installation, the "OBS Virtual Camera" device becomes globally available. This application utilizes that driver for its output stream.

### 2. Python Environment
- Python 3.10 or higher.
- All requisite libraries are documented in `requirements.txt`.

## Installation and Execution

### Standalone Executable (Recommended)
1. Download the `CamEdit_Release.zip` from the Releases page.
2. Extract the archive to a local directory.
3. Execute `CamEdit.exe` to launch the application without requiring a Python environment.

### Source Installation
1. Clone or download the repository.
2. Open a terminal within the project directory.
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Launch the primary interface:
   ```powershell
   python main.py
   ```

## Operations Manual

1.  **Camera Selection**: Select the physical camera device from the top navigation dropdown.
2.  **Quality Settings**: Define the capture resolution and target output frame rate.
3.  **Enhancement Modules**:
    - **Auto Face Focus**: Toggle the module and utilize the Zoom Level slider for framing.
    - **Eye Contact Mode**: Enable the module and adjust Correction Intensity for gaze redirection.
        Sliding controls for settings such as zoom scale and effect sensitivity remain hidden to reduce UI clutter until their primary filter is activated.
    - **Image Sharpening**: Activate the module to apply edge enhancements and dial in the desired sharpening strength.
4.  **Broadcast**: Select "Enable Virtual Cam". In the target conferencing application, select "OBS Virtual Camera" as the video source.

## Technical Considerations

- **Hardware Performance**: Utilizing multiple AI filters and high resolutions simultaneously increases CPU utilization. For optimal performance, consider reducing the target frame rate or disabling secondary filters.
- **Processing Logic**: The Eye Contact feature employs spatial warping. For natural results, maintaining the intensity slider between 0.3 and 0.6 is recommended.

## License
MIT