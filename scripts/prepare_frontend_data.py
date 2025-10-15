"""
Prepare data for frontend React app
Converts CSV data to JSON format optimized for visualization
"""

import pandas as pd
import json
from pathlib import Path

# Paths
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
FRONTEND_PUBLIC = Path(__file__).parent.parent / "frontend" / "public"
FRONTEND_PUBLIC.mkdir(parents=True, exist_ok=True)

def prepare_ookla_data():
    """Prepare Ookla data for geographic visualization"""
    print("📊 Preparing Ookla data...")

    df = pd.read_csv(RAW_DATA_DIR / "synthetic_ookla_mobile_tiles.csv")

    # Aggregate by city for summary view
    city_summary = df.groupby('city').agg({
        'avg_d_kbps': 'mean',
        'avg_u_kbps': 'mean',
        'avg_lat_ms': 'mean',
        'tests': 'sum',
        'lat': 'mean',
        'lon': 'mean',
        'quality': lambda x: x.mode()[0] if len(x) > 0 else 'unknown'
    }).reset_index()

    # Convert to JSON
    city_data = city_summary.to_dict('records')

    # Sample individual tiles (for detailed view)
    sample_tiles = df.sample(n=min(500, len(df))).to_dict('records')

    output = {
        'summary': city_data,
        'tiles': sample_tiles,
        'stats': {
            'total_tests': int(df['tests'].sum()),
            'avg_download_mbps': float(df['avg_d_kbps'].mean() / 1000),
            'avg_upload_mbps': float(df['avg_u_kbps'].mean() / 1000),
            'avg_latency_ms': float(df['avg_lat_ms'].mean())
        }
    }

    # Save
    output_path = FRONTEND_PUBLIC / "ookla_data.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved Ookla data to {output_path}")
    return output


def prepare_5g_timeseries():
    """Prepare 5G time-series data for charts"""
    print("\n📊 Preparing 5G time-series data...")

    df = pd.read_csv(RAW_DATA_DIR / "synthetic_5g_timeseries.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sample every 100th point for performance (500 points total)
    df_sampled = df.iloc[::100].copy()

    # Convert to JSON-friendly format
    df_sampled['timestamp'] = df_sampled['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    time_series_data = df_sampled[['timestamp', 'throughput_mbps', 'latency_ms',
                                   'rsrp_dbm', 'rsrq_db', 'sinr_db', 'cqi',
                                   'packet_loss_pct', 'scenario']].to_dict('records')

    # Hourly aggregation for summary
    df['hour'] = df['timestamp'].dt.hour
    hourly_stats = df.groupby('hour').agg({
        'throughput_mbps': ['mean', 'std'],
        'latency_ms': ['mean', 'std'],
        'packet_loss_pct': 'mean'
    }).reset_index()

    hourly_stats.columns = ['_'.join(col).strip('_') for col in hourly_stats.columns.values]
    hourly_data = hourly_stats.to_dict('records')

    # Scenario distribution
    scenario_counts = df['scenario'].value_counts().to_dict()

    output = {
        'timeseries': time_series_data,
        'hourly': hourly_data,
        'scenarios': scenario_counts,
        'stats': {
            'total_samples': len(df),
            'avg_throughput_mbps': float(df['throughput_mbps'].mean()),
            'avg_latency_ms': float(df['latency_ms'].mean()),
            'avg_rsrp_dbm': float(df['rsrp_dbm'].mean()),
            'anomaly_rate': float(df['is_anomaly'].mean() * 100) if 'is_anomaly' in df.columns else 0
        }
    }

    # Save
    output_path = FRONTEND_PUBLIC / "5g_timeseries.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved 5G data to {output_path}")
    return output


if __name__ == "__main__":
    print("=" * 60)
    print("Preparing Frontend Data")
    print("=" * 60)

    ookla_data = prepare_ookla_data()
    fiveg_data = prepare_5g_timeseries()

    print("\n" + "=" * 60)
    print("✅ All frontend data prepared!")
    print("=" * 60)
    print("\nData files created:")
    print(f"  - ookla_data.json ({len(ookla_data['tiles'])} tiles)")
    print(f"  - 5g_timeseries.json ({len(fiveg_data['timeseries'])} time points)")
