import { Box, Typography, Button } from '@mui/material';
import { OpenInNew } from '@mui/icons-material';

export default function GradioEmbed() {
  // Placeholder for Gradio embedding
  // Once deployed to HuggingFace, replace with actual URL
  const gradioUrl = 'https://huggingface.co/spaces/YOUR-USERNAME/5g-network-ml';

  return (
    <Box sx={{ p: 3, textAlign: 'center', border: '2px dashed', borderRadius: 2, borderColor: 'primary.main' }}>
      <Typography variant="h6" gutterBottom>
        🤖 Interactive ML Models
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        The Gradio app provides interactive ML-powered analytics:
      </Typography>
      <ul style={{ textAlign: 'left', display: 'inline-block' }}>
        <li>Anomaly Detection with Isolation Forest</li>
        <li>Coverage Quality Classification</li>
        <li>Real-time Network Analysis</li>
      </ul>
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          startIcon={<OpenInNew />}
          href={gradioUrl}
          target="_blank"
          disabled
        >
          Launch ML Analytics App
        </Button>
        <Typography variant="caption" display="block" sx={{ mt: 1 }}>
          (Deploy to HuggingFace Spaces to activate)
        </Typography>
      </Box>
    </Box>
  );
}
