from setuptools import find_packages, setup

package_name = 'cam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jose',
    maintainer_email='josesimao@usp.br',
    description='Camera: teste ROS',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'cam_pub = cam.cam_pub_func:main',
        	'cam_sub = cam.cam_sub_func:main',
        	'joy_sub = cam.joy:main',
        ],
    },
)
