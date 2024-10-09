import wx
import fitz
import os
import subprocess

class PDFReaderApp(wx.Frame):
    def __init__(self, parent, id, title):
        super().__init__(parent, id, title, size=(800, 600))

        self.selected_files = []
        self.extracted_info = {}

        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)

        self.pdf_list_page = wx.Panel(self.notebook)
        self.info_page = wx.Panel(self.notebook)

        self.pdf_list_box = wx.ListBox(self.pdf_list_page, choices=[], style=wx.LB_SINGLE)
        self.pdf_list_box.Bind(wx.EVT_LISTBOX, self.display_info)
        self.pdf_list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.open_selected_pdf)
        self.pdf_list_sizer = wx.BoxSizer(wx.VERTICAL)
        self.pdf_list_sizer.Add(self.pdf_list_box, 1, flag=wx.EXPAND | wx.ALL, border=10)
        self.pdf_list_page.SetSizer(self.pdf_list_sizer)

        self.info_text = wx.TextCtrl(self.info_page, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.info_text_sizer = wx.BoxSizer(wx.VERTICAL)
        self.info_text_sizer.Add(self.info_text, 1, flag=wx.EXPAND | wx.ALL, border=10)
        self.info_page.SetSizer(self.info_text_sizer)

        self.notebook.AddPage(self.pdf_list_page, "Lista de PDFs")
        self.notebook.AddPage(self.info_page, "Informações")
        
        open_button = wx.Button(self.panel, label="Abrir PDFs")
        open_button.Bind(wx.EVT_BUTTON, self.openPDFs)

        save_button = wx.Button(self.panel, label="Salvar Informações")
        save_button.Bind(wx.EVT_BUTTON, self.saveInfo)

        open_txt_button = wx.Button(self.panel, label="Abrir Arquivo TXT")
        open_txt_button.Bind(wx.EVT_BUTTON, self.openTxtFile)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(open_button, 0, flag=wx.ALL, border=10)
        hbox.Add(save_button, 0, flag=wx.ALL, border=10)
        hbox.Add(open_txt_button, 0, flag=wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.notebook, 1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(hbox, 0, flag=wx.ALIGN_CENTER)

        self.panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def extract_info_from_pdf(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        extracted_info = {}
        current_field = None

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text().splitlines()

            for line in text:
                # Procura os campos específicos e extrai o texto diretamente abaixo deles
                if "01 - Nome / Razão Social" in line:
                    current_field = "Nome / Razão Social"
                elif "07 - Data de Vencimento" in line:
                    current_field = "Data de Vencimento"
                elif "09 - Número do DARE" in line:
                    current_field = "Número do DARE"
                elif current_field and line.strip():
                    extracted_info[current_field] = line.strip()
                    current_field = None

        pdf_document.close()
        return extracted_info

    def openPDFs(self, event):
        dialog = wx.FileDialog(self, "Abrir PDFs", "", "", "PDF Files (*.pdf)|*.pdf", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if dialog.ShowModal() == wx.ID_OK:
            self.selected_files = dialog.GetPaths()
            self.pdf_list_box.Clear()
            for pdf_path in self.selected_files:
                self.pdf_list_box.Append(pdf_path)

            # Pergunta onde salvar o arquivo .txt
            self.saveInfo(None)

        dialog.Destroy()

    def display_info(self, event):
        selected_item = self.pdf_list_box.GetSelection()
        if selected_item != wx.NOT_FOUND:
            pdf_path = self.selected_files[selected_item]
            self.extracted_info[pdf_path] = self.extract_info_from_pdf(pdf_path)
            pdf_filename = os.path.basename(pdf_path)

            info_text = f'Arquivo: {pdf_filename}\n'
            for key, value in self.extracted_info[pdf_path].items():
                info_text += f"{key}: {value}\n"
            self.info_text.SetValue(info_text)

    def open_selected_pdf(self, event):
        selected_item = self.pdf_list_box.GetSelection()
        if selected_item != wx.NOT_FOUND:
            pdf_path = self.selected_files[selected_item]
            os.system(f'start {pdf_path}')

    def saveInfo(self, event):
        if self.selected_files:
            dialog = wx.FileDialog(self, "Salvar Arquivo", "", "", "Text Files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if dialog.ShowModal() == wx.ID_OK:
                output_filepath = dialog.GetPath()
                with open(output_filepath, "w") as output_file:
                    for pdf_path in self.selected_files:
                        extracted_info = self.extract_info_from_pdf(pdf_path)
                        pdf_filename = os.path.basename(pdf_path)

                        output_file.write(f'Arquivo: {pdf_filename}\n')
                        for key, value in extracted_info.items():
                            output_file.write(f"{key}: {value}\n")
                        output_file.write("--------------\n")

                wx.MessageBox("Informações salvas com sucesso!", "Salvo", wx.OK | wx.ICON_INFORMATION)

                # Abre o arquivo .txt automaticamente usando o subprocess
                subprocess.Popen(['notepad.exe', output_filepath])

            dialog.Destroy()

    def openTxtFile(self, event):
        dialog = wx.FileDialog(self, "Abrir Arquivo TXT", "", "", "Text Files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            txt_filepath = dialog.GetPath()
            subprocess.Popen(['notepad.exe', txt_filepath])

        dialog.Destroy()

app = wx.App()
PDFReaderApp(None, -1, 'Leitor de PDF')
app.MainLoop()
