import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from agents.code_analyzer import CodeAnalyzer
from agents.test_agent import TestAgent
from agents.devops_agent import DevOpsAgent
from agents.monitor_agent import MonitorAgent

class DevOpsOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        print("🤖 Initializing DevOpsMind System...")
        self.code_analyzer = CodeAnalyzer()
        self.test_agent = TestAgent()
        self.devops_agent = DevOpsAgent()
        self.monitor_agent = MonitorAgent()
        print("✅ All agents ready!")
    
    def process_repository(self, repo_url):
        """Complete pipeline for repository"""
        print("\n" + "="*60)
        print(f"🚀 Starting DevOps pipeline for: {repo_url}")
        print("="*60 + "\n")
        
        # Step 1: Analyze Code
        print("📋 STEP 1: Code Analysis")
        print("-" * 40)
        analysis_result = self.code_analyzer.analyze_repo(repo_url)
        
        if "error" in analysis_result:
            print(f"❌ Error: {analysis_result['error']}")
            return
        
        print(f"📊 Analysis Results:")
        for issue, exists in analysis_result.items():
            status = "⚠️  Missing" if exists else "✅ Present"
            print(f"   {issue}: {status}")
        
        # Step 2: Run Tests
        print("\n🧪 STEP 2: Running Tests")
        print("-" * 40)
        test_results = self.test_agent.run_tests(repo_url)
        
        if "error" in test_results:
            print(f"❌ Error running tests: {test_results['error']}")
        else:
            summary = self.test_agent.get_summary()
            print(f"📊 Test Summary: {summary['status']}")
            print(f"   Passed: {summary['passed']}, Failed: {summary['failed']}, Total: {summary['total']}")
        
        # Step 3: Generate Dockerfile
        print("\n🐳 STEP 3: Generating Dockerfile")
        print("-" * 40)
        dockerfile = self.devops_agent.generate_dockerfile(repo_url, analysis_result)
        print(f"✅ {dockerfile['message']}")
        print(f"   File: {dockerfile['filename']}")
        
        # Step 4: Generate CI/CD Config
        print("\n⚙️ STEP 4: Generating CI/CD Pipeline")
        print("-" * 40)
        cicd_config = self.devops_agent.generate_ci_cd_config(repo_url, test_results)
        print(f"✅ {cicd_config['message']}")
        print(f"   File: {cicd_config['filename']}")
        
        # Step 5: Monitor Deployment
        print("\n📊 STEP 5: Monitoring Deployment")
        print("-" * 40)
        self.monitor_agent.start_monitoring()
        
        deployment_info = {
            "test_results": test_results,
            "dockerfile_generated": True,
            "cicd_generated": True
        }
        
        deployment_status = self.monitor_agent.check_deployment(deployment_info)
        
        print(f"\n📈 Deployment Status: {deployment_status['status'].upper()}")
        if deployment_status['errors']:
            print(f"⚠️ Issues found: {deployment_status['errors']}")
        
        # Final Summary
        print("\n" + "="*60)
        print("📋 FINAL SUMMARY")
        print("="*60)
        
        print("\n📁 Generated Files:")
        print(f"   1. {dockerfile['filename']}")
        print(f"   2. {cicd_config['filename']}")
        
        print("\n📊 Test Results:")
        print(f"   {summary['status']}")
        
        print("\n📈 Monitoring Summary:")
        monitor_summary = self.monitor_agent.get_summary()
        print(f"   Status: {monitor_summary['deployment_status']}")
        print(f"   Duration: {monitor_summary['duration']}")
        
        # Save generated files
        self._save_generated_files(dockerfile, cicd_config)
        
        print("\n✅ Pipeline complete! Check the 'generated_files' folder for outputs.\n")
        
        return {
            "analysis": analysis_result,
            "tests": test_results,
            "dockerfile": dockerfile,
            "cicd": cicd_config,
            "monitoring": deployment_status
        }
    
    def _save_generated_files(self, dockerfile, cicd_config):
        """Save generated files to disk"""
        output_dir = Path("generated_files")
        output_dir.mkdir(exist_ok=True)
        
        # Save Dockerfile
        docker_path = output_dir / dockerfile['filename']
        with open(docker_path, 'w') as f:
            f.write(dockerfile['content'])
        print(f"\n💾 Saved: {docker_path}")
        
        # Save CI/CD config
        cicd_path = output_dir / cicd_config['filename']
        cicd_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cicd_path, 'w') as f:
            f.write(cicd_config['content'])
        print(f"💾 Saved: {cicd_path}")

def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════╗
    ║       DevOpsMind - AI DevOps          ║
    ║    Automated Deployment Pipeline      ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Get repository URL from user
    repo_url = input("Enter GitHub repository URL: ").strip()
    
    if not repo_url:
        print("❌ Please enter a valid repository URL")
        return
    
    # Run orchestrator
    orchestrator = DevOpsOrchestrator()
    result = orchestrator.process_repository(repo_url)
    
    if result:
        print("\n🎉 DevOpsMind execution completed successfully!")

if __name__ == "__main__":
    main()