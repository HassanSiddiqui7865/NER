# MED7 NER API

Production-ready Medical Named Entity Recognition API using the MED7 model. This API extracts medical entities from clinical text including medications, dosages, frequencies, and more.

## Features

- **FastAPI** - Modern, fast web framework
- **MED7 Model** - Vector-based medical NER model
- **Docker** - Containerized deployment
- **Production Ready** - Health checks, error handling, logging

## Entity Types

The MED7 model extracts the following entity types:

- **DOSAGE**: Medication dosage information
- **DRUG**: Medication names
- **DURATION**: Duration of medication
- **FORM**: Medication form (tablet, capsule, etc.)
- **FREQUENCY**: Frequency of administration
- **ROUTE**: Route of administration
- **STRENGTH**: Medication strength

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker

```bash
# Build the image
docker build -t med7-ner-api .

# Run the container
docker run -d -p 8000:8000 --name med7-api med7-ner-api
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Extract Entities (Single Text)
```bash
POST /extract
Content-Type: application/json

{
  "text": "The patient was prescribed aspirin 100mg twice daily for 7 days."
}
```

**Response:**
```json
{
  "text": "The patient was prescribed aspirin 100mg twice daily for 7 days.",
  "entities": [
    {
      "text": "aspirin",
      "label": "DRUG",
      "start": 32,
      "end": 39
    },
    {
      "text": "100mg",
      "label": "STRENGTH",
      "start": 40,
      "end": 45
    },
    {
      "text": "twice daily",
      "label": "FREQUENCY",
      "start": 46,
      "end": 57
    },
    {
      "text": "7 days",
      "label": "DURATION",
      "start": 62,
      "end": 68
    }
  ],
  "entity_count": 4
}
```

### Extract Entities (Batch)
```bash
POST /extract/batch
Content-Type: application/json

["Text 1", "Text 2", "Text 3"]
```

### API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Usage

### Using curl

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "Take 2 tablets of ibuprofen 200mg every 6 hours for pain."}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/extract",
    json={"text": "Take 2 tablets of ibuprofen 200mg every 6 hours for pain."}
)

print(response.json())
```

## Production Deployment

### Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures Python output is not buffered (already set in Dockerfile)

### Resource Requirements

- **Memory**: Minimum 1GB, Recommended 2GB
- **CPU**: 1+ cores recommended
- **Storage**: ~2GB for model files

### Health Monitoring

The API includes a health check endpoint that can be used with monitoring tools:

```bash
curl http://localhost:8000/health
```

### Scaling

To scale the service:

```bash
docker-compose up -d --scale med7-api=3
```

Note: You'll need a load balancer (nginx, traefik, etc.) to distribute traffic.

## Troubleshooting

### Model Loading Issues

If the model fails to load, check the container logs:

```bash
docker-compose logs med7-api
```

### Port Already in Use

Change the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"  # Use port 8080 instead of 8000
```

## License

This project uses the MED7 model. Please refer to the original MED7 repository for licensing information.
