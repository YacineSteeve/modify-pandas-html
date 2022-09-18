# Modify-Pandas-Html

A Python script that directly downloads Pandas documentation and create a twin directory by replacing each group of text
by a new group of text with a 1 between each element of the string.

## Configuration and run

Preferably, configure a [VirtualEnv](https://docs.python.org/3/tutorial/venv.html) for this.

1. Clone the repository:

    ```commandline
    git clone https://github.com/YacineSteeve/modify-pandas-html
    ```

2. Go to the project directory and install the required packages using pip:

    ```commandline
    cd modify-pandas-html
    pip install -r requirements.txt
    ```
   
3. Start the processing:

    ```commandline
    python main.py
    ```

## Dependencies

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [tqdm](https://tqdm.github.io/)
