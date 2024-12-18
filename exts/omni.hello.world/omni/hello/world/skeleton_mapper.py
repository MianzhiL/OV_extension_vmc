import omni.ext
import omni.ui as ui
from pxr import Sdf, UsdSkel, Gf, UsdUtils, Usd, UsdGeom, Vt

joint_name_mapping = {
    "Hips": "Hips",
    "LeftUpperLeg": "Upper_leg_L",
    "RightUpperLeg": "Upper_leg_R",
    "LeftLowerLeg": "Lower_leg_L",
    "RightLowerLeg": "Lower_leg_R",
    "LeftFoot": "Foot_L",
    "RightFoot": "Foot_R",
    "Spine": "Spine",
    "Chest": "Chest",
    "Neck": "Neck",
    "Head": "Head",
    "LeftShoulder": "Shoulder_L",
    "RightShoulder": "Shoulder_R",
    "LeftUpperArm": "Upper_arm_L",
    "RightUpperArm": "Upper_arm_R",
    "LeftLowerArm": "Lower_arm_L",
    "RightLowerArm": "Lower_arm_R",
    "LeftHand": "Hand_L",
    "RightHand": "Hand_R",
    "LeftToes": "Toe_L",
    "RightToes": "Toe_R",
    "LeftEye": "LeftEye",
    "RightEye": "RightEye",
    "Jaw": "Hair_Front2",
    # Left hand fingers
    "LeftThumbProximal": "Thumb_Proximal_L",
    "LeftThumbIntermediate": "Thumb_Intermediate_L",
    "LeftThumbDistal": "Thumb_Distal_L",
    "LeftIndexProximal": "Index_Proximal_L",
    "LeftIndexIntermediate": "Index_Intermediate_L",
    "LeftIndexDistal": "Index_Distal_L",
    "LeftMiddleProximal": "Middle_Proximal_L",
    "LeftMiddleIntermediate": "Middle_Intermediate_L",
    "LeftMiddleDistal": "Middle_Distal_L",
    "RightThumbProximal": "Thumb_Proximal_R",
    "RightThumbIntermediate": "Thumb_Intermediate_R",
    "RightThumbDistal": "Thumb_Distal_R",
    "RightIndexProximal": "Index_Proximal_R",
    "RightIndexIntermediate": "Index_Intermediate_R",
    "RightIndexDistal": "Index_Distal_R",
    "RightMiddleProximal": "Middle_Proximal_R",
    "RightMiddleIntermediate": "Middle_Intermediate_R",
    "RightMiddleDistal": "Middle_Distal_R",
}

