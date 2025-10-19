"""
Download Ookla Open Data from GitHub
Ookla provides global network performance data in Parquet format
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm

# Ookla GitHub repository base URL
OOKLA_BASE_URL = "https://github.com/teamookla/ookla-open-data/raw/master/shapefiles/performance"

# Data directories
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, destination):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(destination, 'wb') as file, tqdm(
        desc=destination.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def download_ookla_data(data_type="mobile", year="2024", quarter="Q1"):
    """
    Download Ookla performance data

    Args:
        data_type: 'mobile' or 'fixed'
        year: Year (e.g., '2024')
        quarter: Quarter (e.g., 'Q1', 'Q2', 'Q3', 'Q4')
    """
    # Construct filename
    # Format: type=mobile/year=2024/quarter=1/2024-01-01_performance_mobile_tiles.parquet
    quarter_num = quarter[1]  # Extract number from 'Q1'

    # Ookla uses the first day of the quarter
    quarter_dates = {'1': '01-01', '2': '04-01', '3': '07-01', '4': '10-01'}
    date_str = f"{year}-{quarter_dates[quarter_num]}"

    filename = f"{date_str}_performance_{data_type}_tiles.parquet"

    # For recent data, try the main repository structure
    # You may need to browse https://github.com/teamookla/ookla-open-data to find exact paths
    print(f"\n📡 Downloading Ookla {data_type.upper()} data for {year} {quarter}...")
    print(f"Filename: {filename}")
    print("\nNote: You may need to manually download from:")
    print("https://github.com/teamookla/ookla-open-data")
    print("or https://registry.opendata.aws/speedtest-global-performance/")

    # Save instructions
    instructions_file = RAW_DATA_DIR / "DOWNLOAD_INSTRUCTIONS.txt"
    with open(instructions_file, 'w') as f:
        f.write("Ookla Open Data Download Instructions\n")
        f.write("=" * 50 + "\n\n")
        f.write("Option 1: GitHub\n")
        f.write("1. Visit: https://github.com/teamookla/ookla-open-data\n")
        f.write("2. Navigate to: shapefiles/performance/type=mobile/\n")
        f.write("3. Download recent quarter parquet files\n\n")
        f.write("Option 2: AWS Registry\n")
        f.write("1. Visit: https://registry.opendata.aws/speedtest-global-performance/\n")
        f.write("2. Use AWS CLI:\n")
        f.write("   aws s3 ls s3://ookla-open-data/parquet/performance/\n")
        f.write("   aws s3 cp s3://ookla-open-data/parquet/performance/type=mobile/year=2024/ ./data/raw/ --recursive\n\n")
        f.write("Option 3: Sample Data (Recommended for Demo)\n")
        f.write("We'll create synthetic data based on Ookla's schema for demonstration\n")

    print(f"\n✅ Instructions saved to: {instructions_file}")
    return instructions_file

if __name__ == "__main__":
    download_ookla_data(data_type="mobile", year="2024", quarter="Q1")
    print("\n💡 For quick demo, we'll create synthetic data in the next step")
