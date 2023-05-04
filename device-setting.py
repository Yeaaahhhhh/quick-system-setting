import os
import platform
import psutil
import socket
from screeninfo import get_monitors

def main():
    # Get device name
    device_name = socket.gethostname()

    # Get processor information
    processor = platform.processor()

    # Get CPU core count
    cpu_cores = os.cpu_count()

    # Get RAM size
    ram_size = psutil.virtual_memory().total // (1024 ** 3)

    # Get device and product ID (Windows only)
    
    product_id = ''
    if platform.system() == 'Windows':
        
        product_id = os.popen('wmic os get SerialNumber /value').read().split('=')[-1].strip()

    # Get Windows edition and version
    windows_edition = platform.platform(terse=True)
    windows_version = platform.version()

    # Get HDD and SSD size
    hdd_size = 0
    ssd_size = 0
    for disk in psutil.disk_partitions():
        if 'fixed' in disk.opts:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            if 'SSD' in disk.device:
                ssd_size += disk_usage.total // (1024 ** 3)
            else:
                hdd_size += disk_usage.total // (1024 ** 3)

    # Get GPU information
    gpu_info = ''
    if platform.system() == 'Windows':
        try:
            # Try to get NVIDIA GPU information
            gpu_info = os.popen('nvidia-smi --query-gpu=name --format=csv,noheader').read().strip()
        except:
            # Try to get AMD GPU information
            try:
                gpu_info = os.popen('rocm-smi --showproductname').read().strip()
            except:
                pass

    # Get screen resolution
    screen_resolution = f'{get_monitors()[0].width}x{get_monitors()[0].height}'

    # Save data to a .txt file
    with open('computer_info.txt', 'w') as f:
        f.write(f'Device Name: {device_name}\n')
        f.write(f'Processor: {processor}\n')
        f.write(f'CPU Cores: {cpu_cores}\n')
        f.write(f'RAM Size: {ram_size} GB\n')
        
        f.write(f'Product ID: {product_id}\n')
        f.write(f'Windows Edition: {windows_edition}\n')
        f.write(f'Windows Version: {windows_version}\n')
        f.write(f'HDD Size: {hdd_size} GB\n')
        f.write(f'SSD Size: {ssd_size} GB\n')
        f.write(f'GPU: {gpu_info}\n')
        f.write(f'Screen Resolution: {screen_resolution}\n')

if __name__ == '__main__':
    main()
