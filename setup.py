import lifesospy_mqtt.const as mqtt_const

from setuptools import setup

setup(
    name=mqtt_const.PROJECT_NAME,
    description=mqtt_const.PROJECT_DESCRIPTION,
    version=mqtt_const.PROJECT_VERSION,
    packages=['lifesospy_mqtt'],
    install_requires=[
        'lifesospy~=0.7.4',
        'hbmqtt~=0.9.2',
        'pyyaml~=3.13',
        'python-dateutil~=2.7.3'],
    python_requires='>=3.5.3',
    author='Richard Orr',
    url='https://github.com/rorr73/lifesospy_mqtt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
