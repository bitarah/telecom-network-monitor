import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function HourlyPerformanceChart({ data }) {
  if (!data) return <div>Loading...</div>;

  const chartData = {
    labels: data.hourly.map(d => `${d.hour}:00`),
    datasets: [
      {
        label: 'Avg Throughput (Mbps)',
        data: data.hourly.map(d => d.throughput_mbps_mean),
        backgroundColor: 'rgba(0, 180, 216, 0.7)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Network Performance by Hour of Day' },
    },
  };

  return <Bar data={chartData} options={options} height={60} />;
}
