#!/usr/bin/env python3

from pathlib import Path
import re

src = Path("../urdf/me6_robot_original.xacro")
dst = Path("../urdf/me6_macro.xacro")

text = src.read_text()

# Remove xml declaration
text = re.sub(r"<\?xml.*?\?>", "", text, flags=re.S)

# Remove world and dummy
text = re.sub(r'<link name="dummy_link".*?/>', "", text, flags=re.S)
text = re.sub(r'<link name="world".*?/>', "", text, flags=re.S)
text = re.sub(r'<joint name="world_joint".*?</joint>', "", text, flags=re.S)
text = re.sub(r'<joint name="dummy_joint".*?</joint>', "", text, flags=re.S)

# Remove gazebo
text = re.sub(r"<gazebo.*?</gazebo>", "", text, flags=re.S)

# Remove ros2_control
text = re.sub(r"<ros2_control.*?</ros2_control>", "", text, flags=re.S)

# Rename robot
text = text.replace(
    '<robot name="me6_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">',
    '<robot xmlns:xacro="http://www.ros.org/wiki/xacro">\n'
    '<xacro:macro name="me6_arm" params="parent_link xyz:=\'0 0 0\' rpy:=\'0 0 0\'">'
)

# Rename links
link_names = [
    "base_link",
    "Link1",
    "Link2",
    "Link3",
    "Link4",
    "Link5",
    "Link6",
]

for link in link_names:
    text = text.replace(f'"{link}"', f'"me6_{link}"')

# Mount joint
mount = """
<joint name="me6_mount_joint" type="fixed">
  <parent link="${parent_link}"/>
  <child link="me6_base_link"/>
  <origin xyz="${xyz}" rpy="${rpy}"/>
</joint>

"""

text = text.replace(
    '<link name="me6_base_link">',
    mount + '<link name="me6_base_link">',
    1
)

# Close macro
text = text.replace(
    "</robot>",
    "</xacro:macro>\n</robot>"
)

dst.write_text(text)

print("Done")