# joint_name_mapping = {
#     "Hips": "Hips_Skel",
#     'LeftUpperLeg': 'Upper_leg_L_Skel',
#     'RightUpperLeg': 'Upper_leg_R_Skel',
#     'LeftLowerLeg': 'Lower_leg_L_Skel',
#     'RightLowerLeg': 'Lower_leg_R_Skel',
#     'LeftFoot': 'Foot_L_Skel',
#     'RightFoot': 'Foot_R_Skel',
#     'Spine': 'Spine_Skel',
#     'Chest': 'Chest_Skel',
#     'Neck': 'Neck_Skel',
#     'Head': 'Head_Skel',
#     'LeftShoulder': 'Shoulder_L_Skel',
#     'RightShoulder': 'Shoulder_R_Skel',
#     'LeftUpperArm': 'Upper_arm_L_Skel',
#     'RightUpperArm': 'Upper_arm_R_Skel',
#     'LeftLowerArm': 'Lower_arm_L_Skel',
#     'RightLowerArm': 'Lower_arm_R_Skel',
#     'LeftHand': 'Hand_L_Skel',
#     'RightHand': 'Hand_R_Skel',
#     'LeftToes': 'Toe_L_Skel',
#     'RightToes': 'Toe_R_Skel',
#     'LeftEye': 'LeftEye_Skel',
#     'RightEye': 'RightEye_Skel',
#     'Jaw': 'Hair_Front2_Skel',
#     # Left hand fingers
#     'LeftThumbProximal': 'Thumb_Proximal_L_Skel',
#     'LeftThumbIntermediate': 'Thumb_Intermediate_L_Skel',
#     'LeftThumbDistal': 'Thumb_Distal_L_Skel',
#     'LeftIndexProximal': 'Index_Proximal_L_Skel',
#     'LeftIndexIntermediate': 'Index_Intermediate_L_Skel',
#     'LeftIndexDistal': 'Index_Distal_L_Skel',
#     'LeftMiddleProximal': 'Middle_Proximal_L_Skel',
#     'LeftMiddleIntermediate': 'Middle_Intermediate_L_Skel',
#     'LeftMiddleDistal': 'Middle_Distal_L_Skel',
#     "RightThumbProximal": "Thumb_Proximal_R_Skel",
#     "RightThumbIntermediate": "Thumb_Intermediate_R_Skel",
#     "RightThumbDistal": "Thumb_Distal_R_Skel",
#     "RightIndexProximal": "Index_Proximal_R_Skel",
#     "RightIndexIntermediate": "Index_Intermediate_R_Skel",
#     "RightIndexDistal": "Index_Distal_R_Skel",
#     "RightMiddleProximal": "Middle_Proximal_R_Skel",
#     "RightMiddleIntermediate": "Middle_Intermediate_R_Skel",
#     "RightMiddleDistal": "Middle_Distal_R_Skel",
# }

def find_relative_path(joint_end_path, dict):
    matching_paths = [path for path in dict if path.endswith('/' + joint_end_path)]
    return matching_paths[0] if matching_paths else None

def convert_position_to_omniverse(position):
    """
    将左手 (Y-up) 坐标转换为 Omniverse (Z-up, Right-handed) 坐标。
    :param position: 左手坐标，格式为 [x, y, z]
    :return: 转换后的 Omniverse 坐标，格式为 [x, z, y]
    """
    x, y, z = position
    return Gf.Vec3f(x, y, z)

def convert_quaternion_to_omniverse(quaternion):
    """
    将左手 (Y-up) 四元数转换为 Omniverse (Z-up, Right-handed) 四元数。
    :param quaternion: 左手四元数，格式为 [w, x, y, z]
    :return: 转换后的 Omniverse 四元数，格式为 [w, x, z, y]
    """
    x, y, z, w = quaternion
    return Gf.Quatf(w, Gf.Vec3f(x, y, z))

# def set_local_pose(prim, position, rotation):
    # if prim and prim.IsA(UsdGeom.Xform):
    #     xformable = UsdGeom.Xform(prim)
    #     # Retrieve existing transform operations
    #     xform_ops = xformable.GetOrderedXformOps()
        
    #     # Find existing translate and orient operations
    #     translate_op = next((op for op in xform_ops if op.GetOpType() == UsdGeom.XformOp.TypeTranslate), None)
    #     orient_op = next((op for op in xform_ops if op.GetOpType() == UsdGeom.XformOp.TypeOrient), None)
        
    #     # Update or create translate operation
    #     if translate_op:
    #         translate_op.Set(Gf.Vec3d(position))
    #     else:
    #         translate_op = xformable.AddTranslateOp()
    #         translate_op.Set(Gf.Vec3d(position))
        
    #     # Update or create orient operation
    #     if orient_op:
    #         quaternion = Gf.Quatf(rotation[3], rotation[0], rotation[1], rotation[2])  # Quaternion format (w, x, y, z)
    #         orient_op.Set(quaternion)
    #     else:
    #         orient_op = xformable.AddOrientOp()
    #         quaternion = Gf.Quatf(rotation[3], rotation[0], rotation[1], rotation[2])
    #         orient_op.Set(quaternion)
        
