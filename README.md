# PaulTolremLandingPage_prod

# Cryptocurrency Trend Sensing Tool

## Overview

This Django project provides a straightforward and efficient solution for cryptocurrency investors and enthusiasts. It features a High-Low-Open-Close (HLOC) chart for visualizing cryptocurrency price movements and an Artificial Intelligence (AI) tool designed to identify and highlight the most significant market trends present in the limit order book at any given time.

## Features

- **HLOC Chart Visualization**: Offers users the ability to view the high, low, open, and close prices of cryptocurrencies over a selected time frame, aiding in the analysis of market trends.
- **AI Market Trend Sensing**: Utilizes AI algorithms to analyze the limit order book and detect prevailing market trends, helping users make informed decisions based on current market conditions.

## Installation

Ensure you have Python and Django installed on your system. Follow these steps to set up the project:

1. Clone the repository:
   ```
   git clone https://github.com/hitthecodelabs/PaulTolremLandingPage.git
   ```
2. Navigate to the project directory:
   ```
   cd PaulTolremLandingPage
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Django project:
   ```
   python manage.py runserver
   ```
5. Access the web application at `http://127.0.0.1:8000/` in your web browser.

## Usage

- **Viewing the HLOC Chart**: Navigate to the HLOC chart section through the main menu to select a cryptocurrency and time frame for analysis.
- **Trend Sensing with AI**: The AI tool automatically analyzes the limit order book for the selected cryptocurrency and displays the strongest market trend on the dashboard.

## Limitations

- The AI tool's accuracy in sensing market trends is subject to the quality and quantity of the data it analyzes. It is designed to aid decision-making, not replace it.
- Market conditions are highly volatile; users should use this tool as one of several resources in their investment decision process.

## Contributing

We welcome contributions to enhance the project's features or improve its accuracy. Please follow the standard pull request process:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Disclaimer

This project is for educational and research purposes only. We are not responsible for any financial losses incurred through the use of this tool.
