"""
Create realistic synthetic network data based on Ookla and 5G dataset schemas
This allows the project to run without requiring large downloads
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Data directories
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def create_synthetic_ookla_data(n_samples=10000):
    """
    Create synthetic network performance data similar to Ookla format

    Schema based on Ookla Open Data:
    - avg_d_kbps: Average download speed (kbps)
    - avg_u_kbps: Average upload speed (kbps)
    - avg_lat_ms: Average latency (ms)
    - tests: Number of tests
    - devices: Number of devices
    - quadkey: Geographic quadkey
    """
    print("🔧 Creating synthetic Ookla-style data...")

    np.random.seed(42)

    # Major cities with different network performance characteristics
    cities = {
        'NYC': {'lat_base': 40.7128, 'lon_base': -74.0060, 'quality': 'high'},
        'LA': {'lat_base': 34.0522, 'lon_base': -118.2437, 'quality': 'high'},
        'Chicago': {'lat_base': 41.8781, 'lon_base': -87.6298, 'quality': 'medium'},
        'Houston': {'lat_base': 29.7604, 'lon_base': -95.3698, 'quality': 'medium'},
        'Rural_TX': {'lat_base': 31.9686, 'lon_base': -99.9018, 'quality': 'low'},
        'Rural_MT': {'lat_base': 46.8797, 'lon_base': -110.3626, 'quality': 'low'},
    }

    data = []
    samples_per_city = n_samples // len(cities)

    for city, props in cities.items():
        for _ in range(samples_per_city):
            # Network quality based on city type
            if props['quality'] == 'high':
                download = np.random.normal(150000, 30000)  # ~150 Mbps
                upload = np.random.normal(50000, 10000)     # ~50 Mbps
                latency = np.random.normal(15, 5)           # ~15 ms
            elif props['quality'] == 'medium':
                download = np.random.normal(80000, 20000)   # ~80 Mbps
                upload = np.random.normal(30000, 8000)      # ~30 Mbps
                latency = np.random.normal(25, 8)           # ~25 ms
            else:  # low
                download = np.random.normal(25000, 10000)   # ~25 Mbps
                upload = np.random.normal(10000, 5000)      # ~10 Mbps
                latency = np.random.normal(45, 15)          # ~45 ms

            # Add some outliers/anomalies (5% of data)
            if np.random.random() < 0.05:
                download *= np.random.uniform(0.1, 0.5)  # Degraded performance
                latency *= np.random.uniform(2, 5)        # High latency

            data.append({
                'tile': f"{city}_{_}",
                'quadkey': str(np.random.randint(1000000, 9999999)),
                'avg_d_kbps': max(1000, download),
                'avg_u_kbps': max(500, upload),
                'avg_lat_ms': max(1, latency),
                'tests': np.random.randint(10, 500),
                'devices': np.random.randint(5, 200),
                'lat': props['lat_base'] + np.random.uniform(-0.5, 0.5),
                'lon': props['lon_base'] + np.random.uniform(-0.5, 0.5),
                'city': city,
                'quality': props['quality']
            })

    df = pd.DataFrame(data)

    # Save to CSV (easier for demo without parquet dependencies)
    output_file = RAW_DATA_DIR / "synthetic_ookla_mobile_tiles.csv"
    df.to_csv(output_file, index=False)

    print(f"✅ Created {len(df)} synthetic Ookla samples")
    print(f"📁 Saved to: {output_file}")
    print(f"\nSummary Statistics:")
    print(f"  Avg Download: {df['avg_d_kbps'].mean()/1000:.1f} Mbps")
    print(f"  Avg Upload: {df['avg_u_kbps'].mean()/1000:.1f} Mbps")
    print(f"  Avg Latency: {df['avg_lat_ms'].mean():.1f} ms")

    return df

def create_synthetic_5g_timeseries(n_samples=50000, days=30):
    """
    Create synthetic 5G network time-series data similar to Irish 5G dataset

    Metrics based on 5G KPIs:
    - RSRP: Reference Signal Received Power (dBm)
    - RSRQ: Reference Signal Received Quality (dB)
    - SINR: Signal-to-Interference-plus-Noise Ratio (dB)
    - CQI: Channel Quality Indicator (0-15)
    - Throughput: Download throughput (Mbps)
    - Latency: Round-trip time (ms)
    """
    print("\n🔧 Creating synthetic 5G time-series data...")

    np.random.seed(42)

    # Generate timestamps over 30 days
    start_date = datetime.now() - timedelta(days=days)
    timestamps = [start_date + timedelta(seconds=x) for x in range(n_samples)]

    data = []

    for i, ts in enumerate(timestamps):
        # Time-based patterns (worse performance during peak hours)
        hour = ts.hour
        is_peak = 8 <= hour <= 10 or 17 <= hour <= 20

        # Simulate different network scenarios
        scenario = np.random.choice(['excellent', 'good', 'fair', 'poor', 'anomaly'],
                                   p=[0.3, 0.4, 0.2, 0.08, 0.02])

        if scenario == 'excellent':
            rsrp = np.random.normal(-70, 5)
            rsrq = np.random.normal(-8, 2)
            sinr = np.random.normal(20, 3)
            cqi = np.random.randint(12, 16)
            throughput = np.random.normal(800, 100)
            latency = np.random.normal(10, 2)
        elif scenario == 'good':
            rsrp = np.random.normal(-85, 5)
            rsrq = np.random.normal(-11, 2)
            sinr = np.random.normal(15, 3)
            cqi = np.random.randint(9, 13)
            throughput = np.random.normal(400, 80)
            latency = np.random.normal(15, 3)
        elif scenario == 'fair':
            rsrp = np.random.normal(-100, 5)
            rsrq = np.random.normal(-14, 2)
            sinr = np.random.normal(8, 3)
            cqi = np.random.randint(6, 10)
            throughput = np.random.normal(150, 50)
            latency = np.random.normal(25, 5)
        elif scenario == 'poor':
            rsrp = np.random.normal(-115, 5)
            rsrq = np.random.normal(-17, 2)
            sinr = np.random.normal(3, 2)
            cqi = np.random.randint(2, 7)
            throughput = np.random.normal(50, 20)
            latency = np.random.normal(40, 10)
        else:  # anomaly
            rsrp = np.random.normal(-125, 10)
            rsrq = np.random.normal(-20, 3)
            sinr = np.random.normal(-5, 5)
            cqi = np.random.randint(0, 4)
            throughput = np.random.normal(5, 5)
            latency = np.random.normal(200, 50)

        # Peak hour degradation
        if is_peak:
            throughput *= 0.7
            latency *= 1.3

        data.append({
            'timestamp': ts,
            'rsrp_dbm': rsrp,
            'rsrq_db': rsrq,
            'sinr_db': sinr,
            'cqi': int(np.clip(cqi, 0, 15)),
            'throughput_mbps': max(0, throughput),
            'latency_ms': max(1, latency),
            'packet_loss_pct': max(0, np.random.normal(0.5, 0.3) if scenario != 'anomaly' else np.random.normal(5, 2)),
            'scenario': scenario,
            'hour': hour,
            'is_anomaly': 1 if scenario == 'anomaly' else 0
        })

    df = pd.DataFrame(data)

    # Save to CSV (5G dataset format)
    output_file = RAW_DATA_DIR / "synthetic_5g_timeseries.csv"
    df.to_csv(output_file, index=False)

    print(f"✅ Created {len(df)} synthetic 5G samples over {days} days")
    print(f"📁 Saved to: {output_file}")
    print(f"\nSummary Statistics:")
    print(f"  Avg RSRP: {df['rsrp_dbm'].mean():.1f} dBm")
    print(f"  Avg Throughput: {df['throughput_mbps'].mean():.1f} Mbps")
    print(f"  Avg Latency: {df['latency_ms'].mean():.1f} ms")
    print(f"  Anomalies: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.1f}%)")

    return df

if __name__ == "__main__":
    print("=" * 60)
    print("Creating Synthetic Network Data for Demo")
    print("=" * 60)

    # Create both datasets
    ookla_df = create_synthetic_ookla_data(n_samples=10000)
    fiveg_df = create_synthetic_5g_timeseries(n_samples=50000, days=30)

    print("\n" + "=" * 60)
    print("✅ All synthetic data created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Explore the data with notebooks")
    print("2. Build ML models")
    print("3. Create visualizations")
