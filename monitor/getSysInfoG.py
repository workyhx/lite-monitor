import psutil
import platform
import concurrent.futures


def get_windows_disk_info():
    total_size = 0
    total_used_size = 0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            total_size += disk_usage.total
            total_used_size += disk_usage.used
        except PermissionError:
            continue
    total_percent = (total_used_size / total_size) * 100 if total_size > 0 else 0
    return (
        round(total_used_size / (1024.0 ** 3), 3),
        round(total_size / (1024.0 ** 3), 3),
        round(total_percent, 2),
    )


def get_linux_disk_info():
    disk = psutil.disk_usage('/')
    return (
        round(disk.used / (1024.0 ** 3), 3),
        round(disk.total / (1024.0 ** 3), 3),
        disk.percent
    )


async def get_system_usage():
    os_type = platform.system()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        cpu_future = executor.submit(psutil.cpu_percent, 1)
        mem_future = executor.submit(psutil.virtual_memory)

        if os_type == "Windows":
            disk_future = executor.submit(get_windows_disk_info)
        elif os_type == "Linux":
            disk_future = executor.submit(get_linux_disk_info)
        else:
            disk_future = None

        cpu_percent = cpu_future.result()
        mem = mem_future.result()
        mem_used = round(mem.used / (1024.0 ** 3), 3)
        mem_total = round(mem.total / (1024.0 ** 3), 3)
        mem_percent = mem.percent

        if disk_future:
            disk_used, disk_total, disk_percent = disk_future.result()
        else:
            disk_used = disk_total = disk_percent = 0

    return {
        "cpu_percent": cpu_percent,
        "mem_used": mem_used,
        "mem_total": mem_total,
        "mem_percent": mem_percent,
        "disk_used": disk_used,
        "disk_total": disk_total,
        "disk_percent": disk_percent
    }
