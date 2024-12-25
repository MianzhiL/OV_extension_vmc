import omni.ext
import omni.ui as ui
from pxr import Sdf, UsdSkel, Gf, UsdUtils, Usd, UsdGeom, Vt

# joint_name_mapping = {
#     "Hips": "Hips",
#     "LeftUpperLeg": "Upper_leg_L",
#     "RightUpperLeg": "Upper_leg_R",
#     "LeftLowerLeg": "Lower_leg_L",
#     "RightLowerLeg": "Lower_leg_R",
#     "LeftFoot": "Foot_L",
#     "RightFoot": "Foot_R",
#     "Spine": "Spine",
#     "Chest": "Chest",
#     "Neck": "Neck",
#     "Head": "Head",
#     "LeftShoulder": "Shoulder_L",
#     "RightShoulder": "Shoulder_R",
#     "LeftUpperArm": "Upper_arm_L",
#     "RightUpperArm": "Upper_arm_R",
#     "LeftLowerArm": "Lower_arm_L",
#     "RightLowerArm": "Lower_arm_R",
#     "LeftHand": "Hand_L",
#     "RightHand": "Hand_R",
#     "LeftToes": "Toe_L",
#     "RightToes": "Toe_R",
#     "LeftEye": "LeftEye",
#     "RightEye": "RightEye",
#     "Jaw": "Hair_Front2",
#     # Left hand fingers
#     "LeftThumbProximal": "Thumb_Proximal_L",
#     "LeftThumbIntermediate": "Thumb_Intermediate_L",
#     "LeftThumbDistal": "Thumb_Distal_L",
#     "LeftIndexProximal": "Index_Proximal_L",
#     "LeftIndexIntermediate": "Index_Intermediate_L",
#     "LeftIndexDistal": "Index_Distal_L",
#     "LeftMiddleProximal": "Middle_Proximal_L",
#     "LeftMiddleIntermediate": "Middle_Intermediate_L",
#     "LeftMiddleDistal": "Middle_Distal_L",
#     "RightThumbProximal": "Thumb_Proximal_R",
#     "RightThumbIntermediate": "Thumb_Intermediate_R",
#     "RightThumbDistal": "Thumb_Distal_R",
#     "RightIndexProximal": "Index_Proximal_R",
#     "RightIndexIntermediate": "Index_Intermediate_R",
#     "RightIndexDistal": "Index_Distal_R",
#     "RightMiddleProximal": "Middle_Proximal_R",
#     "RightMiddleIntermediate": "Middle_Intermediate_R",
#     "RightMiddleDistal": "Middle_Distal_R",
# }

