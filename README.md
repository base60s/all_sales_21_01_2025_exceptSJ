# Sales Analysis Dashboard

A Streamlit-based dashboard for analyzing sales data across multiple locations.

## Features

- Interactive visualization of sales data
- Multi-location comparison
- Key metrics overview
- Detailed statistical analysis
- Advanced filtering capabilities
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/base60s/all_sales_21_01_2025_exceptSJ.git
cd all_sales_21_01_2025_exceptSJ
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your sales data CSV files in the appropriate location:
   - Files should be named in the format: `sales_analysis_[Location]_[Date]_[Time].csv`
   - Files should be placed in folders named: `extracted_report_[Location]`

2. Run the dashboard:
```bash
streamlit run dashboard.py
```

3. Access the dashboard in your web browser at `http://localhost:8501`

## Data Structure

The dashboard expects CSV files with the following structure:
- Sales data columns
- Location information
- Date and time information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 