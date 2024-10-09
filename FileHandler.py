import os

class FileHandler:
    @staticmethod
    def write_text_to_file(file_path, text):
        with open(file_path, "w") as output_file:
            output_file.write(text)
    
    @staticmethod
    def open_text_file_in_notepad(file_path):
        os.system(f'start notepad.exe {file_path}')
