import time
import signal
import sys
from datetime import datetime

class Worker:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
    
    def shutdown(self, signum, frame):
        """Graceful shutdown on SIGTERM/SIGINT"""
        print(f"[{datetime.utcnow().isoformat()}] Shutdown signal received")
        self.running = False
    
    def run(self):
        """Main worker loop"""
        print(f"[{datetime.utcnow().isoformat()}] Worker started")
        
        while self.running:
            print(f"[{datetime.utcnow().isoformat()}] Worker heartbeat - ready for tasks")
            time.sleep(30)
        
        print(f"[{datetime.utcnow().isoformat()}] Worker stopped")
        sys.exit(0)

if __name__ == "__main__":
    worker = Worker()
    worker.run()