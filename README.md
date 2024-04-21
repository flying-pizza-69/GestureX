# GestureX 

## Table of Contents

- [GestureX](#gesturex)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Supported Hand Gestures](#supported-hand-gestures)
  - [Credits](#credits)
  - [License](#license)

## Description

GestureX is a Python application that recognizes hand gestures using a webcam and maps them to custom commands making the interaction with your computer more intuitive, fun and inclusive. The application provides a real-time preview of the webcam feed with hand gesture recognition. It is easily configurable through a graphical user interface and supports multiple camera sources.

![](./screenshots/screenshot1.png)

## Features

- Hand gesture recognition: The application recognizes hand gestures using a webcam;
- Real time preview: The application provides a real-time preview of the webcam feed with hand gesture recognition;
- Multiple camera sources: The application supports multiple camera sources;
- Easily configurable: The application is easily configurable through a graphical user interface.

## Installation

1. Clone the repository (Pick your favorite mirror):

    ```bash
    git clone https://git.0x7f.in/sarthak/GestureX
    ```

    ```bash
    git clone https://github.com/flying-pizza-69/GestureX.git
    ```

2. Create and activate Virtual Environment
    
    ```
    cd GestureX
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required dependencies:

    ```bash
    (venv) pip install -r requirements.txt
    ```

3. Install the required fonts to display emojis

- Arch Linux
    ```bash
    pacman -S noto-fonts-emoji
    ```
- Ubuntu or Debian
    ```bash
    apt-get install fonts-noto-color-emoji
    ```
- Fedora or RHEL Based
    ```bash
    dnf install google-noto-emoji-fonts
    ```
- openSUSE
    ```bash
    zypper install google-noto-emoji-fonts
    ```

4. Run the application:

    ```bash
    python3 gui.py
    ```

## Usage

1. Start the application by running the `gui.py` script;
2. Set the camera source and the desired hand gesture commands in the graphical user interface;
3. Perform the hand gestures in front of the webcam to trigger the mapped commands and interact with your computer;
4. (Optional) Import the `gestures_commands.json` file to get sample bindings to test the app.

## Supported Hand Gestures

| Hand Gesture Name | Gesture |
|-------------------|---------|
| Okay              | 👌      |
| Peace             | ✌️      |
| Thumbs Up         | 👍      |
| Thumbs Down       | 👎      |
| Call Me           | 🤙      |
| Stop              | ✋      |
| Rock and Roll     | 🤘      |
| Fist Bump         | 👊      |
| Smile Hand        | 👉      |
| Live Long         | 🖖      |

These are the default gestures recognized by the model I am currently using. I am also working on the possibility of adding your custom gestures and on the support for dynamic gestures. If you have any suggestions or want to contribute to the project, feel free to open an issue or submit a pull request.

## Credits

This project utilizes the following libraries:

- [OpenCV](https://opencv.org/) for the webcam feed and image processing;
- [Google MediaPipe project](https://github.com/google/mediapipe) for the hand gesture recognition model;
- [Gtk](https://www.gtk.org/) for the graphical user interface;

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

