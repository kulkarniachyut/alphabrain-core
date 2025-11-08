from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="AlphaBrain API",
    version="0.1.0",
    description="Production-grade AI system for financial forecasting"
)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "alphabrain-api",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health():
    """Health check endpoint for load balancers"""
    return {
        "status": "healthy",
        "service": "api",
        "timestamp": datetime.utcnow().isoformat()
    }# Docker CI test
