import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function ScenarioDistribution({ data }) {
  if (!data) return <div>Loading...</div>;

  const chartData = {
    labels: Object.keys(data.scenarios),
    datasets: [
      {
        data: Object.values(data.scenarios),
        backgroundColor: [
          'rgba(75, 192, 192, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(153, 102, 255, 0.8)',
        ],
      },
    ],
  };

  return <Pie data={chartData} />;
}
