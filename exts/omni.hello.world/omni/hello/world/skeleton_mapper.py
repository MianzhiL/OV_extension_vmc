class SkeletonMapper:
    def __init__(self, skeleton):
        self.set_skeleton(skeleton)

    def set_skeleton(self, skeleton):
        self._skeleton=skeleton
        self._joint_names=self._skeleton.GetJointsAttr().Get()
        self._joint_transforms = self._skeleton.GetJointLocalTransformsAttr().Get()
        # a=joint_names[0]
        # b=bind_transforms[0]
        # y=1
    def apply_bone_pose(self, joint_name, translation, quaternion):
        if joint_name not in self._joint_names:
            print("joint not found: {joint_name}\n")
            return
        joint_index = self._joint_names.index(joint_name)

        target_matrix = self._joint_transforms[joint_index]
        target_matrix.SetTranslateOnly(Gf.Vec3d(translation))
        rotation_matrix = Gf.Quatf(*quaternion).GetMatrix()
        target_matrix.SetRotateOnly(Gf.Rotation(Gf.Matrix3d(rotation_matrix)))
        
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

    def submit_joint_transforms(self):
        self._skeleton.GetJointLocalTransformsAttr().Set(self._joint_transforms)

    
