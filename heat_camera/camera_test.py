from serial import Serial
import matplotlib.pyplot as pyplt
import matplotlib.animation as animation
import numpy as np
import threading

SERIAL_DATA = [0.0] * 64


def im_setup():
    fig, axis = pyplt.subplots()
    serial_data_2d = np.reshape(SERIAL_DATA, (8, 8))
    im = axis.imshow(serial_data_2d, interpolation='nearest',
                     origin='lower',
                     aspect='auto',  # get rid of this to have equal aspect
                     vmin=20,
                     vmax=40,
                     cmap='jet')

    def animate_data(i):
        serial_data_2d = np.reshape(SERIAL_DATA, (8, 8))
        im.set_data(serial_data_2d)
        pyplt.draw()

    ani = animation.FuncAnimation(fig, animate_data, interval=1000)
    pyplt.show(block=True)


def main():
    """ Reads through serial"""
    global SERIAL_DATA
    with Serial('/dev/cu.usbmodem61505401', 115200) as serial:
        while True:
            line = serial.readline()
            serial_data = line.decode("ascii").replace(",", '').replace("[", "").replace("]", "").split()
            serial_data = list(map(float, serial_data))
            if len(serial_data) < 64:
                print("[WARNING] Packet less than 64bits was found")
                continue
            SERIAL_DATA = serial_data


if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
    im_setup()
