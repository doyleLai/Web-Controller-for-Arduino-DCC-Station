def speedcontrol(addr: int, dir: int, speed:int) -> str:
    if addr < 10 and dir < 3 and speed < 128:
        return f'<S{addr}{dir}{speed:03}>'
    else:
        return None

def functioncontrol(addr: int, func: int, isOn:bool) -> str:
    if addr < 10 and func < 100:
        return f'<F{addr}{func:02}{"1" if isOn else "0"}>'
    else:
        return None