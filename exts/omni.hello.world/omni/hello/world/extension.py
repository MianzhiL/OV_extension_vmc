import omni.ext
import omni.ui as ui
from .udp_receiver import UDPReceiver
from .skeleton_mapper import SkeletonMapper
from .vmc_parser import parse_vmc_message


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
# def some_public_function(x: int):
#     print(f"[omni.hello.world] some_public_function was called with {x}")
#     return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.

class MyExtension:
    # def __init__(self):
    #     self._window = None

    def on_startup(self, ext_id):
        self._skeleton_mapper = SkeletonMapper()
        self._window = ui.Window("VMC Extension", width=400, height=300)
        with self._window.frame:
            self.build_ui()

    def build_ui(self):
        with ui.VStack():
            # IP Address Input
            ui.Label("Enter IP Address:")
            ip_field = ui.StringField()
            ip_field.model.add_value_changed_fn(lambda m: self.validate_ip(m.get_value_as_string()))

            # Port Input
            ui.Label("Enter Port:")
            port_field = ui.StringField()
            port_field.model.add_value_changed_fn(lambda m: self.validate_port(m.get_value_as_string()))

            # Skeleton Selection
            ui.Label("Select Skeleton Prim:")
            skeleton_combo = ui.ComboBox(0, *self.get_skeleton_prims(UsdGeom.Stage.Open("path_to_stage.usda")))
            skeleton_combo.model.add_value_changed_fn(lambda m: self.on_skeleton_selected(m.get_item_value_model().get_value_as_string()))

            self.start_button = ui.Button("Start Receiving", clicked_fn=self.start_receiving)
            self.stop_button = ui.Button("Stop Receiving", clicked_fn=self.stop_receiving)
            self.udp_receiver = None

            # Debug Button
            debug_button = ui.Button("Debug", clicked_fn=self.on_debug_clicked)

    # Helper functions for validation and skeleton retrieval
    def validate_ip(ip_text):
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(pattern, ip_text):
            print(f"Valid IP: {ip_text}")
        else:
            print("Invalid IP format")

    def validate_port(port_text):
        if port_text.isdigit() and 0 <= int(port_text) <= 65535:
            print(f"Valid Port: {port_text}")
        else:
            print("Invalid Port")

    def get_skeleton_prims(stage):
        return [prim.GetPath().pathString for prim in stage.Traverse() if prim.GetTypeName() == "Skeleton"]

    def on_skeleton_selected(selection):
        print(f"Selected Skeleton: {selection}")

    def on_debug_clicked():
        print("Debug Button Clicked")

    def on_shutdown(self):
        print("[omni.hello.world] MyExtension shutdown")
        if self.udp_receiver:
            self.udp_receiver.stop()

    def start_receiving(self):
        if not self.udp_receiver:
            self.udp_receiver = UDPReceiver(self.process_vmc_data)
            self.udp_receiver.start()
            self.label.text = "Receiving VMC data..."

    def stop_receiving(self):
        if self.udp_receiver:
            self.udp_receiver.stop()
            self.udp_receiver = None
            self.label.text = "Stopped receiving."

    def process_vmc_data(self, data):
        parsed_messages = parse_vmc_message(data)
        for msg in parsed_messages:
            print(msg)
        # self._skeleton_mapper.map_to_skeleton(root_position)

# if __name__ == "__main__":
#     plugin = MyExtension()
#     plugin.start_receiving()