class SkeletonMapper:
    def __init__(self, skeleton_path, animation_path):
        self._stage = omni.usd.get_context().get_stage()
        self.set_skeleton(skeleton_path)
        self.define_animation(animation_path)

    def define_animation(self, animation_path):
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
        self._skel_prim=self._stage.GetPrimAtPath(skeleton_path)
        self._skeleton = None
        if self._skel_prim:
            self._skeleton = UsdSkel.Skeleton(self._skel_prim)
        else:
            # failed
            print("Bind skeleton failed: {skeleton_path}")
            return

        self._joint_paths=self._skeleton.GetJointsAttr().Get()
        self.joint_path_to_index = {path: i for i, path in enumerate(self._joint_paths)}
        self._default_transforms = self._skeleton.GetRestTransformsAttr().Get()
        self._default_translations = [Gf.Vec3f(transform.ExtractTranslation()) for transform in self._default_transforms]
        self._default_rotations = [Gf.Quatf(transform.ExtractRotationQuat()) for transform in self._default_transforms]
        self.translations=Vt.Vec3fArray(self._default_translations)
        self.rotations=Vt.QuatfArray(self._default_rotations)
        # a=joint_names[0]
        # b=bind_transforms[0]
        # y=1
    
    def update_skel_anim(self, timestamp, joint_data):
        time_code = Usd.TimeCode(timestamp)

        if not joint_data:
            transform_array = Vt.Matrix4dArray(self._default_transforms)
            self._animation.SetTransforms(transform_array, 0)
            return

        # # Prepare lists for translations and rotations
        
        # default_transforms = self._default_transforms
        # transforms = list(default_transforms)

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
                # transform = Gf.Matrix4d()
                # print(transform)
                # transform.SetRotate(rotation)
                # print(transform)
                # transform.SetTranslate(translation)
                # print(transform)
                # print("\n")
                # transforms[index] = transform
                self.translations[index]=translation
                self.rotations[index]=rotation
            else:
                print(f"joint_relative_path not found: {joint_end_path}")

        # transform_array = Vt.Matrix4dArray(transforms)
        # self._animation.SetTransforms(transform_array, 0)
        self._animation.GetTranslationsAttr().Set(self.translations, 0)
        self._animation.GetRotationsAttr().Set(self.rotations, 0)
        # print(f"Set transform done of timestamp: {timestamp}")

    
    def apply_bone_pose(self, joint_name, translation, quaternion):
        if joint_name not in joint_name_mapping:
            print("joint not found in dict: {joint_name}\n")
            return
        joint_end_path=joint_name_mapping[joint_name]
        joint_relative_path=find_relative_path(joint_end_path,self._joint_paths)
        if not joint_relative_path:
            print("joint not found in model: {joint_end_path}\n")
            return
        joint_path=f"/World/Armature0/Skeleton/{joint_relative_path}"
        joint_prim = self._stage.GetPrimAtPath(joint_path)
        if not joint_prim.IsValid():
            print("joint path wrong: {joint_path}")
        set_local_pose(joint_prim,translation,quaternion)

        # joint_index = self._joint_names.index(joint_name)

        # target_matrix = self._joint_transforms[joint_index]
        # target_matrix.SetTranslateOnly(Gf.Vec3d(translation))
        # rotation_matrix = Gf.Quatf(*quaternion).GetMatrix()
        # target_matrix.SetRotateOnly(Gf.Rotation(Gf.Matrix3d(rotation_matrix)))
        
    # def map_to_skeleton(self, parsed_messages):
    #     for joint_name, translation, quaternion in parsed_messages:
    #         if joint_name not in self._joint_names:
    #             print("joint not found: {joint_name}\n")
    #             continue
    #         joint_index = self._joint_names.index(joint_name)

    #         target_matrix = self._joint_transforms[joint_index]
    #         target_matrix.SetTranslateOnly(Gf.Vec3d(translation))
    #         rotation_matrix = Gf.Quatf(*quaternion).GetMatrix()
    #         target_matrix.SetRotateOnly(Gf.Rotation(Gf.Matrix3d(rotation_matrix)))

    # def submit_joint_transforms(self):
    #     self._skeleton.GetJointLocalTransformsAttr().Set(self._joint_transforms)

    
