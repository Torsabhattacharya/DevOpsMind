import time
import json
from datetime import datetime
from pathlib import Path
import re

class MonitorAgent:
    """Monitors logs, deployment status, and system health"""
    
    def __init__(self):
        self.logs = []
        self.deployment_status = {
            "status": "pending",
            "start_time": None,
            "end_time": None,
            "errors": []
        }
    
    def start_monitoring(self):
        """Start monitoring session"""
        print("📊 Starting monitoring session...")
        self.deployment_status["start_time"] = datetime.now().isoformat()
        self.deployment_status["status"] = "running"
        self._log("INFO", "Monitoring session started")
    
    def check_deployment(self, deployment_info):
        """Check deployment status"""
        print("🔍 Checking deployment status...")
        
        # Simulate checking various deployment aspects
        checks = {
            "docker_build": self._check_docker_build(),
            "tests_passed": self._check_test_status(deployment_info),
            "service_health": self._check_service_health(),
            "logs_analysis": self._analyze_logs()
        }
        
        # Determine overall status
        failed_checks = [k for k, v in checks.items() if v is False]
        
        if failed_checks:
            self.deployment_status["status"] = "failed"
            self.deployment_status["errors"] = failed_checks
            self._log("ERROR", f"Deployment failed: {failed_checks}")
        else:
            self.deployment_status["status"] = "successful"
            self._log("INFO", "Deployment successful!")
        
        self.deployment_status["end_time"] = datetime.now().isoformat()
        
        return {
            "status": self.deployment_status["status"],
            "checks": checks,
            "errors": self.deployment_status["errors"],
            "start_time": self.deployment_status["start_time"],
            "end_time": self.deployment_status["end_time"]
        }
    
    def _check_docker_build(self):
        """Check if Docker build would succeed"""
        # Simulate Docker build check
        self._log("INFO", "Checking Docker build configuration...")
        return True  # Assume success for now
    
    def _check_test_status(self, deployment_info):
        """Check if all tests passed"""
        test_results = deployment_info.get("test_results", {})
        failed_count = test_results.get("failed", 0)
        
        if failed_count == 0:
            self._log("INFO", "All tests passed")
            return True
        else:
            self._log("WARNING", f"{failed_count} tests failed")
            return False
    
    def _check_service_health(self):
        """Check if service is healthy"""
        self._log("INFO", "Checking service health...")
        # In real scenario, this would ping the deployed service
        return True
    
    def _analyze_logs(self):
        """Analyze logs for errors"""
        error_patterns = ["error", "exception", "failed", "crash"]
        
        # Check recent logs for errors
        errors_found = []
        for log in self.logs[-20:]:  # Last 20 logs
            if any(pattern in log["message"].lower() for pattern in error_patterns):
                errors_found.append(log)
        
        if errors_found:
            self._log("WARNING", f"Found {len(errors_found)} errors in logs")
            return False
        
        return True
    
    def _log(self, level, message):
        """Internal logging"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.logs.append(log_entry)
        print(f"[{level}] {message}")
    
    def get_logs(self, last_n=None):
        """Get all or recent logs"""
        if last_n:
            return self.logs[-last_n:]
        return self.logs
    
    def get_summary(self):
        """Get monitoring summary"""
        return {
            "deployment_status": self.deployment_status["status"],
            "total_logs": len(self.logs),
            "errors_count": len([l for l in self.logs if l["level"] == "ERROR"]),
            "warnings_count": len([l for l in self.logs if l["level"] == "WARNING"]),
            "duration": self._get_duration()
        }
    
    def _get_duration(self):
        """Calculate deployment duration"""
        if self.deployment_status["start_time"] and self.deployment_status["end_time"]:
            start = datetime.fromisoformat(self.deployment_status["start_time"])
            end = datetime.fromisoformat(self.deployment_status["end_time"])
            duration = end - start
            return str(duration)
        return "Unknown"