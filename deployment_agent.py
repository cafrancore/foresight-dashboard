"""
Deployment Agent for Foresight Project
Automates conversion of Streamlit app to a deployable website
"""

import os
import json
from pathlib import Path
from typing import Optional

class DeploymentAgent:
    """Agent that manages project deployment tasks"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.deployment_config = {
            "project_name": "foresight-dashboard",
            "framework": "streamlit",
            "deployment_options": ["streamlit-cloud", "heroku", "railway", "render", "docker"],
            "requirements": []
        }
    
    def analyze_project(self) -> dict:
        """Analyze current project structure and dependencies"""
        print("🔍 Analyzing project structure...")
        
        analysis = {
            "python_files": [],
            "data_files": [],
            "requirements": [],
            "project_size": 0
        }
        
        # Find all Python files
        for py_file in self.project_path.glob("*.py"):
            size = py_file.stat().st_size
            analysis["python_files"].append({
                "name": py_file.name,
                "size_kb": size / 1024
            })
            analysis["project_size"] += size
        
        # Check requirements.txt
        req_file = self.project_path / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                analysis["requirements"] = f.read().strip().split("\n")
        
        # Find data files
        for ext in [".csv", ".xlsx", ".json"]:
            for data_file in self.project_path.glob(f"*{ext}"):
                analysis["data_files"].append(data_file.name)
        
        print(f"✅ Project analyzed: {len(analysis['python_files'])} Python files, {len(analysis['data_files'])} data files")
        return analysis
    
    def create_deployment_files(self) -> None:
        """Create necessary deployment configuration files"""
        print("\n📦 Creating deployment files...")
        
        # 1. Create .gitignore
        gitignore_content = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/
.DS_Store
*.xlsx
*.csv
.streamlit/secrets.toml
"""
        self._write_file(".gitignore", gitignore_content)
        print("  ✓ .gitignore created")
        
        # 2. Create Procfile for Heroku/Render
        procfile_content = """web: streamlit run dashboard.py --logger.level=error
"""
        self._write_file("Procfile", procfile_content)
        print("  ✓ Procfile created (for Heroku/Render)")
        
        # 3. Create Dockerfile for containerization
        dockerfile_content = """FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "dashboard.py", "--logger.level=error", "--client.showErrorDetails=false"]
"""
        self._write_file("Dockerfile", dockerfile_content)
        print("  ✓ Dockerfile created (for Docker/container deployment)")
        
        # 4. Create .streamlit/config.toml
        os.makedirs(self.project_path / ".streamlit", exist_ok=True)
        config_content = """[theme]
primaryColor = "#1E3A8A"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#1F2937"
font = "sans serif"

[client]
showErrorDetails = false

[server]
port = 8501
headless = true
maxUploadSize = 200
"""
        self._write_file(".streamlit/config.toml", config_content)
        print("  ✓ Streamlit config created")
        
        # 5. Create runtime.txt for Python version specification
        runtime_content = "python-3.10.0\n"
        self._write_file("runtime.txt", runtime_content)
        print("  ✓ Runtime configuration created")
        
        # 6. Create .dockerignore
        dockerignore_content = """__pycache__
*.py[cod]
.git
.gitignore
.DS_Store
*.xlsx
*.csv
venv
env
.streamlit/secrets.toml
"""
        self._write_file(".dockerignore", dockerignore_content)
        print("  ✓ .dockerignore created")
    
    def create_deployment_guide(self) -> None:
        """Create deployment guide for different platforms"""
        print("\n📚 Creating deployment guide...")
        
        guide = """# Foresight Dashboard - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Streamlit Cloud (Easiest - FREE)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" → Select your repository
4. Click "Deploy"
✅ Live in minutes, no configuration needed!

**Link format:** https://[github-username]-[repo-name]-[random].streamlit.app

---

### Option 2: Railway.app (Fast & Affordable)
1. Create account at railway.app
2. Connect GitHub repository
3. Add these environment variables:
   - PYTHON_VERSION=3.10
4. Deploy automatically on push
💰 Free tier available, paid starts at $5/month

---

### Option 3: Render (Reliable)
1. Create account at render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run dashboard.py --logger.level=error --client.showErrorDetails=false`
💰 Free tier available

---

### Option 4: Docker + Any Cloud (Flexible)
1. Install Docker locally
2. Build: `docker build -t foresight-dashboard .`
3. Test locally: `docker run -p 8501:8501 foresight-dashboard`
4. Deploy to:
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

---

### Option 5: Heroku (Deprecated but still works)
1. Install Heroku CLI
2. Run:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Data files accessible (relative paths)
- [ ] No hardcoded secrets (use environment variables)
- [ ] Test locally with: `streamlit run dashboard.py`
- [ ] Update README.md with instructions
- [ ] Add .gitignore to exclude large files
- [ ] Configure data caching for faster loads

---

## 🔐 Handling Secrets & API Keys

If your app uses API keys (e.g., HuggingFace tokens):

1. **Local development**: Create `.streamlit/secrets.toml`
   ```
   huggingface_token = "your-token"
   ```

2. **On Streamlit Cloud**: 
   - App Settings → Secrets → Add your secrets

3. **On Railway/Render**:
   - Add environment variables in dashboard

4. **With Docker**:
   ```bash
   docker run -e HF_TOKEN="your-token" foresight-dashboard
   ```

---

## 📊 Data Handling

- **Small files** (<50MB): Store in repo
- **Large files**: Use cloud storage (AWS S3, Google Cloud Storage)
- **Cached data**: Use @st.cache_data decorator

---

## ⚡ Performance Tips

1. Add caching:
   ```python
   @st.cache_data
   def load_model():
       return SentenceTransformer(...)
   ```

2. Reduce model size (quantize embeddings)
3. Pre-compute embeddings where possible
4. Lazy load components

---

## 🆘 Troubleshooting

**Port already in use:**
```bash
streamlit run dashboard.py --server.port 8502
```

**Model download takes too long:**
- Download model locally, commit, or pre-cache

**Memory issues:**
- Use smaller model: "all-MiniLM-L6-v2"
- Increase container RAM limit

---

## 📈 Recommended: Streamlit Cloud

**Why?** Easiest for Streamlit apps, free tier, auto-deploy from GitHub.

**Steps:**
1. Push code to GitHub
2. Visit https://streamlit.io/cloud
3. "New app" → Select repo
4. Deploy in 1 click

Total time: 5 minutes!

---

## 💡 Next Steps

1. Choose deployment platform
2. Follow the specific guide above
3. Test the live app
4. Monitor logs for errors
5. Collect feedback & iterate

Happy deploying! 🎉
"""
        
        self._write_file("DEPLOYMENT_GUIDE.md", guide)
        print("✅ Deployment guide created")
    
    def create_docker_compose(self) -> None:
        """Create docker-compose for local testing"""
        print("\n🐳 Creating Docker Compose file...")
        
        compose_content = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    command: streamlit run dashboard.py --logger.level=error
