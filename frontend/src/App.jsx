import { useState, useEffect } from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { Container, Grid, Paper, Typography, Box, AppBar, Toolbar, IconButton } from '@mui/material';
import { Brightness4, Brightness7, ShowChart, Map, Assessment } from '@mui/icons-material';
import MetricsCards from './components/MetricsCards';
import TimeSeriesChart from './components/TimeSeriesChart';
import HourlyPerformanceChart from './components/HourlyPerformanceChart';
import NetworkMap from './components/NetworkMap';
import ScenarioDistribution from './components/ScenarioDistribution';
import GradioEmbed from './components/GradioEmbed';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [data5g, setData5g] = useState(null);
  const [ooklaData, setOoklaData] = useState(null);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#00b4d8',
      },
      secondary: {
        main: '#f72585',
      },
    },
  });

  useEffect(() => {
    // Load 5G time-series data
    fetch('/5g_timeseries.json')
      .then(res => res.json())
      .then(data => setData5g(data))
      .catch(err => console.error('Error loading 5G data:', err));

    // Load Ookla data
    fetch('/ookla_data.json')
      .then(res => res.json())
      .then(data => setOoklaData(data))
      .catch(err => console.error('Error loading Ookla data:', err));
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <ShowChart sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              5G Network Monitor - ML Analytics Dashboard
            </Typography>
            <IconButton onClick={() => setDarkMode(!darkMode)} color="inherit">
              {darkMode ? <Brightness7 /> : <Brightness4 />}
            </IconButton>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
          {/* Key Metrics */}
          <MetricsCards data5g={data5g} ooklaData={ooklaData} />

          {/* Real-time Performance Charts */}
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} lg={8}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <ShowChart sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Network Performance Over Time
                </Typography>
                <TimeSeriesChart data={data5g} />
              </Paper>
            </Grid>

            <Grid item xs={12} lg={4}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <Assessment sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Scenario Distribution
                </Typography>
                <ScenarioDistribution data={data5g} />
              </Paper>
            </Grid>
          </Grid>

          {/* Hourly Analysis */}
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Hourly Performance Analysis
                </Typography>
                <HourlyPerformanceChart data={data5g} />
              </Paper>
            </Grid>
          </Grid>

          {/* Network Map */}
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <Map sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Geographic Coverage Map
                </Typography>
                <NetworkMap data={ooklaData} />
              </Paper>
            </Grid>
          </Grid>

          {/* Gradio ML App Embed */}
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  🤖 Interactive ML Analytics
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Try the interactive ML models for anomaly detection, coverage classification, and more
                </Typography>
                <GradioEmbed />
              </Paper>
            </Grid>
          </Grid>

          {/* Footer */}
          <Box sx={{ mt: 4, mb: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              5G Network Monitor | ML-Powered Network Analytics | Built with React + TensorFlow
            </Typography>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
