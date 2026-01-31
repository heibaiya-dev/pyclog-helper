import os
import threading
from datetime import datetime
from typing import Optional
from pathlib import Path

from .config import LogConfig, Validate_Config
from .formatter import LogFormatter


class FileHandler:
    def __init__(self, config: LogConfig, formatter: LogFormatter):
        Validate_Config(config)
        self.config = config
        self.formatter = formatter
        self._lock = threading.Lock()
        self._current_file_path = self._Get_Current_File_Path()
        
        if config.auto_create_directory:
            self._Create_Directory_If_Not_Exists()

    def Write_Log(self, message: str) -> bool:
        try:
            with self._lock:
                self._Check_And_Perform_Rotation()
                with open(self._current_file_path, 'a', encoding=self.config.encoding) as f:
                    f.write(message + '\n')
                return True
        except Exception as e:
            print(f"Error writing log: {e}")
            return False

    def _Create_Directory_If_Not_Exists(self) -> None:
        log_dir = os.path.dirname(self._current_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _Get_Current_File_Path(self) -> str:
        if self.config.enable_date_rotation:
            date_str = datetime.now().strftime(self.config.date_format)
            base_name = os.path.splitext(self.config.log_file_path)[0]
            extension = os.path.splitext(self.config.log_file_path)[1]
            return f"{base_name}_{date_str}{extension}"
        return self.config.log_file_path

    def _Check_And_Perform_Rotation(self) -> None:
        if self.config.enable_date_rotation:
            self._Check_Date_Rotation()
        
        if self.config.max_file_size > 0:
            self._Check_Size_Rotation()

    def _Check_Date_Rotation(self) -> None:
        new_file_path = self._Get_Current_File_Path()
        if new_file_path != self._current_file_path:
            self._current_file_path = new_file_path
            if self.config.auto_create_directory:
                self._Create_Directory_If_Not_Exists()

    def _Check_Size_Rotation(self) -> None:
        if not os.path.exists(self._current_file_path):
            return
        
        file_size = os.path.getsize(self._current_file_path)
        if file_size >= self.config.max_file_size:
            self._Rotate_Files()

    def _Rotate_Files(self) -> None:
        try:
            for i in range(self.config.backup_count - 1, 0, -1):
                old_file = f"{self._current_file_path}.{i}"
                new_file = f"{self._current_file_path}.{i + 1}"
                if os.path.exists(old_file):
                    if os.path.exists(new_file):
                        os.remove(new_file)
                    os.rename(old_file, new_file)
            
            backup_file = f"{self._current_file_path}.1"
            if os.path.exists(backup_file):
                os.remove(backup_file)
            
            if os.path.exists(self._current_file_path):
                os.rename(self._current_file_path, backup_file)
        except Exception as e:
            print(f"Error rotating log files: {e}")

    def Get_Log_File_Path(self) -> str:
        return self._current_file_path

    def Flush(self) -> None:
        pass

    def Close(self) -> None:
        pass


class RotatingFileHandler(FileHandler):
    def __init__(self, config: LogConfig, formatter: LogFormatter):
        super().__init__(config, formatter)
        self._file_handle = None
        self._Open_File()

    def _Open_File(self) -> None:
        try:
            mode = 'a' if os.path.exists(self._current_file_path) else 'w'
            self._file_handle = open(self._current_file_path, mode, encoding=self.config.encoding)
        except Exception as e:
            print(f"Error opening log file: {e}")
            self._file_handle = None

    def Write_Log(self, message: str) -> bool:
        try:
            with self._lock:
                self._Check_And_Perform_Rotation()
                if self._file_handle:
                    self._file_handle.write(message + '\n')
                    self._file_handle.flush()
                return True
        except Exception as e:
            print(f"Error writing log: {e}")
            return False

    def _Check_Size_Rotation(self) -> None:
        if not os.path.exists(self._current_file_path):
            return
        
        file_size = os.path.getsize(self._current_file_path)
        if file_size >= self.config.max_file_size:
            self._Close_File()
            self._Rotate_Files()
            self._Open_File()

    def _Check_Date_Rotation(self) -> None:
        new_file_path = self._Get_Current_File_Path()
        if new_file_path != self._current_file_path:
            self._Close_File()
            self._current_file_path = new_file_path
            if self.config.auto_create_directory:
                self._Create_Directory_If_Not_Exists()
            self._Open_File()

    def Flush(self) -> None:
        if self._file_handle:
            self._file_handle.flush()

    def Close(self) -> None:
        self._Close_File()

    def _Close_File(self) -> None:
        if self._file_handle:
            try:
                self._file_handle.close()
            except Exception as e:
                print(f"Error closing log file: {e}")
            finally:
                self._file_handle = None


class ConsoleHandler:
    def __init__(self, formatter: LogFormatter):
        self.formatter = formatter
        self._lock = threading.Lock()

    def Write_Log(self, message: str) -> bool:
        try:
            with self._lock:
                print(message)
                return True
        except Exception as e:
            print(f"Error writing to console: {e}")
            return False

    def Flush(self) -> None:
        pass

    def Close(self) -> None:
        pass
