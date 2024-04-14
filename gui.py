import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import threading
import os
import json

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
        Gtk.Window.__init__(self, title="GestureX")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_row_spacing(10)
        self.add(self.grid)

        # Add title for command binding section
        command_title_label = Gtk.Label()
        command_title_label.set_markup('<span size="larger" weight="bold">Command Binding</span>')
        self.grid.attach(command_title_label, 0, 0, 2, 1)

        self.text_entries = {}

        for i, label in enumerate(class_names):
            label_widget = Gtk.Label()
            label_widget.set_markup('<span size="xx-large">' + icons[label] + '</span>')
            textbox = Gtk.Entry()
            textbox.set_width_chars(30)
            self.grid.attach(label_widget, 0, i+1, 1, 1)
            self.grid.attach_next_to(textbox, label_widget, Gtk.PositionType.RIGHT, 1, 1)
            self.text_entries[label] = textbox

        # Create a separate row for buttons
        button_row = Gtk.Grid()
        button_row.set_column_spacing(6)
        self.grid.attach(button_row, 0, len(class_names)+2, 2, 1)

        # Add "Save" button
        save_btn = Gtk.Button(label="Save")
        save_btn.set_hexpand(True)
        button_row.attach(save_btn, 0, 0, 1, 1)
        save_btn.connect("clicked", self.on_save_clicked)

        # Add "Export" button
        export_btn = Gtk.Button(label="Export")
        export_btn.set_hexpand(True)
        button_row.attach_next_to(export_btn, save_btn, Gtk.PositionType.RIGHT, 1, 1)
        export_btn.connect("clicked", self.on_export_clicked)

        # Add "Import" button
        import_btn = Gtk.Button(label="Import")
        import_btn.set_hexpand(True)
        button_row.attach_next_to(import_btn, export_btn, Gtk.PositionType.RIGHT, 1, 1)
        import_btn.connect("clicked", self.on_import_clicked)

        # Create a separator between command binding section and CV2 preview
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        separator.set_size_request(2, -1)
        separator.set_margin_top(10)

        self.grid.set_column_spacing(20)
        self.grid.attach(separator, 2, 0, 1, len(class_names) + 2)

        # Add title for CV2 preview section
        preview_title_label = Gtk.Label()
        preview_title_label.set_markup('<span size="large" weight="bold">Preview</span>')
        self.grid.attach(preview_title_label, 3, 0, 1, 1)

        # Create a widget for displaying the video
        self.video_widget = Gtk.Image()
        self.grid.attach(self.video_widget, 3, 1, 1, len(class_names)+1)

        # Create a separate row for toggle buttons
        toggle_button_row = Gtk.Grid()
        toggle_button_row.set_column_spacing(6)
        self.grid.attach(toggle_button_row, 3, len(class_names)+2, 1, 1)

        # Add buttons below the CV2 preview
        self.preview_button = Gtk.ToggleButton(label="Toggle Preview")
        self.preview_button.set_hexpand(True)
        self.trace_button = Gtk.ToggleButton(label="Toggle Traces")
        self.trace_button.set_hexpand(True)
        self.class_button = Gtk.ToggleButton(label="Toggle Label")
        self.class_button.set_hexpand(True)
        
        # Add button signals
        self.preview_button.connect("toggled", self.toggle_video_preview)
        self.trace_button.connect("toggled", self.toggle_hand_traces)
        self.class_button.connect("toggled", self.toggle_class_text)
        
        # Add buttons to the toggle button row
        toggle_button_row.attach(self.preview_button, 0, 0, 1, 1)
        toggle_button_row.attach_next_to(self.trace_button, self.preview_button, Gtk.PositionType.RIGHT, 1, 1)
        toggle_button_row.attach_next_to(self.class_button, self.trace_button, Gtk.PositionType.RIGHT, 1, 1)

        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.preview_enabled = False
        self.hand_trace_enabled = False
        self.class_text_enabled = False
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

                        if self.hand_trace_enabled:
                            mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)

                        prediction = model.predict([landmarks])
                        class_id = np.argmax(prediction)
                        class_name = class_names[class_id]
                
                if class_name != '':
                    os.system(gesture_commands[class_name])
                
                # Add label on top of the video
                if self.class_text_enabled:
                    cv2.putText(frame, class_name, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                if self.preview_enabled:
                    # Resize the frame
                    frame = cv2.resize(frame, (400, 300))

                    # Convert the frame to GTK-compatible format
                    _, frame = cv2.imencode('.jpg', frame)
                    frame = frame.tobytes()
                    pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type('jpeg')
                    pixbuf_loader.write(frame)
                    pixbuf_loader.close()
                    pixbuf = pixbuf_loader.get_pixbuf()

                    GLib.idle_add(self.update_video_widget, pixbuf)
                else:
                    # Create a black frame with "Preview disabled" text
                    frame = np.zeros((300, 400, 3), dtype=np.uint8)
                    text = "Preview disabled"
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                    text_x = (frame.shape[1] - text_size[0]) // 2
                    text_y = (frame.shape[0] + text_size[1]) // 2
                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

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

    def on_save_clicked(self, widget):
        for label, textbox in self.text_entries.items():
            command = textbox.get_text()
            if command.strip() != '':
                gesture_commands[label] = command
        print("Commands updated:", gesture_commands)

    def on_export_clicked(self, widget):
        filename = "gesture_commands.json"
        with open(filename, 'w') as f:
            json.dump(gesture_commands, f)
        print(f"Gesture commands exported to {filename}")

    def on_import_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a JSON file", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            with open(filename, 'r') as f:
                data = json.load(f)
                for label, command in data.items():
                    self.text_entries[label].set_text(command)
            print(f"Gesture commands imported from {filename}")
        elif response == Gtk.ResponseType.CANCEL:
            print("Import operation cancelled")

        dialog.destroy()

    def close_window(self, *args):
        self.running = False
        self.cap.release()
        Gtk.main_quit()

    def toggle_video_preview(self, button):
        if button.get_active():
            self.preview_enabled = True
        else:
            self.preview_enabled = False

    def toggle_hand_traces(self, button):
        if button.get_active():
            self.hand_trace_enabled = True
        else:
            self.hand_trace_enabled = False

    def toggle_class_text(self, button):
        if button.get_active():
            self.class_text_enabled = True
        else:
            self.class_text_enabled = False

win = Main()
win.connect("destroy", win.close_window)
win.show_all()
Gtk.main()
