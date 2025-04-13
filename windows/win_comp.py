import wmi
import socket
import GPUtil
import psutil

def pccomponents_windows(system_result):
    result = system_result
    # Процессор
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        cpu_name = cpu.Name
        cpu_cores = cpu.NumberOfCores
    result = result + f"ПРОЦЕССОР:\n\t{cpu_name}\n\tКоличество ядер процессора: {cpu_cores}\n\n"

    #Видеокарта
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_driver = gpu.driver
        gpu_vram = gpu.memoryTotal
    result = result + f"ВИДЕОКАРТА:\n\tНазвание видеокарты: {gpu_name}\n\tВерсия видеодрайвера: {gpu_driver}\n\tПамять видеокарты: {gpu_vram} MB\n\n"

    #Накопители
    result = result + f"ЖЁСТКИЙ ДИСК:\n\t"
    for disk in c.Win32_LogicalDisk():
        disk_type = disk.Description
        disk_lett = disk.Caption

        if disk.Size is not None:
            if int(disk.Size) >= 1099511627776:
                disk_size = round(int(disk.Size) / 1099511627776, 2)
                disk_is = "TB"
            elif int(disk.Size) >= 1073741824:
                disk_size = round(int(disk.Size) / 1073741824, 2)
                disk_is = "GB"
            elif int(disk.Size) >= 1048576:
                disk_size = round(int(disk.Size) / 1048576, 2)
                disk_is = "MB"
        result += f"Тип: {disk_type}({disk_lett})\n\tОбъём: {disk_size}{disk_is}\n\t"
    
    result += f"\n\tСписок дисков:\n\t"

    for disk in c.Win32_DiskDrive():
        disk_model = disk.Model
        result += f"\tНазвание: {disk_model}\n\t"

    #Материнская плата
    mboard = c.Win32_BaseBoard()[0].Product
    result += f"\nМАТЕРИНСКАЯ ПЛАТА:\n\tСерия: {mboard}\n"
    
    #Оперативная память

    memory_types = {
        20: "DDR",
        21: "DDR2",
        22: "DDR2-FB-DIMM",
        24: "DDR3",
        26: "DDR4",
        27: "LPDDR4",
        28: "LPDDR5",
        30: "LPDDR3",
        34: "DDR5",
        0: "Unknown"
    }

    total = 0
    result += "\nОПЕРАТИВНАЯ ПАМЯТЬ:\n\t"
    for mem in c.Win32_PhysicalMemory():
        total += int(mem.Capacity)
    total = round(total / 1073741824, 2)
    result += f"Установленная {total} GB\n"

    count = 1  
    for mem in c.Win32_PhysicalMemory():
        mem_speed = mem.Speed
        mem_manf = mem.Manufacturer
        mem_typeid = mem.SMBIOSMemoryType
        mem_type = memory_types[mem_typeid]
        result += f"\tОперативная память {count}:\n\t\tНазвание: {mem_manf}\n\t\tТип памяти: {mem_type}\n\t\tСкорость: {mem_speed}\n"
        count += 1

    #Сетевые настройки
    result += "\nСЕТЕВЫЕ НАСТРОЙКИ:"
    count = 1
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                ip_address = address.address
                netmask = address.netmask
                result += f"\n\tСеть {count}:\n\t\tIP Адрес: {ip_address}\n\t\tМаска подсети: {netmask}"
                count += 1
    # Финальный результат
    return result