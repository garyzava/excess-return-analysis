# Predict “news/events” that lead to an excess return of >5% within 48 hours for certain crypto projects

Predicting the occurrence of news/events that cause an excess return of more than 5% within 48 hours for specific crypto projects: Ethereum and Solana

# Installation
To install this project, follow these steps:

Clone the repository.
Install the necessary dependencies using pip install -r requirements.txt.
Run the project using python main.py.

# Dependencies
This project requires the following dependencies:

* Python 3.7
* Requests
* NumPy
* Pandas
* JSON
* Regex
* Matplotlib
* Seaborn
* SciPy
* Scikit-learn
* Statsmodels (ta-lib)
* GoogleNews (pygooglenews)

# Usage
To use this project, you may use Google Colab, click on the link below

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/garyzava/excess-return-analysis/blob/master/notebook/eda_notebook.ipynb)

## Jupyter Notebooks

If you are not using Colab, run the following commands in a cell before going through the Notebook

```
!pip install numpy
!pip install pandas
!pip install regex
!pip install matplotlib
!pip install seaborn
!pip install scipy
!pip install scikit-learn
%conda install -c conda-forge ta-lib
import talib

#Steps to install pygooglenews
!pip install pygooglenews --no-deps
!pip install feedparser --force
!pip install beautifulsoup4 --force
!pip install dateparser --force
%pip install pygooglenews --no-deps
%pip install feedparser --force
%pip install beautifulsoup4 --force
%pip install dateparser --force
from pygooglenews import GoogleNews
```