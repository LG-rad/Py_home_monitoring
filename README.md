# Dash FTP Data Visualization App

This Dash web application connects to an FTP server, retrieves CSV data, and visualizes the data in graphs.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-dash-app.git
   cd your-dash-app
   ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the following command to start the Dash web application:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:8050/` by default.

## Dependencies

- Dash
- Dash DAQ
- Pandas
- Other dependencies mentioned in `requirements.txt`

## File Structure

- `app.py`: Main application file containing the Dash app and callbacks.
- `common/ftp.py`: Module for FTP connection functionality.
- `infos.py`: Module containing information about sensors.
- `requirements.txt`: List of Python dependencies.

## Configuration

- Update FTP server, username, and password in the FTP connection window of the app.
- Customize sensor information in the `infos.py` file.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.