# Customer Segmentation System

A professional customer segmentation system using K-Means clustering.

## Architecture

The project follows a modular `src/` layout:

- `src/customer_segmentation/api/`: FastAPI implementation and routes.
- `src/customer_segmentation/core/`: Configuration, schemas, and constants.
- `src/customer_segmentation/services/`: Business logic and model management.
- `src/customer_segmentation/cli/`: Command-line interface.
- `src/customer_segmentation/client.py`: Python client library.

## Getting Started

### Prerequisites

- Python 3.12+
- `uv` (recommended)

### Installation

```bash
uv sync
```

### Running the API

```bash
uv run segmentation-api
```
Or:
```bash
uv run python -m customer_segmentation.api.main
```

### Using the CLI

```bash
uv run segmentation-cli predict 45 50000 500 5 8 6 30
```

## API Documentation

Once the API is running, documentation is available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Model Information

The system uses 4 clusters:
0. **Low-Value**: Low income, low spending.
1. **Premium**: High income, high spending.
2. **Occasional**: Inactive customers.
3. **Active High-Value**: Active, good income/spending.
