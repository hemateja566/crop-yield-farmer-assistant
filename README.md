# Crop Yield & Farmer Advisory Assistant

A full-stack AgriTech application providing crop yield predictions and AI-powered farmer advisory services.

## Project Structure

```
crop-yield-farmer-assistant/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py       # Main FastAPI application
│   │   ├── config.py     # Configuration settings
│   │   ├── routes/       # API route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic services
│   │   ├── ml/           # Machine learning pipeline
│   │   └── rag/          # RAG chatbot components
│   └── data/             # Data directory
├── frontend/             # React + Vite + Tailwind frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── dashboard/    # Farmer dashboard
│   │   ├── chatbot/      # AI chatbot interface
│   │   └── services/     # API services
│   └── package.json
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Local development setup
└── README.md            # This file
```

## Features

### 1. Farmer Registration & Farm Management
- Register farmer profiles with name, language, and location
- Register farm details including area, soil type, irrigation, and crop selection
- View farm history and crop records

### 2. Crop Yield Prediction
- Machine learning predictions using Random Forest and XGBoost
- Input features: soil NPK, pH, temperature, rainfall, humidity, area
- Confidence intervals with calibrated uncertainty ranges
- Model evaluation: MAE, RMSE, R² score

### 3. AI Farmer Advisory Chatbot (RAG)
- Retrieval-Augmented Generation with FAISS vector search
- LangChain-based retrieval pipeline
- Sentence Transformers embeddings (all-MiniLM-L6-v2)
- Agriculture knowledge base with crop guides, fertilizer recommendations, irrigation practices, and pest/disease management
- Multilingual support: English, Telugu, Hindi
- Source-cited responses for verified advice

### 4. Dashboard
- Farm overview and summaries
- Yield prediction results with confidence intervals
- Weather forecast integration (Open-Meteo API)
- Soil health indicators
- Previous prediction history
- AI chatbot integration

### 5. External API Integrations
- **Weather**: Open-Meteo API for forecasts and historical data
- **Soil**: SoilGrids API for soil property information (pH, NPK, texture)
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for session caching and background tasks

## Technology Stack

### Frontend
- React + Vite + Tailwind CSS
- Recharts for data visualizations
- Axios for API requests
- React Router for navigation

### Backend
- Python + FastAPI
- REST APIs with automatic Swagger documentation
- Pydantic validation
- SQLAlchemy ORM
- JWT authentication (planned)
- Background tasks

### Machine Learning
- Pandas + NumPy for data processing
- Scikit-learn (Random Forest Regressor)
- XGBoost Regressor
- Model evaluation: MAE, RMSE, R², MAPE

### Generative AI / RAG
- LangChain for retrieval pipeline
- FAISS vector database
- Sentence Transformers embeddings
- Hugging Face models
- RAG-based agronomy knowledge base

### Database & Infrastructure
- PostgreSQL: farmers, farms, predictions
- Redis: caching and background job support
- Docker: containerization
- GitHub Actions: CI/CD (configuration ready)

### External APIs
- Open-Meteo: Weather forecasts and historical data
- SoilGrids: Soil property information
- NASA POWER: Alternative weather data source

## Development Roadmap

### Week 1: Dataset and ML
- Find and load agricultural yield datasets
- Clean data using Pandas
- Train Random Forest and XGBoost models
- Evaluate MAE, RMSE, and R²
- Save the best model (.pkl)

### Week 2: Backend and Integrations
- Create FastAPI application
- Connect PostgreSQL database
- Integrate weather and soil APIs
- Create yield prediction endpoints
- Test APIs using Swagger/Postman

### Week 3: RAG Chatbot
- Collect agricultural documents
- Build document ingestion pipeline
- Generate embeddings with Sentence Transformers
- Store embeddings in FAISS
- Implement LangChain chatbot
- Add Telugu and English support

### Week 4: Frontend and Deployment
- Build React dashboard
- Integrate prediction API
- Add chatbot interface
- Display weather and yield charts
- Dockerize and deploy
- Test complete application

## API Endpoints

| Endpoint | Purpose |
| --- | --- |
| `POST /auth/register` | Farmer registration |
| `POST /auth/login` | User authentication |
| `POST /farms/` | Register farm details |
| `GET /farms/{id}` | Retrieve farm information |
| `GET /weather/{farm_id}` | Get weather information |
| `POST /predict/yield` | Generate crop yield prediction |
| `GET /predict/history` | Previous predictions |
| `POST /chat/ask` | Ask AI farmer assistant |
| `GET /advisory/{farm_id}` | Get personalized crop advice |
| `GET /crops` | Retrieve supported crops |

## Local Development

1. **Install dependencies**:
   ```bash
   cd crop-yield-farmer-assistant
   pip install -r requirements.txt
   cd frontend && npm install
   ```

2. **Start services**:
   ```bash
   docker-compose up -d  # Starts PostgreSQL and Redis
   ```

3. **Run the backend**:
   ```bash
   cd backend
   uicorn app.main:app --reload
   ```

4. **Run the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

5. **Access the application**:
   - API docs: `http://localhost:8000/docs`
   - Frontend: `http://localhost:3000`

## License

This project is licensed under the MIT License.