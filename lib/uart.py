import time
import traceback
from functools import wraps
from queue import Queue
from threading import Thread

import serial

from lib.log_tools import log


class Serial:
    def __init__(self, use_uart):
        self.use_uart = use_uart
        self.ser = serial.Serial() if self.use_uart else ""
        self.uart_thread = None
        self.running = True
        self.buffer_queue = Queue()

    def use_uart(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.use_uart:
                return func(self, *args, **kwargs)

        return wrapper

    def log_oversize_helper(self, fd, size):
        """
        when log file oversize, write to a new file, old log file will be renamed
        Args:
            fd:
            size:

        Returns:

        """
        pass

    @use_uart
    def open_serial(self, port, baudrate="38400"):
        self.ser.port = port
        self.ser.baudrate = int(baudrate)
        self.ser.open()
        if self.ser.is_open:
            log.logger.info(f"serial {port} open success")
            return True
        else:
            log.logger.error(f"serial {port} open fail")
            return False

    @use_uart
    def close_serial(self):
        if self.ser.is_open:
            self.ser.flushOutput()
            if self.running:
                try:
                    self.running = False
                    self.uart_thread.join()
                except:
                    log.logger.error(traceback.format_exc())
            self.ser.close()

    @use_uart
    def write(self, cmd):
        """
        write data to serial
        Args:
            cmd:

        Returns:

        """
        self.ser.write(bytes(cmd, encoding="utf8"))

    @use_uart
    def read_all_data(self):
        return self.ser.read_all()

    @use_uart
    def read_by_size(self, size=1024):
        """
        read data by size
        Args:
            size: data size

        Returns:

        """
        return self.ser.read(size)

    @use_uart
    def read_by_time(self, duration=3):
        """
        read data by time
        Args:
            duration: time in seconds

        Returns:

        """
        if duration <= 0:
            return self.read_by_size(1024)
        buffer = b""
        t0 = time.time()
        while time.time() - t0 < duration:
            buffer += self.ser.read(4)
        return buffer

    def save_data_by_time(self, timeout=30, file_path="data.txt"):
        """
        save data to file by time
        Args:
            file_path:
            timeout:

        Returns:

        """
        t0 = time.time()
        with open(file_path, "wb", encoding="utf-8", errors="replace") as f:
            while time.time() - t0 < timeout:
                f.write(self.ser.read(1024))

    def save_data_until_false(self, file_path="data.txt"):
        """
        save serial data to file until running is False
        Args:
            file_path:

        Returns:

        """
        with open(file_path, "wb", encoding="utf-8", errors="replace") as f:
            while self.running:
                f.write(self.ser.read(1024))

    def recieve_data_to_buffer(self):
        """
        receive data from serial
        Returns:

        """
        buffer = self.buffer_queue
        while self.running:
            buffer.put(self.ser.read(1024))

    def write_data_from_buffer(self, filename="data.txt"):
        """
        write data from buffer queue to file
        Args:
            filename:

        Returns:

        """
        with open(filename, "wb", encoding="utf-8", errors="replace") as f:
            while self.running or not self.buffer_queue.empty():
                f.write(self.buffer_queue.get())

    def receive_data_thread(self):
        Thread(target=self.recieve_data_to_buffer).start()
        log.logger.info("receive data to buffer thread start")

    def write_data_thread(self, filename):
        Thread(target=self.write_data_from_buffer, args=(filename,)).start()
        log.logger.info("write data to file thread start")

    def save_data_buffered(self, filename):
        self.receive_data_thread()
        self.write_data_thread(filename)

    @use_uart
    def save_uart_data(self, func, args=(), filename="data.txt", save_opt=0):
        save_func = (self.save_data_until_false, self.save_data_buffered)[save_opt]
        self.running = True
        t = Thread(target=save_func, args=(filename,))
        t.start()
        r = func(*args)
        self.running = False
        t.join()
        return r

    @use_uart
    def start_uart_thread(self, filename, func_opt=0):
        func = (self.save_data_until_false, self.save_data_buffered)[func_opt]
        self.running = True
        self.uart_thread = Thread(target=func, args=(filename,))
        self.uart_thread.start()
        log.logger.info("uart thread start")

    @use_uart
    def stop_uart_thread(self):
        self.running = False
        try:
            self.uart_thread.join()
        except Exception:
            log.logger.error(traceback.format_exc())
        log.logger.info("uart thread stop")