joint_name_mapping = {
    "Hips": "Hips_Skel",
    'LeftUpperLeg': 'Upper_leg_L_Skel',
    'RightUpperLeg': 'Upper_leg_R_Skel',
    'LeftLowerLeg': 'Lower_leg_L_Skel',
    'RightLowerLeg': 'Lower_leg_R_Skel',
    'LeftFoot': 'Foot_L_Skel',
    'RightFoot': 'Foot_R_Skel',
    'Spine': 'Spine_Skel',
    'Chest': 'Chest_Skel',
    'Neck': 'Neck_Skel',
    'Head': 'Head_Skel',
    'LeftShoulder': 'Shoulder_L_Skel',
    'RightShoulder': 'Shoulder_R_Skel',
    'LeftUpperArm': 'Upper_arm_L_Skel',
    'RightUpperArm': 'Upper_arm_R_Skel',
    'LeftLowerArm': 'Lower_arm_L_Skel',
    'RightLowerArm': 'Lower_arm_R_Skel',
    'LeftHand': 'Hand_L_Skel',
    'RightHand': 'Hand_R_Skel',
    'LeftToes': 'Toe_L_Skel',
    'RightToes': 'Toe_R_Skel',
    'LeftEye': 'LeftEye_Skel',
    'RightEye': 'RightEye_Skel',
    'Jaw': 'Hair_Front2_Skel',
    # Left hand fingers
    'LeftThumbProximal': 'Thumb_Proximal_L_Skel',
    'LeftThumbIntermediate': 'Thumb_Intermediate_L_Skel',
    'LeftThumbDistal': 'Thumb_Distal_L_Skel',
    'LeftIndexProximal': 'Index_Proximal_L_Skel',
    'LeftIndexIntermediate': 'Index_Intermediate_L_Skel',
    'LeftIndexDistal': 'Index_Distal_L_Skel',
    'LeftMiddleProximal': 'Middle_Proximal_L_Skel',
    'LeftMiddleIntermediate': 'Middle_Intermediate_L_Skel',
    'LeftMiddleDistal': 'Middle_Distal_L_Skel',
    "RightThumbProximal": "Thumb_Proximal_R_Skel",
    "RightThumbIntermediate": "Thumb_Intermediate_R_Skel",
    "RightThumbDistal": "Thumb_Distal_R_Skel",
    "RightIndexProximal": "Index_Proximal_R_Skel",
    "RightIndexIntermediate": "Index_Intermediate_R_Skel",
    "RightIndexDistal": "Index_Distal_R_Skel",
    "RightMiddleProximal": "Middle_Proximal_R_Skel",
    "RightMiddleIntermediate": "Middle_Intermediate_R_Skel",
    "RightMiddleDistal": "Middle_Distal_R_Skel",

    "LeftRingProximal":"Ring_Proximal_L_Skel",
    "LeftRingIntermediate":"Ring_Intermediate_L_Skel",
    "LeftRingDistal":"Ring_Distal_L_Skel",
    "LeftLittleProximal":"Little_Proximal_L_Skel",
    "LeftLittleIntermediate":"Little_Intermediate_L_Skel",
    "LeftLittleDistal":"Little_Distal_L_Skel",
    "RightRingProximal":"Ring_Proximal_R_Skel",
    "RightRingIntermediate":"Ring_Intermediate_R_Skel",
    "RightRingDistal":"Ring_Distal_R_Skel",
    "RightLittleProximal":"Little_Proximal_R_Skel",
    "RightLittleIntermediate":"Little_Intermediate_R_Skel",
    "RightLittleDistal":"Little_Distal_R_Skel"
}

def find_relative_path(joint_end_path, dict):
    """Find the relative path of a joint in the provided paths.

    Args:
        joint_end_path (str): The end path of the joint.
        paths (list): A list of paths to search.

    Returns:
        str or None: The matching path if found, otherwise None.
    """
    matching_paths = [path for path in dict if path.endswith('/' + joint_end_path)]
    return matching_paths[0] if matching_paths else None

def convert_position_to_omniverse(position):
    """Convert left-handed (Y-up) coordinates to Omniverse (Z-up, Right-handed) coordinates.

    Args:
        position (list): Left-handed coordinates in the format [x, y, z].

    Returns:
        Gf.Vec3f: Converted Omniverse coordinates in the format [x, z, y].
    """
    x, y, z = position
    return Gf.Vec3f(x, y, z)

def convert_quaternion_to_omniverse(quaternion):
    """Convert left-handed (Y-up) quaternion to Omniverse (Z-up, Right-handed) quaternion.

    Args:
        quaternion (list): Left-handed quaternion in the format [w, x, y, z].

    Returns:
        Gf.Quatf: Converted Omniverse quaternion in the format [w, x, z, y].
    """
    x, y, z, w = quaternion
    return Gf.Quatf(w, Gf.Vec3f(x, y, z))

