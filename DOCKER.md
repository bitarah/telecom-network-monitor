# Docker Setup Guide

This project is fully containerized using Docker and Docker Compose for easy deployment.

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌─────────────┐    ┌─────────────┐   │
│  │  Frontend   │    │   Backend   │   │
│  │   (React)   │    │  (Gradio)   │   │
│  │             │    │             │   │
│  │ Port: 5173  │    │ Port: 7860  │   │
│  └─────────────┘    └─────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## Services

### Frontend
- **Container Name:** `5g-network-frontend`
- **Base Image:** `node:18-alpine`
- **Port:** 5173
- **URL:** http://localhost:5173
- **Description:** React + Vite dashboard with real-time network visualizations

### Backend
- **Container Name:** `5g-network-backend`
- **Base Image:** `python:3.9-slim`
- **Port:** 7860
- **URL:** http://localhost:7860
- **Description:** Gradio ML analytics app with anomaly detection and classification models

## Quick Commands

### Start Everything
```bash
./start.sh
```
- Builds images if needed
- Starts frontend in detached mode (background)
- Starts backend in attached mode (shows logs)

### Stop Everything
```bash
./stop.sh
```
- Gracefully stops all containers
- Preserves data and volumes

### View Logs
```bash
# Frontend logs
docker-compose logs frontend

# Backend logs (if running detached)
docker-compose logs -f backend

# All logs
docker-compose logs -f
```

### Rebuild Containers
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build frontend
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

### Access Container Shell
```bash
# Frontend container
docker exec -it 5g-network-frontend sh

# Backend container
docker exec -it 5g-network-backend bash
```

## Advanced Usage

### Run Backend in Detached Mode
If you prefer both containers running in background:

```bash
docker-compose up -d
```

To view logs:
```bash
docker-compose logs -f backend
```

### Custom Port Mapping
Edit `docker-compose.yml` to change ports:

```yaml
services:
  frontend:
    ports:
      - "3000:5173"  # Access on port 3000 instead

  backend:
    ports:
      - "8080:7860"  # Access on port 8080 instead
```

### Development Mode with Hot Reload

Both services support hot reload:
- **Frontend:** Edit files in `./frontend/src` - changes reflect immediately
- **Backend:** Edit `./gradio-app/app.py` - Gradio auto-reloads

### Clean Up Everything
```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes (⚠️ deletes data)
docker-compose down -v

# Remove all images
docker-compose down --rmi all
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5173 or 7860
lsof -i :5173
lsof -i :7860

# Kill the process or change ports in docker-compose.yml
```

### Containers Won't Start
```bash
# Check Docker is running
docker info

# View detailed logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Models Not Found Error
The backend requires ML models to be trained first:

```bash
# On host machine (not in container)
source venv/bin/activate
python ml/anomaly_detector.py
python ml/coverage_classifier.py
```

Models are stored in `./ml/models/` and mounted to the container.

### Permission Issues (Linux)
```bash
# Fix permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo ./start.sh
```

## Production Deployment

For production, create a separate `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      target: production
    ports:
      - "80:80"
    restart: always

  backend:
    build:
      context: .
      dockerfile: gradio-app/Dockerfile
    ports:
      - "7860:7860"
    restart: always
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Frontend
VITE_API_URL=http://localhost:7860

# Backend
PYTHONUNBUFFERED=1
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## Health Checks

Check if services are running:

```bash
# List running containers
docker-compose ps

# Check container health
docker inspect 5g-network-frontend | grep Status
docker inspect 5g-network-backend | grep Status

# Test endpoints
curl http://localhost:5173
curl http://localhost:7860
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Gradio Docker Guide](https://gradio.app/guides/deploying-gradio-with-docker/)
