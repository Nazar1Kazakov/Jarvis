import subprocess
import re
import psutil

def get_cpu_temp():
    try:
        output = subprocess.check_output(['sensors'], encoding='utf-8')
        match = re.search(r'k10temp-pci-[\w\d]+\n(?:.*\n)*?.*Tctl:\s+\+([\d.]+)°C', output)
        if match:
            return float(match.group(1))
    except Exception:
        return None

def get_cpu_load():
    return psutil.cpu_percent(interval=1)

def get_gpu_temp_and_load():
    try:
        output = subprocess.check_output(['rocm-smi'], encoding='utf-8')
        temp_match = re.search(r'\d+\s+\d+\s+0x[\da-f]+,\s+\d+\s+([\d.]+)°C', output)
        load_match = re.search(r'GPU%\s+(\d+)%', output)
        temp = float(temp_match.group(1)) if temp_match else None
        load = int(load_match.group(1)) if load_match else None
        return temp, load
    except Exception:
        return None, None

def get_ram_usage():
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024 ** 3)  # в Гб
    percent = mem.percent
    return used_gb, percent