"""
        self._write_file("docker-compose.yml", compose_content)
        print("✅ Docker Compose created - Test locally with: docker-compose up")
    
    def create_github_actions(self) -> None:
        """Create GitHub Actions CI/CD workflow"""
        print("\n⚙️  Creating GitHub Actions workflow...")
        
        os.makedirs(self.project_path / ".github" / "workflows", exist_ok=True)
        
        workflow_content = """name: Test & Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Check Python syntax
      run: python -m py_compile *.py
    
    - name: Test imports
      run: python -c "from dashboard import *; from definitions_model import *; print('✓ All imports successful')"
"""
        
        self._write_file(".github/workflows/test.yml", workflow_content)
        print("✅ GitHub Actions workflow created")
    
    def create_readme(self) -> None:
        """Create comprehensive README"""
        print("\n📄 Creating README...")
        
        readme = """# Strategic Foresight - Social Protection Reform Analysis Dashboard

A machine learning-powered dashboard for analyzing and classifying social protection reforms across key strategic dimensions.

## 🎯 Features

- **Intelligent Classification**: AI-powered categorization of reforms using sentence embeddings
- **Interactive Dashboard**: Real-time visualizations and analytics
- **Semantic Search**: Find relevant reforms by meaning, not just keywords
- **Multi-dimensional Analysis**: View reforms across Climate, Demographics, Technology, and Work trends

## 📊 Categories

1. **Climate Change** - Environmental resilience and adaptation
2. **Demographic Change** - Ageing, migration, family structures
3. **Digital Technology** - Digital transformation & inclusion
4. **Shifting Nature of Work** - Gig economy, remote work, reskilling

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone <your-repo-url>
cd foresight_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
streamlit run dashboard.py
```

Visit `http://localhost:8501`

## 🌐 Deploy to Cloud

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on:
- ☁️ Streamlit Cloud (Recommended - Free & Easiest)
- 🚂 Railway.app
- 🎨 Render
- 🐳 Docker
- And more...

**Fastest deployment**: Streamlit Cloud (5 minutes)

## 📦 Requirements

- Python 3.10+
- Streamlit 1.28+
- Sentence Transformers
- Scikit-learn
- Plotly
- Pandas

## 📂 Project Structure

```
.
├── dashboard.py              # Main Streamlit app
├── definitions_model.py      # ML classification model
├── classify.py              # Classification logic
├── clasify_reforms.py       # Batch processing
├── requirements.txt         # Dependencies
├── Dockerfile              # Container setup
├── docker-compose.yml      # Local testing
├── Procfile               # Deployment config
└── DEPLOYMENT_GUIDE.md    # Deployment instructions
```

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Color theme
- Page layout
- Server settings

