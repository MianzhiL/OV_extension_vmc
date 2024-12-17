import omni.ext
import omni.ui as ui
from .udp_receiver import UDPReceiver
from .skeleton_mapper import SkeletonMapper
from .vmc_parser import parse_vmc_message
from .CircularQueue import CircularQueue
from pxr import Sdf, UsdSkel, Gf, UsdUtils, Usd
import carb.events



# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
# def some_public_function(x: int):
#     print(f"[omni.hello.world] some_public_function was called with {x}")
#     return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
# class MyExtension(omni.ext.IExt):
#     # ext_id is current extension id. It can be used with extension manager to query additional information, like where
#     # this extension is located on filesystem.
#     def on_startup(self, ext_id):
#         print("[omni.hello.world] MyExtension startup")

#         self._count = 0

#         self._window = ui.Window("My Window", width=300, height=300)
#         with self._window.frame:
#             with ui.VStack():
#                 label = ui.Label("")
                

#                 def on_click():
#                     self._count += 1
#                     label.text = f"count: {self._count}"

#                 def on_reset():
#                     self._count = 0
#                     label.text = "empty"

#                 on_reset()

#                 with ui.HStack():
#                     ui.Button("Add", clicked_fn=on_click)
#                     ui.Button("Reset", clicked_fn=on_reset)

#     def on_shutdown(self):
#         print("[omni.hello.world] MyExtension shutdown")


class MyExtension(omni.ext.IExt):
    # def __init__(self):
    #     self._window = None

    def on_startup(self, ext_id):
        self.frame_queue = CircularQueue(5)
        self._stage = omni.usd.get_context().get_stage()
        self._skeleton_mapper = None
        self._ip='127.0.0.1'
        self._port=39539
        # skeleton_path='/World/Character/Root'
        skeleton_path='/World/Armature0/Skeleton'
        animation_path='/World/Armature0/Anim'
        self._skeleton_mapper = SkeletonMapper(skeleton_path, animation_path)

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

            # # Skeleton Selection
            # ui.Label("Select Skeleton Prim:")
            # skeleton_combo = ui.ComboBox(0, *self.get_skeleton_prims(self._stage.Open("path_to_stage.usda")))
            # skeleton_combo.model.add_value_changed_fn(lambda m: self.on_skeleton_selected(m.get_item_value_model().get_value_as_string()))
            with ui.HStack():
                self.start_button = ui.Button("Start Receiving", clicked_fn=self.start_receiving)
                self.stop_button = ui.Button("Stop Receiving", clicked_fn=self.stop_receiving)
                self.udp_receiver = None

                # Debug Button
                debug_button = ui.Button("Debug", clicked_fn=self.on_debug_clicked)


    def start_receiving(self):
        if not self.udp_receiver:
            self.udp_receiver = UDPReceiver(self.process_vmc_data, self._ip, self._port)
            self.udp_receiver.start()
            self.register_event()
            # self.label.text = "Receiving VMC data..."

    def stop_receiving(self):
        if self.udp_receiver:
            self.udp_receiver.stop()
            self.udp_receiver = None
            # self.label.text = "Stopped receiving."

    def register_event(self):
        app = omni.kit.app.get_app()
        self._subscription_handle = app.get_pre_update_event_stream().create_subscription_to_pop(
            self.on_update_anim, order=-1000000, name="anim_pre_update"
        )

    def on_update_anim(self,e):
        entry=self.frame_queue.dequeue()
        if entry:
            self._skeleton_mapper.update_skel_anim(entry["timestamp"],entry["joints"])
        else: 
            print("No data in frame_queue")

    def process_vmc_data(self, data):
        parsed_messages = parse_vmc_message(data)

        entry = {"timestamp": 0, 
                 "joints": []
                 }
        # joint_info = {
        #         "name": joint_name,
        #         "position": position,
        #         "rotation": rotation
        #     }

        for item in parsed_messages:
            # print(item)
            if item['address'] == '/VMC/Ext/T':
                timestamp=self.process_timestamp(item)
                entry["timestamp"]=timestamp
            # elif item['address'] == '/VMC/Ext/Root/Pos':
            #     self.process_root_pose(item)
            elif item['address'] == '/VMC/Ext/Bone/Pos':
                joint_info=self.process_bone_pose(item, self._skeleton_mapper)
                entry["joints"].append(joint_info)
            # elif item['address'] == '/VMC/Ext/Blend/Val':
            #     self.process_expression_value(item)
            # elif item['address'] == '/VMC/Ext/Blend/Apply':
            #     self.process_expression_confirmation(item)
            # elif item['address'] == '/VMC/Ext/OK':
            #     self.process_heartbeat_check(item)
        # self._skeleton_mapper.update_skel_anim(entry["timestamp"],entry["joints"])
        if not self.frame_queue.enqueue(entry):
            # print("Failed to enqueue data.")
            x=1

    def submit(self):
        self._skeleton_mapper.submit_joint_transforms()

    # Helper functions for validation and skeleton retrieval
    def validate_ip(self, ip_text):
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(pattern, ip_text):
            print(f"Valid IP: {ip_text}")
            self._ip=ip_text
        else:
            print("Invalid IP format")

    def validate_port(self, port_text):
        if port_text.isdigit() and 0 <= int(port_text) <= 65535:
            print(f"Valid Port: {port_text}")
            self._port=int(port_text)
        else:
            print("Invalid Port")

    def get_skeleton_prims(stage):
        return [prim.GetPath().pathString for prim in stage.Traverse() if prim.GetTypeName() == "Skeleton"]

    def on_skeleton_selected(self, selection):
        print(f"Selected Skeleton: {selection}")
        self.set_skeleton(selection)

    def on_debug_clicked(self):
        print("Debug Button Clicked")
        entry=self.frame_queue.dequeue()
        if entry:
            self._skeleton_mapper.update_skel_anim(entry["timestamp"],entry["joints"])
        else: 
            print("No data in frame_queue")
        # self._skeleton_mapper.update_skel_anim(0, None)

    def on_shutdown(self):
        print("[omni.hello.world] MyExtension shutdown")
        if self.udp_receiver:
            self.udp_receiver.stop()

    def process_timestamp(self, data):
        timestamp = data['args'][0]
        # print(f"Processing timestamp: {timestamp}")
        return timestamp

    def process_root_pose(self, data):
        name = data['args'][0]
        translation = data['args'][1:4]
        quaternion = data['args'][4:]
        print(f"Processing root pose: {name}, Translation: {translation}, Quaternion: {quaternion}")

    def process_bone_pose(self, data, skeleton_mapper):
        name = data['args'][0]
        translation = data['args'][1:4]
        quaternion = data['args'][4:]
        # print(f"Processing bone pose: {name}")
        # print(f"Processing bone pose: {name}, Translation: {translation}, Quaternion: {quaternion}\n")
        # skeleton_mapper.apply_bone_pose(name, translation, quaternion)
        joint_info = {
                "name": name,
                "position": translation,
                "rotation": quaternion
            }
        return joint_info

    def process_expression_value(self, data):
        expression_name = data['args'][0]
        value = data['args'][1]
        # if value==0:
        #     return
        print(f"Processing expression value: {expression_name}, Value: {value}\n")

    def process_expression_confirmation(self, data):
        print("Processing expression confirmation.\n")

    def process_heartbeat_check(self, data):
        args = data['args']
        print(f"Processing heartbeat check: {args}\n")


# if __name__ == "__main__":
#     plugin = MyExtension()
#     plugin.start_receiving()