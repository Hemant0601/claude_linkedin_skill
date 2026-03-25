from setuptools import setup, find_packages

setup(
    name="claude-linkedin-skill",
    version="1.0.0",
    description="Claude Code skill for LinkedIn automation",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedin=linkedin_skill.cli:main",
        ],
    },
)
