import openmm
import openmm.app as app

print(f"OpenMM Version: {openmm.__version__}")
platforms = [openmm.Platform.getPlatform(i).getName() for i in range(openmm.Platform.getNumPlatforms())]
print(f"Platforms: {platforms}")

# Check CUDA platform availability
try:
    platform = openmm.Platform.getPlatformByName("CUDA")
    print(f"CUDA Platform available! Device count: {platform.getPropertyDefaultValue('CudaDeviceIndex')}")
except Exception as e:
    print(f"CUDA Platform check: {e}")
