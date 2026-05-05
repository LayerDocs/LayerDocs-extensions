import subprocess
import sys
import os
import urllib.request
import zipfile
import shutil

class LayerDocs:
    """Python wrapper for the LayerDocs Engine with Auto-Downloader."""
    
    ENGINE_URL = "https://github.com/LayerDocs/LayerDocs-core/releases/latest/download/layerdocs.zip"
    
    def __init__(self, cli_path=None):
        self.cli_path = cli_path or self._find_or_install_engine()

    def _find_or_install_engine(self):
        # 1. Check if in PATH
        path = shutil.whoami() if hasattr(shutil, "whoami") else None # Fallback
        if shutil.which("layerdocs"):
            return "layerdocs"
        
        # 2. Check local app data
        app_data = os.path.join(os.path.expanduser("~"), ".layerdocs")
        engine_bin = os.path.join(app_data, "bin", "layerdocs.bat" if os.name == "nt" else "layerdocs")
        
        if os.path.exists(engine_bin):
            return engine_bin
            
        # 3. Auto-Download if missing
        print("🚀 LayerDocs Engine not found. Downloading the latest version...")
        os.makedirs(app_data, exist_ok=True)
        zip_path = os.path.join(app_data, "engine.zip")
        
        try:
            urllib.request.urlretrieve(self.ENGINE_URL, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(app_data)
            os.remove(zip_path)
            
            # Make executable on Linux/Mac
            if os.name != "nt":
                os.chmod(engine_bin, 0o755)
                
            print("✅ Engine installed successfully!")
            return engine_bin
        except Exception as e:
            print(f"❌ Failed to download engine: {e}")
            print("Please install the LayerDocs engine manually from https://github.com/LayerDocs/LayerDocs-core")
            return "layerdocs"

    def compile(self, file_path, output_dir=None):
        """Compiles a .qd file using the LayerDocs CLI."""
        cmd = [self.cli_path, "c", file_path]
        if output_dir:
            cmd.extend(["-o", output_dir])
        return subprocess.run(cmd, capture_output=True, text=True)

def main():
    """Entry point for the layerdocs command-line interface."""
    ld = LayerDocs()
    subprocess.run([ld.cli_path] + sys.argv[1:])
