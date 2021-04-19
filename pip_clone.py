import itertools
import os

if not os.path.exists("output"):
    os.mkdir("output")

with open("requirements.txt", "r") as fp:
    packages = fp.readlines()

    platforms = [
        "manylinux1_x86_64",
        "linux_x86_64",
        "win_amd64",
        "any",
    ]

    python_versions = [
        "35",
        "36",
        "37",
    ]

    implementations = ["cp"]

    for results in itertools.product(
            platforms,
            python_versions,
            implementations,
            packages,
    ):
        platform, python_version, implementation, package = results
        os.system(f'''
    python -m pip download \
    --only-binary=:all: \
    --platform {platform} \
    --python-version {python_version} \
    --implementation {implementation} \
    --abi cp{python_version} \
    --progress-bar off \
    --no-deps\
    -d ./output/\
    {package}

    python -m pip download \
    --only-binary=:all: \
    --platform {platform} \
    --python-version {python_version} \
    --implementation {implementation} \
    --abi cp{python_version}m \
    --progress-bar off \
    --no-deps\
    -d ./output/\
    {package}
    ''')

    for package in packages:
        os.system(f"""
            python -m pip download --only-binary=:all: --abi none --progress-bar off -d ./output/ {package}
            python -m pip download --no-binary=:all: --progress-bar off -d ./output/ {package}
            """)