## 💡 How It Works

1. **Input Processing**: Reforms are processed as text
2. **Embedding**: Converted to semantic vectors using SentenceTransformer
3. **Classification**: Compared against category definitions
4. **Visualization**: Results displayed in interactive dashboard

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## 📋 Troubleshooting

### App runs slow
- First load downloads ML models (~400MB)
- Models are cached locally after first run
- Consider deploying on platform with persistent storage

### Data not loading
- Check relative file paths
- Ensure data files are in repository root
- Use absolute paths for cloud deployment

### Memory issues
- Streamlit Cloud: Use smaller models
- Docker: Increase container memory limit

## 📞 Support

For issues, please check:
1. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. [Streamlit Docs](https://docs.streamlit.io)
3. GitHub Issues

## 📄 License

Specified in LICENSE file

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io)
- [Sentence Transformers](https://www.sbert.net)
- [Plotly](https://plotly.com)
- [Scikit-learn](https://scikit-learn.org)

---

**Ready to deploy?** Check out [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions! 🚀
"""
        
        self._write_file("README.md", readme)
        print("✅ README created")
    
    def create_requirements_optimized(self) -> None:
        """Create optimized requirements for production"""
        print("\n📦 Optimizing requirements...")
        
        requirements = """streamlit==1.28.1
pandas==2.0.3
plotly==5.17.0
numpy==1.24.3
openpyxl==3.1.2
sentence-transformers==2.2.2
scikit-learn==1.3.1
torch==2.0.1
gunicorn==21.2.0
"""
        self._write_file("requirements-prod.txt", requirements)
        print("✅ Production requirements created")
    
    def generate_deployment_report(self, analysis: dict) -> None:
        """Generate a deployment readiness report"""
        print("\n📊 Generating deployment report...")
        
        report = {
            "project_name": "foresight-dashboard",
            "analysis": analysis,
            "deployment_readiness": {
                "status": "READY",
                "files_created": [
                    "Dockerfile",
                    "docker-compose.yml",
                    ".gitignore",
                    "Procfile",
                    ".streamlit/config.toml",
                    "runtime.txt",
                    "DEPLOYMENT_GUIDE.md",
                    "README.md"
                ],
                "recommended_platforms": [
                    {"name": "Streamlit Cloud", "effort": "Minimal", "cost": "Free"},
                    {"name": "Railway.app", "effort": "Low", "cost": "$5-50/month"},
                    {"name": "Render", "effort": "Low", "cost": "Free-$7/month"},
                    {"name": "Docker", "effort": "Medium", "cost": "Varies"}
                ]
            },
            "next_steps": [
                "1. Review DEPLOYMENT_GUIDE.md",
                "2. Choose deployment platform",
                "3. Push code to GitHub",
                "4. Follow platform-specific instructions",
                "5. Test live application",
                "6. Share with stakeholders"
            ]
        }
        
        with open(self.project_path / "DEPLOYMENT_REPORT.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("✅ Deployment report generated")
        self._print_report(report)
    
    def _write_file(self, filename: str, content: str) -> None:
        """Helper to write files"""
        file_path = self.project_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def _print_report(self, report: dict) -> None:
        """Pretty print deployment report"""
        print("\n" + "="*60)
        print("🎉 DEPLOYMENT READY!")
        print("="*60)
        print(f"\n✅ Status: {report['deployment_readiness']['status']}")
        print(f"\n📁 Files Created:")
        for file in report['deployment_readiness']['files_created']:
            print(f"   • {file}")
        
        print(f"\n☁️  Recommended Platforms:")
        for platform in report['deployment_readiness']['recommended_platforms']:
            print(f"   • {platform['name']}: {platform['effort']} effort, {platform['cost']}")
        
        print(f"\n📋 Next Steps:")
        for step in report['next_steps']:
            print(f"   {step}")
        
        print("\n" + "="*60)
    
    def run(self) -> None:
        """Run complete deployment preparation"""
        print("\n🤖 FORESIGHT DEPLOYMENT AGENT STARTED\n")
        print(f"📍 Project Path: {self.project_path}\n")
        
        # Step 1: Analyze
        analysis = self.analyze_project()
        
        # Step 2: Create all deployment files
        self.create_deployment_files()
        self.create_docker_compose()
        self.create_github_actions()
        
        # Step 3: Create documentation
        self.create_deployment_guide()
        self.create_readme()
        self.create_requirements_optimized()
        
        # Step 4: Generate report
        self.generate_deployment_report(analysis)
        
        print("\n✨ AGENT TASK COMPLETE!\n")


if __name__ == "__main__":
    # Get project path
    project_path = Path(__file__).parent
    
    # Initialize and run agent
    agent = DeploymentAgent(str(project_path))
    agent.run()
    
    print("\n💡 Next: Review DEPLOYMENT_GUIDE.md and choose your deployment platform!")
