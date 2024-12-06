class SkeletonMapper:
    def __init__(self, skeleton):
        # skeleton: 传入的骨骼对象，包含所有骨骼的引用
        self.skeleton = skeleton

    def map_to_skeleton(self, position, quaternion):
        """
        将接收到的位置和四元数映射到骨骼上

        :param position: 根骨骼的位置 [x, y, z]
        :param quaternion: 根骨骼的旋转四元数 [q.x, q.y, q.z, q.w]
        """
        # 更新根骨骼的位置
        self.update_bone_position("Root", position)

        # 更新根骨骼的旋转
        self.update_bone_rotation("Root", quaternion)

        # 如果有其他骨骼需要更新，可以在这里添加逻辑
        # 例如，遍历所有子骨骼并更新它们的位置和旋转
        for bone_name in self.skeleton.get_all_bone_names():
            if bone_name != "Root":
                # 这里可以根据具体逻辑更新其他骨骼的位置和旋转
                # 例如，使用某种插值或相对位置计算
                pass

    def update_bone_position(self, bone_name, position):
        """
        更新指定骨骼的位置

        :param bone_name: 骨骼名称
        :param position: 新位置 [x, y, z]
        """
        bone = self.skeleton.get_bone(bone_name)
        if bone:
            bone.set_position(position)

    def update_bone_rotation(self, bone_name, quaternion):
        """
        更新指定骨骼的旋转

        :param bone_name: 骨骼名称
        :param quaternion: 新旋转四元数 [q.x, q.y, q.z, q.w]
        """
        bone = self.skeleton.get_bone(bone_name)
        if bone:
            bone.set_rotation(quaternion)