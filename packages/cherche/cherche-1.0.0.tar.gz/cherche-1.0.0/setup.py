import setuptools

from cherche.__version__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base_packages = [
    "elasticsearch >= 7.10.0",
    "faiss-cpu >= 1.7.1.post3",
    "flashtext >= 2.7",
    "implicit >= 0.6.1",
    "lunr >= 0.6.1",
    "meilisearch >= 0.22.1",
    "more-itertools >= 9.0.0",
    "numpy >= 1.19.0",
    "pymilvus >= 2.1.3",
    "rank-bm25 == 0.2.1",
    "rapidfuzz >= 1.9.1",
    "river >= 0.8.0",
    "scikit-learn >= 1.0",
    "scipy >= 1.7.3",
    "sentence-transformers >= 2.1.0",
    "transformers >= 4.12.0",
    "tqdm >= 4.62.3",
    "typesense >= 0.14.0",
]

onnx = ["onnx >= 1.10.2", "onnxruntime >= 1.9.0"]

onnxgpu = ["onnx >= 1.10.2", "onnxruntime-gpu >= 1.9.0"]

doc = [
    "numpydoc >= 1.4.0",
    "mkdocs_material >= 8.3.5",
    "mkdocs-awesome-pages-plugin >= 2.7.0",
    "mkdocs-jupyter >= 0.21.0",
]

setuptools.setup(
    name="cherche",
    version=f"{__version__}",
    license="MIT",
    author="Raphael Sourty",
    author_email="raphael.sourty@gmail.com",
    description="Neural Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raphaelsty/cherche",
    download_url="https://github.com/user/cherche/archive/v_01.tar.gz",
    keywords=[
        "neural",
        "search",
        "question",
        "answering",
        "summarization",
        "collaborative filtering",
    ],
    packages=setuptools.find_packages(),
    install_requires=base_packages,
    extras_require={
        "recommend": base_packages,
        "onnx": base_packages + onnx,
        "onnxgpu": base_packages + onnxgpu,
        "doc": base_packages + doc,
    },
    package_data={
        "cherche": ["data/towns.json", "data/semanlink/*.json", "data/norvig.txt"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
