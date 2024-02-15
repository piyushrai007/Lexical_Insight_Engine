# Text Analysis Tool

## Overview

This is a Python script for performing text analysis on articles extracted from URLs.

## Installation

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/your_username/text-analysis-tool.git
    ```

2. **Install Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare Input**: 
   - Ensure you have an `Input.xlsx` file containing the URLs to extract article text from.

2. **Data Extraction**: 
    - Run the data extraction script:
        ```bash
        python extract_data.py Input.xlsx
        ```

3. **Text Analysis**: 
    - Once the data extraction is complete, run the text analysis script:
        ```bash
        python analyze_text.py
        ```

4. **Output**: 
    - The analyzed data will be saved to an `Output.xlsx` file.

## Requirements

- Python 3.x
- BeautifulSoup4
- NLTK

## File Structure

- `extract_data.py`: Python script to extract article text from URLs.
- `analyze_text.py`: Python script to perform text analysis on the extracted text.
- `requirements.txt`: List of Python dependencies.
- `stop_words/`: Directory containing stop words text files.
- `positive-words.txt`: List of positive words.
- `negative-words.txt`: List of negative words.
- `txt/`: Directory containing extracted text files.
- `Input.xlsx`: Input Excel file containing URLs.
- `Output.xlsx`: Output Excel file containing analyzed data.

## Contributors

- PIYUSH RAI

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
