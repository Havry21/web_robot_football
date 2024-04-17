from setuptools import find_packages, setup

package_name = 'web_robot_footbot'

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
    maintainer='dima',
    maintainer_email='dimagavrilov2001@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'web = web_robot_footbot.app:main',
            'udpSender = web_robot_footbot.udpSender:main',
        ],
    },
)
