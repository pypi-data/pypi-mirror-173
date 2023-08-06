import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="autobio-tool",
  version="0.1.6",
  author="kaizheng&&haoyuanli",
  author_email="a1242884508@gmail.com",
  description="A tool for prediction of molecules associations",
  url="https://github.com/haohaodaren/autobio-tool.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
