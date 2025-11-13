import mlflow
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set tracking URI
# mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_tracking_uri("http://localhost:5000")

# Create experiment
experiment_name = "test-alphabrain"
try:
    experiment_id = mlflow.create_experiment(experiment_name)
except:
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

# Log a simple run
with mlflow.start_run(experiment_id=experiment_id):
    # Log parameters
    mlflow.log_param("model", "test")
    mlflow.log_param("learning_rate", 0.01)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)
    
    # Log artifact (dummy file)
    with open("test_output.txt", "w") as f:
        f.write("Test artifact from AlphaBrain")
    mlflow.log_artifact("test_output.txt")
    
    print("✅ Experiment logged successfully!")
    print(f"View at: http://localhost:5000/#/experiments/{experiment_id}")