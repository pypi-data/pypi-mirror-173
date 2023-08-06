from setuptools import setup, find_packages

version = '0.0.8'

requirements = [
    'numpy',
    'onnxruntime',
    'matplotlib',
    'torch>=1.8',
    'torchvision'   
]

setup(
    name='snapml_auto_quantization',
    version=version,
    packages=find_packages(exclude=['tests*']),
    package_dir={'snapml_auto_quantization':'snapml_auto_quantization'}, 
    package_data={
       'snapml_auto_quantization': ['snapml_auto_quantization/*.onnx', 'snapml_auto_quantization/*.obj'],
    },
    include_package_data=True,
    license='MIT',
    description='A automatic pipeline for SnapML quantization',
    long_description=open('README.md').read(),
    install_requires=requirements,
    python_requires='>=3.6',
    url='https://github.sc-corp.net/Snapchat/snapml_auto_quantization',
    author='Jiazhuo Wang',
    author_email='jwang7@snapchat.com'
)
