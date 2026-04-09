from setuptools import setup, find_packages

setup(
    name="carefusion_ai",            # must match folder name
    version="0.1.0",
    author="RAJ",
    packages=find_packages("src"),   # tell setuptools to look inside src/
    package_dir={"": "src"},         # map root to src/
)
