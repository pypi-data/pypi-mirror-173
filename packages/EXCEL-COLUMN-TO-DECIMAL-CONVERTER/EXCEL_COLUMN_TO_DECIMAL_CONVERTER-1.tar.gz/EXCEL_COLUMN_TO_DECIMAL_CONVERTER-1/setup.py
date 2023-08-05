from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='EXCEL_COLUMN_TO_DECIMAL_CONVERTER',
    version='1',
    packages=['EXCEL_COLUMN_TO_DECIMAL_CONVERTER'],
    url='https://github.com/GlobalCreativeApkDev/GlobalCreativeApkDev.github.io/tree/main/programming-libraries/EXCEL_COLUMN_TO_DECIMAL_CONVERTER',
    license='MIT',
    author='GlobalCreativeApkDev',
    author_email='globalcreativeapkdev2022@gmail.com',
    description='This library is a simple library to convert Excel column to decimal.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "EXCEL_COLUMN_TO_DECIMAL_CONVERTER=EXCEL_COLUMN_TO_DECIMAL_CONVERTER.excel_column_to_decimal_converter:main",
        ]
    }
)