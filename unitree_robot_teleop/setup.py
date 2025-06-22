from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'unitree_robot_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        (os.path.join('share', package_name, 'rviz'), 
            glob(os.path.join('rviz', '*.rviz'))),
        
        (os.path.join('share', package_name, 'launch'), 
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=[
        'setuptools',
        'pinocchio',  # 添加 Pinocchio 依赖
    ],
    zip_safe=True,
    maintainer='rundong',
    maintainer_email='rundong@todo.todo',
    description='Teleoperation package for Unitree robots',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'interactive_marker_node = unitree_robot_teleop.interactive_marker:main',
            'robot_control_node = unitree_robot_teleop.robot_control:main',
        ],
    },
)