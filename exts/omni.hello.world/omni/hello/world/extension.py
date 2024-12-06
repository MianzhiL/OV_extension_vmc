# import omni.ext
# import omni.ui as ui
from udp_receiver import UDPReceiver
from skeleton_mapper import SkeletonMapper
from vmc_parser import parse_vmc_data


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
# def some_public_function(x: int):
#     print(f"[omni.hello.world] some_public_function was called with {x}")
#     return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.

class MyExtension:
# class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    # def on_startup(self, ext_id):
    #     print("[omni.hello.world] MyExtension startup")

    #     self._count = 0

    #     self._window = ui.Window("My Window", width=300, height=300)
    #     with self._window.frame:
    #         with ui.VStack():
    #             label = ui.Label("")
                

    #             def on_click():
    #                 self._count += 1
    #                 label.text = f"count: {self._count}"

    #             def on_reset():
    #                 self._count = 0
    #                 label.text = "empty"

    #             on_reset()

    #             with ui.HStack():
    #                 ui.Button("Add", clicked_fn=on_click)
    #                 ui.Button("Reset", clicked_fn=on_reset)

    # def on_startup(self, ext_id):
    #     print("[my_omniverse_plugin] MyExtension startup")

    #     self._count = 0
    #     self._skeleton_mapper = SkeletonMapper()

    #     self._window = ui.Window("VMC Receiver", width=400, height=300)
    #     with self._window.frame:
    #         with ui.VStack():
    #             self.label = ui.Label("Waiting for VMC data...")
    #             self.start_button = ui.Button("Start Receiving", clicked_fn=self.start_receiving)
    #             self.stop_button = ui.Button("Stop Receiving", clicked_fn=self.stop_receiving)

    #             self.udp_receiver = None

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
        parsed_data = parse_vmc_data(data)
        for msg in parsed_messages:
            print(msg)
        # self._skeleton_mapper.map_to_skeleton(root_position)

if __name__ == "__main__":
    plugin = MyExtension()
    plugin.start_receiving()