from setuptools import find_packages, setup

# Get Packages from Pipfile by parsing them
lines = []
with open("Pipfile", "r") as pipfile:
    lines = pipfile.readlines()
c = [idx for idx, x in enumerate(lines) if x[0] == "["]

# packages index range
packages_sec = [x for x in c if "[packages]" in lines[x]][0]
if c.index(packages_sec) + 1 == len(c):
    packages_end = len(lines)
else:
    packages_end = c[c.index(packages_sec)+1]

# retrieve the packages (except itself)
packages = []
for i in range(packages_sec+1, packages_end):
    if lines[i] == "\n":
        continue
    package = lines[i].split("=")[0].strip()
    if package != "protgraph":
        packages.append(package)

# read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='protgraph',
    version='0.3.8',
    author="Dominik Lux",
    description="ProtGraph, a graph generator for proteins.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpc-bioinformatics/ProtGraph",
    project_urls={
        "Bugs": "https://github.com/mpc-bioinformatics/ProtGraph/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
    ],
    license="BSD",
    python_requires=">=3.6",
    entry_points=dict(console_scripts=[
        'protgraph = protgraph.protgraph:main',
        'protgraph_pepsqlite_to_fasta = protgraph.scripts.pepsqlite_to_fasta:main [sqlite]',
        'protgraph_replace_fasta_header = protgraph.scripts.replace_fasta_header:main',
        'protgraph_generate_fasta_decoys = protgraph.scripts.generate_fasta_decoys:main',
        'protgraph_compact_fasta = protgraph.scripts.compact_fasta:main',
        'protgraph_print_sums = protgraph.scripts.print_sums:main'
    ]),
    packages=find_packages(),
    include_package_data=True,
    install_requires=packages,
    extras_require={
        "postgres": ["psycopg>=3.0"],
        "mysql": ["mysql"],
        "sqlite": ["apsw"],
        "cassandra": ["cassandra-driver"],
        "gremlin": ["gremlinpython"],
        "redis": ["redis", "redisgraph"],
        "full": ["mysql", "psycopg>=3.0", "apsw", "cassandra-driver", "redis", "redisgraph", "gremlinpython"],
    },
)
