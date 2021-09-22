from setuptools import setup

package_name = 'banxter_bridge'

setup(
    name=package_name,
    version='0.9.4',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Riccardo Lastrico',
    author_email='mail@mail.org',
    maintainer='Riccardo Lastrico',
    maintainer_email='mail@mail.org',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Examples of minimal subscribers using rclpy.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'subscriber_old_school = banxter_bridge.subscriber_old_school:main',
            'subscriber_lambda = banxter_bridge.subscriber_lambda:main',
            'subscriber = banxter_bridge.subscriber_member_function:main',
            'publisher = banxter_bridge.publisher_point:main',
            'move_coke = banxter_bridge.move_coke:main',
            'move_coke2 = banxter_bridge.prova1:main',
            'state_machine = banxter_bridge.publisher_point_sm:main',
            'subscriber_state = banxter_bridge.subscriber_state:main',
            'client_gazebo_state = banxter_bridge.repub_pos:main',
            
        ],
    },
)

