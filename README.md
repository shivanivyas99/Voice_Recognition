
# Voice Recognition Project

## Overview
This project is a voice recognition system designed to perform a series of operations based on voice input. It utilizes Python for processing and analyzing spoken commands. This is supposed to be a part of the Drone Response Project.

## Installation

To run this project, you will need to install certain Python libraries. You can install these dependencies using pip:

```bash
pip3 install -r requirements.txt
```

## Usage

To start the voice recognition system, run the following command in your terminal:

```bash
python3 main.py
```

## Functions in main.py

### `init()`
This function initializes the system's settings and configurations. It's called at the beginning to set up any necessary parameters or configurations.

### `request_current_status()`
After initialization, this function is called to request the current status of the system. It might check system readiness or other initial status indicators.

### `communication()`
The core function of the project, `communication()` is responsible for capturing and recognizing audio inputs from the user. It processes spoken commands and converts them to a format that the system can understand and act upon.

### `display()`
This function is called at the end of the program. It is responsible for displaying results, providing outputs, or asking the user if they want to see the recognized text from their spoken commands.
