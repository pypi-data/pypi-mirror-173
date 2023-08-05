from distutils.core import setup

setup(
    name="bunkatopics",
    packages=["bunkatopics"],
    version="0.25",
    license="MIT",
    description="Advanced Topic Modeling Using Transformers",
    author="Charles de Dampierre",
    author_email="charles.de-dampierre@hec.edu",
    url="https://github.com/charlesdedampierre/BunkaTopics",
    download_url="https://github.com/charlesdedampierre/BunkaTopics/archive/v_01.tar.gz",
    keywords=[
        "Topic Modeling",
        "NLP",
        "Search",
    ],
    install_requires=[
        "pandas",
        "scikit_learn",
        "sentence_transformers",
        "textacy",
        "tqdm",
        "umap-learn",
        "hdbscan",
        # "spacy== 3.2.3",
        # "en_core_web_sm",
        # "fr_core_news_lg",
        "plotly"
        # "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz",
    ],
    # dependency_links=[
    # "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz#egg=en_core_web_sm"
    # ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
