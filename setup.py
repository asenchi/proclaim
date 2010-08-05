try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name="proclaim",
    version="0.5",
    description="Conditionally roll out features with Redis",
    long_description="""
    Conditionally roll out features with Redis by assigning
    percentages, groups or users to features. This is a port of jamesgolick's
    rollout: http://github.com/jamesgolick/rollout""",
    author="Curt Micol",
    license="MIT",
    author_email="asenchi@asenchi.com",
    url="http://github.com/asenchi/proclaim",
    download_url="http://github.com/asenchi/proclaim/downloads",
    keywords="redis rollout",
    classifiers = [
        "Development Status :: 5 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Web Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independant",
        "Topic :: Software Development"
    ],
    py_modules=["proclaim"],
)
