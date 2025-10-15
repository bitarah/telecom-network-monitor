import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import { TrendingUp, Speed, NetworkCheck, SignalCellularAlt } from '@mui/icons-material';

export default function MetricsCards({ data5g, ooklaData }) {
  if (!data5g || !ooklaData) {
    return <Typography>Loading metrics...</Typography>;
  }

  const metrics = [
    {
      title: 'Avg Throughput',
      value: `${data5g.stats.avg_throughput_mbps.toFixed(1)} Mbps`,
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: '#00b4d8'
    },
    {
      title: 'Avg Latency',
      value: `${data5g.stats.avg_latency_ms.toFixed(1)} ms`,
      icon: <Speed sx={{ fontSize: 40 }} />,
      color: '#f72585'
    },
    {
      title: 'Avg RSRP',
      value: `${data5g.stats.avg_rsrp_dbm.toFixed(1)} dBm`,
      icon: <SignalCellularAlt sx={{ fontSize: 40 }} />,
      color: '#4cc9f0'
    },
    {
      title: 'Network Quality',
      value: `${(100 - data5g.stats.anomaly_rate).toFixed(1)}%`,
      icon: <NetworkCheck sx={{ fontSize: 40 }} />,
      color: '#7209b7'
    },
  ];

  return (
    <Grid container spacing={3}>
      {metrics.map((metric, index) => (
        <Grid item xs={12} sm={6} md={3} key={index}>
          <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${metric.color}22, ${metric.color}11)` }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    {metric.title}
                  </Typography>
                  <Typography variant="h4" component="div">
                    {metric.value}
                  </Typography>
                </Box>
                <Box sx={{ color: metric.color }}>
                  {metric.icon}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
