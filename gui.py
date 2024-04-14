import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import threading
import os

class_names = ['okay', 'peace', 'thumbs up', 'thumbs down', 'call me', 'stop', 'rock', 'live long', 'fist', 'smile']

gesture_commands = {
    'okay': 'true',
    'peace': 'true',
    'thumbs up': 'true',
    'thumbs down': 'true',
    'call me': 'true',
    'stop': 'true',
    'rock': 'true',
    'fist': 'true',
    'smile': 'true',
    'live long': 'true'
}

icons = {
    'okay': '👌',
    'peace': '✌️',
    'thumbs up': '👍',
    'thumbs down': '👎',
    'call me': '🤙',
    'stop': '✋',
    'rock': '🤟',
    'fist': '✊',
    'smile': '👉',
    'live long': '🖖'
}

class Main(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Label and Textbox Pairs")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_row_spacing(10)  # Set row spacing
        self.add(self.grid)

        self.text_entries = {}  # Dictionary to store text entry widgets

        for i, label in enumerate(class_names):
            label_widget = Gtk.Label(icons[label])
            textbox = Gtk.Entry()
            textbox.set_width_chars(50)
            self.grid.attach(label_widget, 0, i, 1, 1)
            self.grid.attach_next_to(textbox, label_widget, Gtk.PositionType.RIGHT, 1, 1)
            self.text_entries[label] = textbox

        # Add "Save" button
        button = Gtk.Button(label="Save")
        button.connect("clicked", self.on_button_clicked)
        self.grid.attach(button, 0, len(class_names), 2, 1)  # Attach button to the grid

        # Create a widget for displaying the video
        self.video_widget = Gtk.Image()
        self.grid.attach(self.video_widget, 3, 0, 1, len(class_names)+1)

        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.thread = threading.Thread(target=self.run_video_loop)
        self.thread.start()

    def run_video_loop(self):
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mp_draw = mp.solutions.drawing_utils

        model = load_model('mp_hand_gesture')

        while self.running:
            ret, frame = self.cap.read()

            if ret:
                x, y, _ = frame.shape
                frame = cv2.flip(frame, 1)
                framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(framergb)

                class_name = ''

                if result.multi_hand_landmarks:
                    landmarks = []
                    for handslms in result.multi_hand_landmarks:
                        for lm in handslms.landmark:
                            lmx = int(lm.x * x)
                            lmy = int(lm.y * y)
                            landmarks.append([lmx, lmy])

                        mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)

                        prediction = model.predict([landmarks])
                        class_id = np.argmax(prediction)
                        class_name = class_names[class_id]
                
                if class_name != '':
                    os.system(gesture_commands[class_name])
                
                # Add label on top of the video
                cv2.putText(frame, 'CV2 Preview', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, class_name, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Convert the frame to GTK-compatible format
                _, frame = cv2.imencode('.jpg', frame)
                frame = frame.tobytes()
                pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type('jpeg')
                pixbuf_loader.write(frame)
                pixbuf_loader.close()
                pixbuf = pixbuf_loader.get_pixbuf()

                GLib.idle_add(self.update_video_widget, pixbuf)

            else:
                break

    def update_video_widget(self, pixbuf):
        self.video_widget.set_from_pixbuf(pixbuf)
        return False

    def on_button_clicked(self, widget):
        for label, textbox in self.text_entries.items():
            command = textbox.get_text()
            if command.strip() != '':
                gesture_commands[label] = command
        print("Commands updated:", gesture_commands)

    def close_window(self, *args):
        self.running = False
        self.cap.release()
        Gtk.main_quit()

win = Main()
win.connect("destroy", win.close_window)
win.show_all()
Gtk.main()
