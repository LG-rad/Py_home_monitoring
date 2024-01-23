# FTP Data Analysis Script

## Overview

This Python script connects to an FTP server, retrieves a CSV file, and performs data analysis on the downloaded dataset. The analysis includes calculating the number of cycles, total operational time, average cycle duration, and generating a bar chart showing the average activity per hour.

## Requirements

- Python 3.x
- pandas
- matplotlib
- ftplib

## Setup

1. Clone the repository:

```
git clone https://github.com/LG-rad/Py_home_monitoring.git

cd Py_home_monitoring
```

1. Install the required dependencies:

```
pip install pandas matplotlib
```

3. Update FTP and file information:

Open `lib/info.py` and replace the placeholder values in the `infos` dictionary with your actual FTP server details and file information.

## Usage

Run the script by executing the following command:

```
python main.py
```

The script will download the CSV file from the FTP server, perform the analysis, and display the results in the console. Additionally, a bar chart will be generated and displayed.

## Example Results
```
- Number of cycles: 1000
- Total operational time: 172:12:36
- Average cycle duration: 00:04:36
```

## Visualization

The bar chart displays the average activity per hour. Each bar represents an hour, and the height of the bar indicates the average number of cycles during that hour.

[Include a link or path to your generated chart image]

## Notes

- [Any additional information or notes about the script]

Feel free to reach out if you have any questions or encounter issues.
