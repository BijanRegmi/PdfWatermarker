import tkinter as tk, os, PyPDF2, time
from tkinter import filedialog,ttk,messagebox

class scrollwindow:
    def __init__(self,parent,**kwargs):
        canvas = tk.Canvas(parent, **kwargs)
        scrollbar = tk.Scrollbar(parent, orient = "vertical", command = canvas.yview)
        self.scrollframe = tk.Frame(canvas, **kwargs)

        self.scrollframe.bind("<Configure>",lambda x: canvas.configure(scrollregion = canvas.bbox("all")))
        canvas.create_window((0,0), window = self.scrollframe, anchor = "nw")
        canvas.configure(yscrollcommand = scrollbar.set)
        
        canvas.pack(side = "left", fill = "both")
        scrollbar.pack(side = "right", fill = "y")


def merge():
    num = len(pdf_files)
    try:
        bar["maximum"] = num
        watermark_reader = PyPDF2.PdfFileReader(watermark_field.get()).getPage(0)
        for num,file in enumerate(pdf_files):
            reader = PyPDF2.PdfFileReader(file)
            writer = PyPDF2.PdfFileWriter()

            for pagenum in range(reader.numPages):
                page = reader.getPage(pagenum)
                page.mergePage(watermark_reader)
                writer.addPage(page)

            with open(f"{os.path.splitext(file)[0]}_watermarked.pdf", "wb") as fi:
                writer.write(fi)
            bar["value"] = num + 1
            bar.update()
            time.sleep(1)
        messagebox.showinfo("Completed", f"Process Completed!\nAdded watermarks on {num+1} files")
    except:
        messagebox.showerror("Error", "OOPS! Something went wrong.")

def addwatermark():
    x = filedialog.askopenfilename(title = "Select your watermark pdf file", filetypes = (("Pdf FIle","*.pdf"), ("All Files","*.*")))
    if x != "":
        watermark_field.configure(state = "normal")
        watermark_field.delete(0, tk.END)
        watermark_field.insert(0, x)
        watermark_field.configure(state = "readonly")

def addfile():
    x = filedialog.askopenfilenames(title = "Select your pdf files", filetypes = (("Pdf FIle","*.pdf"), ("All Files","*.*")))
    if x != ():
        for y in x:
            pdf_files.append(y)
            tk.Label(frame, text = y, bg = "grey", anchor = "w", padx = 10).pack(fill = "both")

def resetfile():
    global pdf_files
    pdf_files = []
    for child in frame.winfo_children():
        child.destroy()
        

pdf_files = []
root = tk.Tk()
root.title("PDF WATERMARKER")
root.iconphoto(True, tk.PhotoImage(file = "icon.png"))

files = tk.LabelFrame(root, text = "Files to have watermark on", padx = 15, pady = 10)
files.grid(row = 1, column = 0, padx = 5, pady = 5)

file_add = tk.Button(files, text = "Load", command = addfile)
file_add.grid(row = 0, column = 1, padx = 10)

file_reset = tk.Button(files, text = "Reset", command = resetfile)
file_reset.grid(row = 1, column = 1, padx = 10)

loaded_files = tk.LabelFrame(files, text = "Loaded Files", padx = 5, pady = 5)
loaded_files.grid(row = 0, column = 0, rowspan = 2)

scroll = scrollwindow(loaded_files, bg = "grey")
frame = scroll.scrollframe

watermark = tk.LabelFrame(root, text = "Add watermark PDF file", padx = 10, pady = 10)
watermark.grid(row = 0, column = 0, pady = 5, padx = 5)

watermark_field = tk.Entry(watermark, width = 53, state = "readonly")
watermark_field.grid(row = 0, column = 0)

watermark_add = tk.Button(watermark, text = "Load", command = addwatermark)
watermark_add.grid(row = 0, column = 1, padx = 2)

but = tk.Button(root, text = "EXECUTE", command = merge)
but.grid(row = 2, column = 0, pady = 5)

bar = ttk.Progressbar(root, length = 525)
bar.grid(row = 3, column = 0, pady = 5, padx = 10)

root.mainloop()