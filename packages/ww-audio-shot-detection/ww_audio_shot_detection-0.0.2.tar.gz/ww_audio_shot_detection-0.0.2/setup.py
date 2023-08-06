from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='ww_audio_shot_detection',
    version='0.0.2',
    author='wingwarp',
    description='Package to detect shots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/wingwarp/BallTracking',
    packages=['ww_audio_shot_detection', 'ww_audio_shot_detection.utils'],
    install_requires=[
        'requests', 'matplotlib', 'pandas', 'boto3', 'm3u8', 'aiohttp', 'imutils'
    ],
)