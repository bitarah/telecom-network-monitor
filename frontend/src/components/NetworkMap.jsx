import { Box, Typography } from '@mui/material';

export default function NetworkMap({ data }) {
  if (!data) return <div>Loading...</div>;

  return (
    <Box sx={{ p: 2, textAlign: 'center' }}>
      <Typography variant="body1" gutterBottom>
        Geographic coverage data for {data.summary.length} cities
      </Typography>
      <Box sx={{ mt: 2, p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
        {data.summary.map((city, idx) => (
          <Box key={idx} sx={{ mb: 1, textAlign: 'left' }}>
            <Typography variant="subtitle2">
              📍 {city.city}: {(city.avg_d_kbps / 1000).toFixed(1)} Mbps ↓ | {(city.avg_u_kbps / 1000).toFixed(1)} Mbps ↑ | {city.avg_lat_ms.toFixed(0)} ms
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
}
