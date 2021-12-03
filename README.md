# VulScrape

## About The Project

VulScrape is a vulnerability detection & prediction tool for forecasting exploits of common vulnerabilities found in source code written in C/C++. The tool is created as a Google Chrome extension for ease of use. 

This project is inspired by the works of *[Li, Zhen, et al. (2021)](https://ieeexplore.ieee.org/abstract/document/9321538)* & *[Fang, Yong, et al. (2020)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0228439)*. The web extension integrates the vulnerability detection methodology from  *Li, Zhen, et al. (2018)* where they used a deep neural network to detect code vulnerabilities and exploit prediction methodology from *Fang, Yong, et al. (2020)*'s ensemble machine learning algorithm.

All vulnerabilities that can be detected by VulScrape are listed under the [National Vulnerability Database](https://nvd.nist.gov/)'s CVE *[listing](https://nvd.nist.gov/vuln/full-listing)*.

## Built With

This section describes the essential packages and frameworks used for the project.

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Django 3.1](https://www.djangoproject.com/download/)
- [Joern 0.3](https://joern.io/)
- [Neo4j 2.1.8](https://community.chocolatey.org/packages/neo4j-community/2.1.8.20150617#dependencies)
- [TensorFlow 1.14](https://github.com/tensorflow/tensorflow/releases/tag/v1.14.0-rc1)
- [Gensim 3.8.3](https://pypi.org/project/gensim/3.8.3/)
- [PostgreSQL](https://www.postgresql.org/)
- [React](https://reactjs.org/)
- [Material-UI](https://mui.com/)


## Getting Started
### Installation

1. Download the compressed extension from [here](https://github.com/Saleh-Ibtasham/VulScrape/releases/tag/add-on).
2. Extract the extension with [WinRAR](https://www.win-rar.com/start.html?&L=0) or [7zip](https://www.7-zip.org/).
3. Load the extension from Google Chrome's manage extensions option.
4. Clone the project repo
    > `git clone https://github.com/Saleh-Ibtasham/VulScrape.git`

### Usage
1. Specify the ".joernIndex" folder in joern
2. Turn on Joern and Neo4j database locally
3. Run the downloaded Django project repo in the background
4. Open the extension in Google Chrome

    *For detailed extension instructions, please refer to the user manual section at the end of the [Documentation](https://github.com/Saleh-Ibtasham/VulScrape/blob/master/VuleScrape_documentation.pdf)*

### Acknowledgements
Included here are the projects that inspired this work:

1. [SySeVR](https://github.com/SySeVR/SySeVR)
2. [VulDeePecker](https://github.com/CGCL-codes/VulDeePecker)