class SkeletonMapper:
    def __init__(self, skeleton_path, animation_path):
        """Initialize the SkeletonMapper with given skeleton and animation paths.

        Args:
            skeleton_path (str): The USD path to the skeleton.
            animation_path (str): The USD path for the animation.
        """
        self._stage = omni.usd.get_context().get_stage()
        self.set_skeleton(skeleton_path)
        self.define_animation(animation_path)

    def define_animation(self, animation_path):
        """Define the animation for the skeleton.

        Args:
            animation_path (str): The USD path for the animation.
        """
        self._animation = UsdSkel.Animation.Define(self._stage, animation_path)
        self._animation.GetJointsAttr().Set(self._joint_paths)
        constant_scales = [Gf.Vec3h(1.0, 1.0, 1.0) for _ in self._joint_paths]
        self._animation.GetScalesAttr().Set(constant_scales)

        if self._skel_prim.IsValid():
            binding_api = UsdSkel.BindingAPI.Apply(self._skel_prim)
            binding_api.GetAnimationSourceRel().SetTargets([animation_path])
        else:
            raise ValueError("Invalid prim: self._skel_prim is not a valid UsdPrim.")

    def set_skeleton(self, skeleton_path):
        """Set the skeleton based on the provided path.

        Args:
            skeleton_path (str): The USD path to the skeleton.
        """
        self._skel_prim=self._stage.GetPrimAtPath(skeleton_path)
        self._skeleton = None
        if not self._skel_prim:
            print(f"Bind skeleton failed: {skeleton_path}")
            return
        self._skeleton = UsdSkel.Skeleton(self._skel_prim)
        if not self._skeleton:
            print(f"Bind skeleton failed: {skeleton_path}")
            return
        
        self._joint_paths=self._skeleton.GetJointsAttr().Get()
        self.joint_path_to_index = {path: i for i, path in enumerate(self._joint_paths)}
        self._default_transforms = self._skeleton.GetRestTransformsAttr().Get()
        # Extract default translations and rotations
        self._default_translations = [Gf.Vec3f(transform.ExtractTranslation()) for transform in self._default_transforms]
        self._default_rotations = [Gf.Quatf(transform.ExtractRotationQuat()) for transform in self._default_transforms]
        
        # Initialize translation and rotation arrays
        self.translations=Vt.Vec3fArray(self._default_translations)
        self.rotations=Vt.QuatfArray(self._default_rotations)

    def update_skel_anim(self, timestamp, root_data, joint_data):
        """Update skeleton animation based on received data.

        Args:
            timestamp (float): The timestamp of the animation update.
            root_data (dict): Data for the root joint.
            joint_data (list): List of joint data dictionaries.
        """
        time_code = Usd.TimeCode(timestamp)

        if not joint_data:
            transform_array = Vt.Matrix4dArray(self._default_transforms)
            self._animation.SetTransforms(transform_array, 0)
            return
        
        if root_data:
            root_translation = convert_position_to_omniverse(root_data["position"])
            root_rotation = convert_quaternion_to_omniverse(root_data["rotation"])
            self.translations[0]=root_translation
            self.rotations[0]=root_rotation

        # Iterate over each joint in the entry
        for joint in joint_data:
            joint_name = joint["name"]

            if joint_name not in joint_name_mapping:
                print(f"joint not found in dict: {joint_name}\n")
                continue

            joint_end_path=joint_name_mapping[joint_name]
            joint_relative_path=find_relative_path(joint_end_path,self._joint_paths)

            if joint_relative_path in self.joint_path_to_index:
                index = self.joint_path_to_index[joint_relative_path]
                translation = convert_position_to_omniverse(joint["position"])
                rotation = convert_quaternion_to_omniverse(joint["rotation"])

                # Update translations and rotations
                self.translations[index]=translation
                self.rotations[index]=rotation
            else:
                print(f"joint_relative_path not found: {joint_end_path}")

        # Set updated translations and rotations to animation attributes
        self._animation.GetTranslationsAttr().Set(self.translations, 0)
        self._animation.GetRotationsAttr().Set(self.rotations, 0)
        # print(f"Set transform done of timestamp: {timestamp}")
