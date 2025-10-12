#!/usr/bin/env python3
"""
Setup script for Type 2 Diabetes Drug Sequencing NMA Project
Automates installation and deployment of all components
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ProjectSetup:
    """Automated setup and deployment for the diabetes NMA project"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_met = False

    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
            return False

    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")

        # Install main requirements
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ])
            print("✅ Pip upgraded successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to upgrade pip: {e}")
            return False

        # Install Streamlit dashboard requirements
        requirements_file = self.project_root / "10_streamlit_dashboard" / "requirements.txt"
        if requirements_file.exists():
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ])
                print("✅ Streamlit dashboard dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dashboard dependencies: {e}")
                return False

        # Install visualization dependencies
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "matplotlib", "seaborn", "plotly", "pandas", "numpy"
            ])
            print("✅ Visualization dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install visualization dependencies: {e}")
            return False

        return True

    def check_r_installation(self):
        """Check if R is available"""
        print("🔍 Checking R installation...")
        try:
            result = subprocess.run(
                ["R", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print("✅ R is installed")
                return True
            else:
                print("❌ R not found in PATH")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ R not found or not accessible")
            return False

    def setup_r_environment(self):
        """Setup R environment and install packages"""
        print("🛠️ Setting up R environment...")

        r_script = """
        # Install required R packages
        packages <- c('gemtc', 'rjags', 'coda', 'ggplot2', 'dplyr', 'readr', 'tidyr', 'metafor')
        for (pkg in packages) {
            if (!require(pkg, character.only = TRUE)) {
                install.packages(pkg, repos = 'https://cran.r-project.org', dependencies = TRUE)
                library(pkg, character.only = TRUE)
            }
        }
        print('✅ All R packages installed successfully')
        """

        try:
            # Write R script to temporary file
            with open(self.project_root / "temp_r_setup.R", "w") as f:
                f.write(r_script)

            # Run R script
            result = subprocess.run(
                ["R", "--vanilla", "-f", str(self.project_root / "temp_r_setup.R")],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("✅ R environment setup completed")
                return True
            else:
                print(f"❌ R setup failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error setting up R environment: {e}")
            return False
        finally:
            # Clean up temporary file
            temp_file = self.project_root / "temp_r_setup.R"
            if temp_file.exists():
                temp_file.unlink()

    def run_visualizations(self):
        """Generate all visualizations"""
        print("🎨 Generating visualizations...")

        viz_script = self.project_root / "09_python_visualization" / "python_nma_visualization.py"
        if viz_script.exists():
            try:
                result = subprocess.run([
                    sys.executable, str(viz_script)
                ], capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    print("✅ Visualizations generated successfully")
                    return True
                else:
                    print(f"❌ Visualization generation failed: {result.stderr}")
                    return False

            except subprocess.TimeoutExpired:
                print("❌ Visualization generation timed out")
                return False
            except Exception as e:
                print(f"❌ Error generating visualizations: {e}")
                return False
        else:
            print("❌ Visualization script not found")
            return False

    def create_deployment_package(self):
        """Create deployment package for easy sharing"""
        print("📦 Creating deployment package...")

        # Create deployment directory
        deploy_dir = self.project_root / "deployment"
        deploy_dir.mkdir(exist_ok=True)

        # Copy essential files for deployment
        files_to_copy = [
            "README.md",
            "LICENSE",
            ".gitignore",
            "10_streamlit_dashboard/app.py",
            "10_streamlit_dashboard/requirements.txt",
            "09_python_visualization/python_nma_visualization.py",
            "05_manuscript/complete_manuscript.md",
            "08_project_summary/final_project_report.md"
        ]

        for file_path in files_to_copy:
            src = self.project_root / file_path
            if src.exists():
                dst = deploy_dir / file_path.replace("/", "_")
                shutil.copy2(src, dst)
                print(f"  ✅ Copied: {file_path}")

        # Create deployment instructions
        deploy_readme = deploy_dir / "DEPLOYMENT_README.md"
        with open(deploy_readme, "w") as f:
            f.write("""
# Diabetes NMA Project - Deployment Package

## Quick Start

### Option 1: Interactive Dashboard
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Generate Visualizations
```bash
python python_nma_visualization.py
```

### Option 3: View Results
- Open `complete_manuscript.md` for full research findings
- Open `final_project_report.md` for executive summary

## Project Structure
- **app.py** - Interactive Streamlit dashboard
- **python_nma_visualization.py** - Generate publication-ready plots
- **complete_manuscript.md** - Full research manuscript
- **final_project_report.md** - Executive summary

## Requirements
- Python 3.8+
- R 4.0+ (for statistical analysis)
- Required packages listed in requirements.txt

## Support
For issues or questions, please refer to the main project repository.
""")

        print(f"✅ Deployment package created: {deploy_dir}")
        return True

    def run_diagnostics(self):
        """Run comprehensive diagnostics"""
        print("🔍 Running project diagnostics...")

        diagnostics = {
            "Python Version": self.check_python_version(),
            "Python Dependencies": self.install_python_dependencies(),
            "R Installation": self.check_r_installation(),
            "R Environment": self.setup_r_environment(),
            "Visualizations": self.run_visualizations(),
            "Deployment Package": self.create_deployment_package()
        }

        # Summary
        print("\n" + "="*50)
        print("📋 DIAGNOSTICS SUMMARY")
        print("="*50)

        all_passed = True
        for check, result in diagnostics.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{check:20} {status}")
            if not result:
                all_passed = False

        print("="*50)
        if all_passed:
            print("🎉 All diagnostics passed! Project is ready for use.")
        else:
            print("⚠️ Some diagnostics failed. Please check the errors above.")

        return all_passed

    def run_setup(self):
        """Run complete setup process"""
        print("🚀 Starting automated project setup...")
        print("="*60)

        success = self.run_diagnostics()

        print("\n" + "="*60)
        if success:
            print("✅ SETUP COMPLETED SUCCESSFULLY!")
            print("🎯 Project is ready for use:")
            print("   • Run 'streamlit run 10_streamlit_dashboard/app.py' for interactive dashboard")
            print("   • Run 'python 09_python_visualization/python_nma_visualization.py' for plots")
            print("   • Check deployment/ folder for portable version")
        else:
            print("❌ SETUP COMPLETED WITH ERRORS")
            print("🔧 Please resolve the issues above and run setup again")
        print("="*60)

        return success

# Main execution
if __name__ == "__main__":
    setup = ProjectSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)
