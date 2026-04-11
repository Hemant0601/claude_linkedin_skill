from setuptools import setup, find_packages

setup(
    name="claude-linkedin-skill",
    version="2.0.0",
    description="Claude Code skill for LinkedIn - no developer app needed",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "linkedin-api>=2.2.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedin=linkedin_skill.cli:main",
        ],
    },
)
