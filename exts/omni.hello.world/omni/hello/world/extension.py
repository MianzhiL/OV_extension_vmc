import omni.ext
import omni.ui as ui
from .udp_receiver import UDPReceiver
from .skeleton_mapper import SkeletonMapper
from .vmc_parser import parse_vmc_message
from .CircularQueue import CircularQueue
from pxr import Sdf, UsdSkel, Gf, UsdUtils, Usd
import carb.events
import re


class Extension(omni.ext.IExt):
    """Omniverse Extension for receiving and processing VMC data for skeleton animation."""

    MAX_QUEUE_SIZE = 5  # Maximum size of the frame queue

    def on_startup(self, ext_id):
        """Initialize the extension and set up the UI and UDP receiver."""
        self.frame_queue = CircularQueue(5)
        self._stage = omni.usd.get_context().get_stage()
        self._ip='127.0.0.1'
        self._port=39539
        
        skeleton_path='/World/kikiyo_01/kikiyo/Armature_Skel/Skeleton'
        animation_path='/World/kikiyo_01/kikiyo/Armature_Skel/Anim'
        self._skeleton_mapper = SkeletonMapper(skeleton_path, animation_path)

        self._window = ui.Window("VMC Extension", width=400, height=300)
        with self._window.frame:
            self.build_ui()

    def build_ui(self):
        """Build the user interface for the extension."""
        with ui.VStack():
            # IP Address Input
            ui.Label("Enter IP Address:")
            ip_field = ui.StringField()
            ip_field.model.add_value_changed_fn(lambda m: self.validate_ip(m.get_value_as_string()))

            # Port Input
            ui.Label("Enter Port:")
            port_field = ui.StringField()
            port_field.model.add_value_changed_fn(lambda m: self.validate_port(m.get_value_as_string()))
            
            with ui.HStack():
                self.start_button = ui.Button("Start Receiving", clicked_fn=self.start_receiving)
                self.stop_button = ui.Button("Stop Receiving", clicked_fn=self.stop_receiving)
                # self.stop_play_button = ui.Button("Stop Playing", clicked_fn=self.stop_playing)
                self.udp_receiver = None

                # Debug Button
                debug_button = ui.Button("Debug", clicked_fn=self.on_debug_clicked)


    def start_receiving(self):
        """Start receiving VMC data via UDP."""
        if not self.udp_receiver:
            self.udp_receiver = UDPReceiver(self.process_vmc_data, self._ip, self._port)
            self.udp_receiver.start()
            self.register_event()

    def stop_receiving(self):
        if self.udp_receiver:
            self.udp_receiver.stop()
            self.udp_receiver = None

    def register_event(self):
        """Register the update event for animating the skeleton."""
        app = omni.kit.app.get_app()
        self._subscription_handle = app.get_pre_update_event_stream().create_subscription_to_pop(
            self.on_update_anim, order=-1000000, name="anim_pre_update"
        )

    def on_update_anim(self,e):
        """Update skeleton animation based on received data."""
        entry=self.frame_queue.dequeue()
        if entry:
            self._skeleton_mapper.update_skel_anim(entry["timestamp"],entry["root"],entry["joints"])
        else: 
            print("No data in frame_queue")

    def process_vmc_data(self, data):
        """Process incoming VMC data and enqueue it for animation updates."""
        parsed_messages = parse_vmc_message(data)

        entry = {"timestamp": 0, 
                 "root":{},
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
            elif item['address'] == '/VMC/Ext/Root/Pos':
                root_info=self.process_root_pose(item)
                entry["root"]=root_info
            elif item['address'] == '/VMC/Ext/Bone/Pos':
                joint_info=self.process_bone_pose(item)
                entry["joints"].append(joint_info)
            elif item['address'] == '/VMC/Ext/Blend/Val':
                self.process_expression_value(item)
            elif item['address'] == '/VMC/Ext/Blend/Apply':
                self.process_expression_confirmation(item)
            elif item['address'] == '/VMC/Ext/OK':
                self.process_heartbeat_check(item)
        if not self.frame_queue.enqueue(entry):
            print("Failed to enqueue data.")

    def validate_ip(self, ip_text):
        """Validate the format of the provided IP address."""
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(pattern, ip_text):
            print(f"Valid IP: {ip_text}")
            self._ip=ip_text
        else:
            print("Invalid IP format")

    def validate_port(self, port_text):
        """Validate the provided port number."""
        if port_text.isdigit() and 0 <= int(port_text) <= 65535:
            print(f"Valid Port: {port_text}")
            self._port=int(port_text)
        else:
            print("Invalid Port")

    def on_debug_clicked(self):
        print("Debug Button Clicked")
        # entry=self.frame_queue.dequeue()
        # if entry:
        #     self._skeleton_mapper.update_skel_anim(entry["timestamp"],entry["joints"])
        # else: 
        #     print("No data in frame_queue")
        self._skeleton_mapper.update_skel_anim(0, None)

    def on_shutdown(self):
        print("[omni.anim.vmc] VMC extension shutdown")
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
        # print(f"Processing root pose: {name}, Translation: {translation}, Quaternion: {quaternion}")
        root_info = {
                "position": translation,
                "rotation": quaternion
            }
        return root_info
    
    def process_bone_pose(self, data):
        name = data['args'][0]
        translation = data['args'][1:4]
        quaternion = data['args'][4:]
        # print(f"Processing bone pose: {name}")
        # print(f"Processing bone pose: {name}, Translation: {translation}, Quaternion: {quaternion}\n")
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
