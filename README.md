# da_maestro
DA Maestro generates for you Purchase Order Requests in excel format by reading your quotation document


# DA Maestro: Generate Purchase Order Requests in excel format

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

**DA Maestro** is a web application built with Python and Shiny that simplifies the creation of Purchase Order Requests. It leverages AI (Gemini or Pixtral models) to automatically extract data from quotations, validates the provided information and generate a formatted Excel file.

## Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Key Features

-   **AI-Powered Data Extraction:** Utilizes either the Gemini or Pixtral AI models to automatically extract key information (provider details, item descriptions, prices, quantities, etc.) from PNG images of quotations.
-   **User-Friendly Interface:** Provides a web-based interface (built with Shiny) for seamless interaction.
-   **Data Validation:** Validates the extracted data and user inputs to ensure the accuracy and completeness of the Purchase Order Request.
-   **Excel Export:** Generates a fully formatted Excel file (.xlsx) based on a predefined template, ready to be shared and processed.
-   **Code analytique and spending line:** Helps user to select these elements from a list.
- **File management:** Stores the quotation uploaded.
-   **Customizable AI Models:** Supports multiple AI models (Gemini, Pixtral), allowing flexibility and experimentation.
- **Error handling:** User can visualize validation errors with a modal

## Getting Started

### Prerequisites

Before you begin, ensure you have the python 3 installed on your computer and:

- **Python 3.x:** The project is built using Python.
- **API Keys:** You'll need to configure API keys for the AI models you plan to use (Gemini or Pixtral). These keys are managed in `src/LLM_query`.
- **Excel Template:** You need your specific excel template to be located in `src\ressources\open_template.xlsx`.
 To adapt the code to your specific template, adjust the fields association to your excel cell, listed in xlsx_exporter function. 

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rribault/da_maestro.git
    cd da_maestro    
    ```

2.  **Install your environment, dependencies and the da_maestro package**
    ```bash
    conda create -n da_maestro python=3.12.0
    conda activate da_maestro
    pip install -e .
    ```

### Running the Application

1.  **Run the application:**
    ```bash
    conda activate da_maestro
    python -m shiny run --port 58188 src/app.py 
    ```
2. **Access:** Open your web browser and navigate to the URL provided in the console output (usually `http://127.0.0.1:58188`).

## Usage

1.  **Upload a Quotation:** Use the "Choose PNG File" button to upload a PNG image of a quotation.
2. **Select the IA model:** Choose between gemini or pixtral model.
3.  **Review Extracted Data:** The application will use the selected AI model to extract data, which will be displayed in editable fields.
4.  **Edit and Validate:** Review the extracted data and make any necessary corrections. Fill mandatory field (marked with "OBLIGATOIRE").
5. **Download:** Download the filled excel file by clicking on "create xlsx".

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Acknowledgements:**
The creation of this app was made possible thanks to the use of open source packages, as mentionned in the `setup.py` file.
