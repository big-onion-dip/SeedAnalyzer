import serial.tools.list_ports

def list_serial_ports():
    return [f"{port.device} - {port.description}" for port in serial.tools.list_ports.comports()]

def save_weight_to_txt(weight, base_name, out_dir):
    if not base_name:
        raise ValueError("请先拍照以生成对应文件名")
    txt_path = f"{out_dir}/{base_name}_weight.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(str(weight))
    return txt_path