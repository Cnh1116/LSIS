import subprocess
import os
import re
from datetime import datetime
import xml.etree.ElementTree as lsis
from xml.dom import minidom

# LSIS: Linux System Information Script
# Carson Holland
# December 2023

error_logging_file_name = 'lsis_error_log.txt'
xml_output_file_name = 'lsis_output.xml'

# Command to Ensure this Script is not running on a Windows system
def Is_Linux():
      return(os.name == 'posix')

# Command to Run a command and return output. Logs Errors.
def Run_Command(command_string):
    pipe = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
    out,err = pipe.communicate()
    if pipe.returncode != 0:
        Log_Error(f'COMMAND: {command_string.strip()}\nERROR: {err.strip()}\nRETURN CODE:{pipe.returncode}\n')
    return (dict([('Return Code', pipe.returncode),('Output', out)]))

def Log_Error(error_string):
    Log_Error.counter += 1
    header = '\n' + '_'*55 + '\n'
    error_logging_file = open(error_logging_file_name, 'a')
    error_logging_file.write(header+error_string)
    error_logging_file.close()

#def Reg_Search(reg_exp_string):

# APU INFORMATION FUNCTIONS~~~~~~
def Get_CPU_Name(): 
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('CPU Name: Information Not Available')
        return('Information Not Available')
        
    search_object = re.findall('^Model name:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            print('CPU Name: Information Not Available')
            return('Information Not Available')
            
    cpu_model_name = search_object[0]
    cpu_model_name = cpu_model_name.replace('Model name:', '')
    cpu_model_name = cpu_model_name.lstrip()
    print(f'CPU Name: {cpu_model_name}')
    return(cpu_model_name)

def Get_CPU_Info():
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('CPU Info: Information Not Available')
        return('Information Not Available')
    
    #Vendor ID
    search_object = re.findall('^Vendor ID:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
            vendor_id = '---'
    else:       
        vendor_id = search_object[0]
        vendor_id = vendor_id.replace('Vendor ID:', '')
        vendor_id = vendor_id.lstrip()
    
        if 'AMD' in vendor_id:
            vendor_id = 'AMD'
        if 'Intel' in vendor_id:
            vendor_id = 'Intel'
    
    #32/64 Bit
    search_object = re.findall('^Architecture:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            bit_size = '--'
            
    architecture = search_object[0]
    if '64' in architecture:
        bit_size = '64'
    elif '32' in architecture:
        bit_size = '32'
    else:
        bit_size = '--'
    
    #Family
    search_object = re.findall('^CPU family:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        cpu_family = ""
    else:
        cpu_family = search_object[0]
        cpu_family = cpu_family.replace('CPU family:','')
        cpu_family = cpu_family.lstrip()
    
    #CPU Model
    search_object = re.findall('^Model:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            cpu_model = '----'
    else:
        cpu_model = search_object[0]
        cpu_model = cpu_model.replace('Model:','')
        cpu_model = cpu_model.lstrip()
    
    #CPU Stepping
    search_object = re.findall('^Stepping:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
        cpu_stepping == '---'
    else:
        cpu_stepping = search_object[0]
        cpu_stepping = cpu_stepping.replace('Stepping:','')
        cpu_stepping = cpu_stepping.lstrip()
    
    cpu_info = vendor_id  + bit_size + ' Family ' + cpu_family + 'h Model ' + cpu_model + 'h Stepping ' + cpu_stepping
    print(f'CPU Info: {cpu_info}')
    return(cpu_info)

def Get_Core_Count():
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('Core Count: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^Core\(s\) per socket:\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            print('Core Count: Information Not Available')
            return('Information Not Available')
    core_count = search_object[0]
    core_count = core_count.replace('Core(s) per socket:', '')
    core_count = core_count.lstrip()
    
    print(f'Core Count: {core_count}')
    return(core_count)
    
def Get_Logical_Processors():
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('Logical Processors: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^CPU\(s\):\s+.+.*$', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            print('Logical Processors: Information Not Available')
            return('Information Not Available')
    logical_processors = search_object[0]
    logical_processors = logical_processors.replace('CPU(s):', '')
    logical_processors = logical_processors.lstrip()
    
    print(f'Logical Processors: {logical_processors}')
    return(logical_processors)
    
def Get_Total_Memory():
    meminfo_output = Run_Command('cat /proc/meminfo')
    if meminfo_output['Return Code'] != 0:
        print('Total Memory: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^MemTotal:\s+.+.*$', meminfo_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0: #If len is 0, nothing was found...
            print('Total Memory: Information Not Available')
            return('Information Not Available')
    total_memory = search_object[0]
    total_memory = total_memory.replace('MemTotal:', '')
    total_memory = total_memory.replace('kB', '')
    total_memory = total_memory.lstrip()
    total_memory = total_memory.rstrip()
    total_memory_gb = float(total_memory) / 1000000.0
    total_memory_gb = round(total_memory_gb, 2)
    total_memory_gb = str(total_memory_gb)
    total_memory_gb = total_memory_gb + ' GB'
    print(f'Total Memory: {total_memory_gb}')
    return(total_memory_gb)
    
def Get_Memory_Info():
    meminfo_output = Run_Command('sudo dmidecode --type 17')
    if meminfo_output['Return Code'] != 0:
        print('Memory Info: Information Not Available')
        return('Information Not Available')
    
    locators = re.findall('^\s+Locator:.+', meminfo_output['Output'], re.M)  #^CTR.*$
    manufacturers = re.findall('^\s+Manufacturer:.+', meminfo_output['Output'], re.M)  #^CTR.*$
    mem_speeds = re.findall('^\s+Configured Memory Speed:.+', meminfo_output['Output'], re.M)  #^CTR.*$
    mem_sizes = re.findall('^\s+Size:.+', meminfo_output['Output'], re.M)  #^CTR.*$
    
    for iterator in range(len(manufacturers)): #Reformat the Strings
        locators[iterator] = locators[iterator].replace('Locator:', '')
        locators[iterator] = locators[iterator].lstrip()
        manufacturers[iterator] = manufacturers[iterator].replace('Manufacturer:', '')
        manufacturers[iterator] = manufacturers[iterator].lstrip()
        mem_speeds[iterator] = mem_speeds[iterator].replace('Configured Memory Speed:', '')
        mem_speeds[iterator] = mem_speeds[iterator].lstrip()
        mem_sizes[iterator] = mem_sizes[iterator].replace('Size:', '')
        mem_sizes[iterator] = mem_sizes[iterator].lstrip()
    
    memory_info = ''
    for iterator in range(len(locators)):
        if ('No Module Installed' not in mem_sizes[iterator]): #Logic check to see if the current mem slot was empty/not
            memory_info = memory_info + '[' + locators[iterator] + ' ' + manufacturers[iterator] + ' ' + mem_speeds[iterator] + ' ' + mem_sizes[iterator] + ']'
            if iterator != len(locators)-1: #IF not last element, add a comma
                memory_info = memory_info + ','   
    print(f'Memory Information: {memory_info}')
    return(memory_info)
# END APU INFORMATION FUNCTIONS

# BASEBOARD INFORMATION FUNCTIONS~~~~~~
def Get_Product_Name():
    dmidecode_output = Run_Command('sudo dmidecode -t baseboard')
    if dmidecode_output['Return Code'] != 0:
        print('Product Name: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+Product Name:.+', dmidecode_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('Product Name: Information Not Available')
        return('Information Not Available')
    product_name = search_object[0]
    product_name = product_name.replace('Product Name:', '')
    product_name = product_name.lstrip()
    
    print(f'Product Name: {product_name}')
    return(product_name)

def Get_Board_Version():
    dmidecode_output = Run_Command('sudo dmidecode -t baseboard')
    if dmidecode_output['Return Code'] != 0:
        print('Board Version: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+Version:.+', dmidecode_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('Board Version: Information Not Available')
        return ('Information Not Available')
    board_version = search_object[0]
    board_version = board_version.replace('Version:', '')
    board_version = board_version.lstrip()
    
    print(f'Board Version: {board_version}')
    return(board_version)
    
def Get_Board_Manufacturer():
    dmidecode_output = Run_Command('sudo dmidecode -t baseboard')
    if dmidecode_output['Return Code'] != 0:
        print('Board Manufacturer: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+Manufacturer:.+', dmidecode_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('Manufacturer: Information Not Available')
        return('Information Not Available')
    board_manufacturer = search_object[0]
    board_manufacturer = board_manufacturer.replace('Manufacturer:', '')
    board_manufacturer = board_manufacturer.lstrip()
    
    print(f'Board Manufacturer: {board_manufacturer}')
    return(board_manufacturer)

def Get_Board_SKU():
    dmidecode_output = Run_Command('sudo dmidecode -t system')
    if dmidecode_output['Return Code'] != 0:
        print('SKU: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+SKU Number:.+', dmidecode_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('SKU: Information Not Available')
        return ('Information Not Available')
    sku = search_object[0]
    sku = sku.replace('SKU Number:', '')
    sku = sku.lstrip()
    
    print(f'SKU: {sku}')
    return(sku)

def Get_Battery_Info():
    if Run_Command('which ectool') == "": #Meaning Pure Linux system
        upower_e_output = Run_Command('upower -e')
        
        #Find the location relating to the battery
        search_object = re.findall('^.+battery.+', upower_e_output['Output'], re.M)  #^CTR.*$
        if len(search_object) == 0: #If not location containing battery is output, no info available
            print('Battery Info: Information Not Available')
            return('Information Not Available')
        battery_info_location = search_object[0]
        battery_info_output = Run_Command(f'upower -i {battery_info_location}')

        
        search_object = re.findall('^.+state:.+unknown', battery_info_output['Output'], re.M)  #^CTR.*$
        if len(search_object) != 0: #If there was a location for battery, but specs say unknown, no info available
            print('Battery Info: Information Not Available')
            return('Information Not Available')
            
        else: # VALIDATE FOR LINUX LAPTOPS
            search_object = re.findall('^.+energy:.+', battery_info_output['Output'], re.M)  #^CTR.*$
            if len(search_object) == 0: #If len is 0, nothing was found...
                print('Battery Info: Information Not Available')
                return('Information Not Available')
            battery_capacity = search_object[0]
            battery_capacity = battery_capacity.replace('Design capacity:', '')
            battery_capacity = battery_capacity.lstrip()
            
            search_object = re.findall('^.+technology.+', battery_info_output['Output'], re.M)  #^CTR.*$
            if len(search_object) == 0: #If len is 0, nothing was found...
                print('Battery Info: Information Not Available')
                return('Information Not Available')
            battery_chemistry = search_object[0]
            battery_chemistry = battery_chemistry.replace('Chemistry   :', '')
            battery_chemistry = battery_chemistry.lstrip()
        
        print(f'Battery Info: {battery_info_output}')
        return(battery_info_output) #search for energy and technology
        
    else: #Meaning Chromebook
        ectool_output = Run_Command('ectool battery') #Search for Designed Capacity and Chemistry
        
        search_object = re.findall('^.+Design capacity:.+', ectool_output['Output'], re.M)  #^CTR.*$
        if len(search_object) == 0: #If len is 0, nothing was found...
            print('Battery Info: Information Not Available')
            return('Information Not Available')
        battery_capacity = search_object[0]
        battery_capacity = battery_capacity.replace('Design capacity:', '')
        battery_capacity = battery_capacity.lstrip()
        
        
        search_object = re.findall('^.+Chemistry.+', ectool_output['Output'], re.M)  #^CTR.*$
        if len(search_object) == 0: #If len is 0, nothing was found...
            print('Battery Info: Information Not Available')
            return('Information Not Available')
        battery_chemistry = search_object[0]
        battery_chemistry = battery_chemistry.replace('Chemistry   :', '')
        battery_chemistry = battery_chemistry.lstrip()
        battery_final_information = battery_capacity + ' ' + battery_chemistry

        print(f'Battery Info: {battery_final_information}')
        return(battery_final_information)
# END OF BASEBOARD INFO FUNCTIONS

# STORAGE INFO FUNCTIONS~~~~~~
def Get_ALPM_Mode():
    alpm_output = Run_Command('cat /sys/class/scsi_host/host0/link_power_management_policy')
    if alpm_output['Return Code'] != 0:
        print('ALPM Not Supported in this System')
        return('ALPM Not Supported in this System')

    else: #If the command did find the file ALPM does exist
        if (alpm_output['Output'] == 'min_power') or (alpm_output['Output'] == 'medium_power'): #ALPM has 3 states: min/medium power means it is active, max performance means it is not active
            print('ALPM On: ' + alpm_output['Output'].strip())
            return 'ALPM On: ' + alpm_output['Output'].strip()
        else:
            print('ALPM Off: ' + alpm_output['Output'].strip())
            return 'ALPM Off: ' + alpm_output['Output'].strip()
# END STORAGE INFO FUNCTIONS

# CACHE INFO FUNCTIONS~~~~~~
def Get_L1_Cache():
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('L1 Cache: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('L1d.+', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('L1 Cache Info: Information Not Available')
        return ('Information Not Available')
    l1_data = search_object[0]
    l1_data = l1_data.replace('L1d cache:', '')
    l1_data = l1_data.lstrip()
    
    search_object = re.findall('L1i.+', lscpu_output['Output'], re.M)  #^CTR.*$
    l1_instruct = search_object[0]
    l1_instruct = l1_instruct.replace('L1i cache:', '')
    l1_instruct = l1_instruct.lstrip()
    
    l1_cache = 'DATA: ' + l1_data + ' INSTRUCT: ' + l1_instruct
    print(f'L1 Cache Info: {l1_cache}')
    return(l1_cache)
    
def Get_L2_Cache():
    lscpu_output = Run_Command('lscpu')
    
    search_object = re.findall('L2.+', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('L1 Cache Info: Information Not Available')
        return ('Information Not Available')
    l2_cache = search_object[0]
    l2_cache = l2_cache.replace('L2 cache:', '')
    l2_cache = l2_cache.lstrip()
    
    print(f'L2 Cache Info: {l2_cache}')
    return(l2_cache)
    
def Get_L3_Cache():
    lscpu_output = Run_Command('lscpu')
    if lscpu_output['Return Code'] != 0:
        print('L3 Cache Info: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('L3.+', lscpu_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('L3 Cache Info: Information Not Available')
        return ('Information Not Available')
    l3_cache = search_object[0]
    l3_cache = l3_cache.replace('L3 cache:', '')
    l3_cache = l3_cache.lstrip()
    
    print(f'L3 Cache Info: {l3_cache}')
    return(l3_cache)
# END OF CACHE INFO FUNCTIONS 

# OS INFORMATION FUNCTIONS~~~~~~
def Get_OS_Version():
    os_info_output = Run_Command('cat /etc/os-release')
    if os_info_output['Return Code'] != 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
        
    search_object = re.findall('^NAME.+', os_info_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
    os_name = search_object[0]
    os_name = os_name.replace('NAME=', '')
    os_name = os_name.lstrip()
    
    search_object = re.findall('^VERSION=.+', os_info_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
    os_version = search_object[0]
    os_version = os_version.replace('VERSION=', '')
    os_version = os_version.lstrip() 
    
    os = os_name + ' ' + os_version
    os = os.replace('"', '')
    
    print(f'OS Info: {os}')
    return(os)
# END OF OS INFORMATION FUNCTIONS 

# BIOS INFO FUNCTIONS
def Get_BIOS_Info():
    bios_info_output = Run_Command('sudo dmidecode -t bios') #Search for Designed Capacity and Chemistry
    if bios_info_output['Return Code'] != 0:
        print('BIOS Info: Information Not Available')
        return('Information Not Available')
        
    search_object = re.findall('^\s+Vendor:.+', bios_info_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
    bios_vendor = search_object[0]
    bios_vendor = bios_vendor.replace('Vendor:', '')
    bios_vendor = bios_vendor.lstrip()
    
    search_object = re.findall('^\s+Version:.+', bios_info_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
    bios_version = search_object[0]
    bios_version = bios_version.replace('Version:', '')
    bios_version = bios_version.lstrip()
    
    search_object = re.findall('^\s+Release Date:.+', bios_info_output['Output'], re.M)  #^CTR.*$
    if len(search_object) == 0:
        print('OS Info: Information Not Available')
        return('Information Not Available')
    bios_date = search_object[0]
    bios_date = bios_date.replace('Release Date:', '')
    bios_date = bios_date.lstrip()
    
    bios_final_output = bios_vendor + ' ' + bios_version + ' ' + bios_date
    print(f'BIOS Info: {bios_final_output}')
    return(bios_final_output)
# END OF BIOS FUNCTIONS

# USB~~~~~~
def Get_USB():
    lsusb_output = Run_Command('lsusb')
    if lsusb_output['Return Code'] != 0:
        print('USB Info: Information Not Available')
        return('Information Not Available')
    
    print(lsusb_output["Output"])
    return(lsusb_output['Output'])
# END OF USB

# PCI~~~~~~
def Get_PCI():
    lspci_output = Run_Command('lspci')
    if lspci_output['Return Code'] != 0:
        print(f'PCI Info: Information Not Available')
        return('Information Not Available')
    
    print(lspci_output["Output"])
    return(lspci_output['Output'])
# END OF PCI

# GRAPHICS INFORMATION~~~~~~
def Get_Adapter_Name():
    lshw_display_output = Run_Command('sudo lshw -C display')
    if lshw_display_output['Return Code'] != 0:
        print('Adapter Name: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+product:.+', lshw_display_output['Output'], re.M)
    if len(search_object) == 0:
        print('Adapter Name: Information Not Available')
        return ('Information Not Available')
    adapter_name = search_object[0]
    adapter_name = adapter_name.replace('product:', '')
    adapter_name = adapter_name.lstrip()
    
    print(f'Adapter Name: {adapter_name}')
    return(adapter_name)
    
def Get_PCI_Address():
    lshw_display_output = Run_Command('sudo lshw -C display')
    if lshw_display_output['Return Code'] != 0:
        print('PCI Address: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+bus info:.+', lshw_display_output['Output'], re.M)
    if len(search_object) == 0:
        print('PCI Address: Information Not Available')
        return ('Information Not Available')
    pci_address = search_object[0]
    pci_address = pci_address.replace('bus info:', '')
    pci_address = pci_address.lstrip()
    
    print(f'PCI Address: {pci_address}')
    return(pci_address)
    
def Get_Driver():
    lshw_display_output = Run_Command('sudo lshw -C display')
    if lshw_display_output['Return Code'] != 0:
        print('Driver Info: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('driver=\w+', lshw_display_output['Output'], re.M)
    if len(search_object) == 0:
        print('Driver Info: Information Not Available')
        return ('Information Not Available')
    driver = search_object[0]
    driver = driver.replace('driver=', '')
    driver = driver.lstrip()
    
    print(f'Driver Info: {driver}')
    return(driver)
    
def Get_VRAM():
    dmesg_output = Run_Command('sudo dmesg | grep VRAM')
    if dmesg_output['Return Code'] != 0:
        print('VRAM Info: Information Not Available')
        return('Information Not Available')

    search_object = re.findall('\sDetected VRAM RAM=\w+', dmesg_output['Output'], re.M)
    if len(search_object) == 0:
        print('VRAM Info: Information Not Available')
        return ('Information Not Available')
    vram = search_object[0]
    vram = vram.replace('Detected VRAM RAM=', '')
    vram = vram.lstrip()
    
    print(f'VRAM Info: {vram}')
    return(vram)
    
def Get_Clock():
    lshw_display_output = Run_Command('sudo lshw -C display')
    if lshw_display_output['Return Code'] != 0:
        print('Clock Info: Information Not Available')
        return('Information Not Available')
    
    search_object = re.findall('^\s+clock:\s+\w+', lshw_display_output['Output'], re.M)
    if len(search_object) == 0:
        print('Clock Info: Information Not Available')
        return ('Information Not Available')
    gpu_clock = search_object[0]
    gpu_clock = gpu_clock.replace('clock:', '')
    gpu_clock = gpu_clock.lstrip()
    
    print(f'Clock Info: {gpu_clock}')
    return(gpu_clock)
# END OF GRAPHICS INFORMATION 

# MONITOR INFORMATION~~~~~~
def Get_Monitor_Support_Count():
    monitor_count_output = Run_Command('sudo ls /sys/kernel/debug/dri/0 | grep crtc-')
    if monitor_count_output['Return Code'] != 0:
        print('Monitors Supported Count: Information Not Available')
        return('Information Not Available')
    monitor_list = monitor_count_output['Output'].splitlines()
    print(f'Monitors Supported Count: {len(monitor_list)}')
    return len(monitor_list)

def Get_Monitor_Logical_Name():
    lshw_output = Run_Command('sudo lshw -C display')
    if lshw_output['Return Code'] != 0:
        return('Information Not Available')
    search_object = re.findall('^\s+logical name:.+', lshw_output['Output'], re.M)
    if len(search_object) == 0:
        return ('Information Not Available')
    logical_name = search_object[0]
    logical_name = logical_name.replace('logical name:', '')
    logical_name = logical_name.replace('/dev/', '')
    logical_name = logical_name.lstrip()
    return(logical_name)
 
def Get_Monitor_Resolution():
    logic_name = Get_Monitor_Logical_Name()
    if logic_name == 'Information Not Available':
        print('Monitor Resolution: Information Not Available')
        return 'Information Not Available'
    resolution = Run_Command(f'cat /sys/class/graphics/{logic_name}/virtual_size')
    resolution['Output'] = resolution['Output'].strip()
    print(f'Monitor Resolution: {resolution["Output"]}')
    return(resolution['Output'])
    
def Get_Bits_Per_Pixel():
    logic_name = Get_Monitor_Logical_Name()
    if logic_name == 'Information Not Available':
        print('Monitor Bit per Pixel: Information Not Available')
        return 'Information Not Available'
    
    b_p_p = Run_Command(f'cat /sys/class/graphics/{logic_name}/bits_per_pixel')
    if b_p_p['Return Code'] != 0:
        print('Monitor Bits per Pixel: Information Not Available')
        return('Information Not Available')
    b_p_p['Output'] = b_p_p['Output'].strip()
    print(f'Monitor Bits per Pixel: {b_p_p["Output"]}')
    return(b_p_p['Output'])
#END OF MONITOR INFORMATION

# ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ MAIN LOGIC ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
def main():
    print('============================== Linux System Information Script ==============================')
    date = datetime.today().strftime('%m-%d-%Y, %H:%M:%S')
    print(f'Start Time: {date}\n')
    Log_Error.counter = 0

    if (Is_Linux() == False):
        print('OS on this system is NOT LINUX. Run this script on a LINUX system. Exiting the LSIS Script')
        exit()
    print('OS on this system is LINUX!')


    #Create Log File For Logging Errors with Commands
    error_logging_file = open(error_logging_file_name, 'w')
    error_logging_file.write('========== Linux System Information Script ERRORS ==========\n\n')
    error_logging_file.write(f'Start Time: {date}\n')
    error_logging_file.close()

    #XML File Creation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    root = lsis.Element('LSIS')

    #Title Element
    title_element = lsis.SubElement(root,'Title')
    title_element.text = 'Linux System Information Script'


    #Time Element
    time_element = lsis.SubElement(root,'Time')
    time_element.text = f'{date}'

    #System Information
    system_info_element = lsis.SubElement(root,'Section', attrib={"name":"System Information"}) #Section Name = System Information

    #APU
    print('\nAPU Information ~~ ~~ ~~ ~~ ~~ ~~')
    apu_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"APU"})

    cpu_name_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"CpuName"})
    cpu_name_block.text = Get_CPU_Name()

    cpu_info_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"CpuInfo"})
    cpu_info_block.text = Get_CPU_Info()

    cores_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"Cores"})
    cores_block.text = Get_Core_Count()

    logical_processors_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"LogicalProcessors"})
    logical_processors_block.text = Get_Logical_Processors()

    memory_size_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"MemorySize"})
    memory_size_block.text = Get_Total_Memory()

    memory_info_block = lsis.SubElement(apu_block, 'Info', attrib={"name":"MemoryInfo"})
    memory_info_block.text = Get_Memory_Info()

    # Baseboard Information
    print('\nBaseboard Information ~~ ~~ ~~ ~~ ~~ ~~')
    baseboard_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"Baseboard"})

    product_name_block = lsis.SubElement(baseboard_block, 'Info', attrib={"name":"ProductName"})
    product_name_block.text = Get_Product_Name()

    sku_block = lsis.SubElement(baseboard_block, 'Info', attrib={"name":"SKU"})
    sku_block.text = Get_Board_SKU()

    board_version_block = lsis.SubElement(baseboard_block, 'Info', attrib={"name":"Version"})
    board_version_block.text = Get_Board_Version()

    board_manufacturer_block = lsis.SubElement(baseboard_block, 'Info', attrib={"name":"Manufacturer"})
    board_manufacturer_block.text = Get_Board_Manufacturer()

    battery_block = lsis.SubElement(baseboard_block, 'Info', attrib={"name":"BatteryInfo"})
    battery_block.text = Get_Battery_Info()

    #Cache
    print('\nCache Information ~~ ~~ ~~ ~~ ~~ ~~')
    cache_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"Cache"})

    l1_block = lsis.SubElement(cache_block, 'Info', attrib={"name":"L1"})
    l1_block.text = Get_L1_Cache()

    l2_block = lsis.SubElement(cache_block, 'Info', attrib={"name":"L2"})
    l2_block.text = Get_L2_Cache()

    l3_block = lsis.SubElement(cache_block, 'Info', attrib={"name":"L3"})
    l3_block.text = Get_L3_Cache()

    #Storage
    print('\nStorage Information ~~ ~~ ~~ ~~ ~~ ~~')
    storage_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"Storage"})

    alpm_block = lsis.SubElement(storage_block, 'Info', attrib={"name":"ALPMSetting"})
    alpm_block.text = Get_ALPM_Mode()


    #OS
    print('\nOS Information ~~ ~~ ~~ ~~ ~~ ~~')
    os_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"OS"})

    os_version_block = lsis.SubElement(os_block, 'Info', attrib={"name":"Version"})
    os_version_block.text = Get_OS_Version()

    #BIOS
    print('\nBIOS Information ~~ ~~ ~~ ~~ ~~ ~~')
    bios_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"BIOS"})

    bios_version_block = lsis.SubElement(bios_block, 'Info', attrib={"name":"Version"})
    bios_version_block.text = Get_BIOS_Info()

    #USB
    print('\nUSB Information ~~ ~~ ~~ ~~ ~~ ~~')
    usb_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"USB"})

    usb_output = Get_USB()
    usb_device_list = usb_output.splitlines()

    for device in usb_device_list:
        usb_address = re.findall('^Bus\s+\w.+Device\s+\w+:\s+\w+\s+\w+:\w+\s+', device, re.M)
        usb_device_name = re.split('^Bus\s+\w.+Device\s+\w+:\s+\w+\s+\w+:\w+\s+', device, re.M)
        
        usb_device_block = lsis.SubElement(usb_block, 'Info', attrib={"name":usb_address[0]})
        usb_device_block.text = usb_device_name[1]

    #PCI
    print('\nPCI Information ~~ ~~ ~~ ~~ ~~ ~~')
    pci_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"PCI"})

    pci_output = Get_PCI()
    pci_device_list = pci_output.splitlines()

    for device in pci_device_list:
        pci_address = re.findall('\w+:\w+.\w+\s+', device, re.M)
        pci_device_name = re.split('\w+:\w+.\w+\s+', device, re.M)
        #print(f'ADDRESS: {pci_address[0]} DEVICE NAME: {pci_device_name[1]}')
        
        pci_device_block = lsis.SubElement(pci_block, 'Info', attrib={"name":pci_address[0]})
        pci_device_block.text = pci_device_name[1]

    #Graphics
    print('\nGraphics Information ~~ ~~ ~~ ~~ ~~ ~~')
    graphics_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"Graphics"})

    adapter_block = lsis.SubElement(graphics_block, 'Info', attrib={"name":"Adapter Name"})
    adapter_block.text = Get_Adapter_Name()

    pci_address_block = lsis.SubElement(graphics_block, 'Info', attrib={"name":"PCI Address"})
    pci_address_block.text = Get_PCI_Address()

    driver_block = lsis.SubElement(graphics_block, 'Info', attrib={"name":"Driver Info"})
    driver_block.text = Get_Driver()

    clock_info_block = lsis.SubElement(graphics_block, 'Info', attrib={"name":"Clock Info"})
    clock_info_block.text = Get_Clock()

    vram_block = lsis.SubElement(graphics_block, 'Info', attrib={"name":"VRAM Size"})
    vram_block.text = Get_VRAM()

    #MONITORS
    print('\nMonitors Information ~~ ~~ ~~ ~~ ~~ ~~')
    monitors_block = lsis.SubElement(system_info_element,'Panel',attrib={"name":"Monitors"})

    monitors_count_block = lsis.SubElement(monitors_block, 'Info', attrib={"name":"Monitors Supported"})
    monitors_count_block.text = str(Get_Monitor_Support_Count())

    monitor_logical_name_block = lsis.SubElement(monitors_block, 'Info', attrib={"name":"Monitor Logical Name"})
    monitor_logical_name_block.text = Get_Monitor_Logical_Name()

    resolution_block = lsis.SubElement(monitors_block, 'Info', attrib={"name":"Monitor Resolution"})
    resolution_block.text = Get_Monitor_Resolution()

    b_p_p_block = lsis.SubElement(monitors_block, 'Info', attrib={"name":"Bits per Pixel"})
    b_p_p_block.text = Get_Bits_Per_Pixel()


    #Create The Tree (Older Python Versions Can't Use indent function)
    print('\nGenerating the XML File Now ~~ ~~ ~~ ~~ ~~ ~~')
    tree = lsis.ElementTree(root)
    xmlstr = minidom.parseString(lsis.tostring(root)).toprettyxml(indent="   ")
    with open(xml_output_file_name, "w") as file:
        file.write(xmlstr)

    print(f'\n\n~--~--~--~-- ERRORS LOGGED: {Log_Error.counter} --~--~--~--~')


if __name__ == '__main__':
    main()