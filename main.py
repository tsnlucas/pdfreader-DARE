import wx
from PDFReaderApp import PDFReaderApp
app = wx.App()
PDFReaderApp(None, -1, 'Leitor de PDF')
app.MainLoop()
