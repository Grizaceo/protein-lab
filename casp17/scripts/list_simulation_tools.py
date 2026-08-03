import sys
import os

print("Python executable:", sys.executable)

packages = ["openmm", "MDAnalysis", "prody", "scipy", "numpy", "Bio", "torch"]
print("=== Installed Science Packages ===")
for pkg in packages:
    try:
        mod = __import__(pkg)
        version = getattr(mod, "__version__", "installed")
        print(f"  - {pkg}: {version}")
    except ImportError:
        print(f"  - {pkg}: NOT INSTALLED")
