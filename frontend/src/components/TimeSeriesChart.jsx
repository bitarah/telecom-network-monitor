import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function TimeSeriesChart({ data }) {
  if (!data) return <div>Loading...</div>;

  const chartData = {
    labels: data.timeseries.map(d => new Date(d.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: 'Throughput (Mbps)',
        data: data.timeseries.map(d => d.throughput_mbps),
        borderColor: 'rgb(0, 180, 216)',
        backgroundColor: 'rgba(0, 180, 216, 0.1)',
        yAxisID: 'y',
      },
      {
        label: 'Latency (ms)',
        data: data.timeseries.map(d => d.latency_ms),
        borderColor: 'rgb(247, 37, 133)',
        backgroundColor: 'rgba(247, 37, 133, 0.1)',
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: { display: true, text: 'Throughput (Mbps)' },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: { display: true, text: 'Latency (ms)' },
        grid: { drawOnChartArea: false },
      },
    },
  };

  return <Line data={chartData} options={options} height={80} />;
}
