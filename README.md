# GestureX 

GestureX enables you to control your Linux PC using hand gestures. You can assign specific commands or functionalities to different hand gestures, allowing for hands-free interaction with your computer.

## Features

- Recognizes hand gestures using a webcam
- Maps hand gestures to custom commands or functionalities
- Real-time preview of webcam feed with hand gesture recognition
- Easily configurable through a graphical user interface

## Installation

1. Clone the repository (You can also clone this GitHub repo):

    ```bash
    git clone https://git.0x7f.in/sarthak/GestureX
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

1. Launch the application.
2. Define hand gestures and assign commands or functionalities to them through the graphical user interface.
3. Perform the defined hand gestures in front of your webcam to trigger the corresponding commands or functionalities.
4. (Optional) Import the `gestures_commands.json` file to get sample bindings to test the app.

## Supported Hand Gestures

- "Okay" gesture
- "Peace" sign
- Thumbs up
- Thumbs down
- "Call me" gesture
- Stop gesture
- Rock and roll sign
- Fist gesture
- Smile hand gesture
- "Live long" gesture

These are the default gestures supported by the model. I am working on adding your own custom gesture as well.

## Screenshots
![Main UI](screenshots/screenshot1.png)

## Credits

This project utilizes the hand gesture recognition model provided by the [Google MediaPipe project](https://github.com/google/mediapipe).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

