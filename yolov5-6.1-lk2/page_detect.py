import shutil
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Inspection Items For Critical Parts Of Pigs")
        master.geometry("800x450")

        # 选择图片按钮
        self.select_button = Button(master, text="Select Image",  width=12, height=1, command=self.select_image)
        self.select_button.pack(side=TOP)

        # 检测按钮
        self.detect_button = Button(master, text="Detect",  width=12, height=1, command=self.detect)
        self.detect_button.pack(side=TOP)

        # 显示图片
        self.image_label = Label(master)
        self.image_label.pack(side=LEFT)

        # 显示结果
        self.result_label = Label(master)
        self.result_label.pack(side=RIGHT)



    def select_image(self):
        # 弹出文件选择框，选择图片
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if file_path:
            # 加载图片，并显示
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)

            # 复制图片到指定文件夹下
            os.makedirs("datasets/images/test-1", exist_ok=True)
            file_name = os.path.basename(file_path)
            dest_path = os.path.join("datasets/images/test-1", file_name)
            shutil.copy(file_path, dest_path)

    def detect(self):
        # 调用detect.py，生成结果图片
        subprocess.run(["python", "detect.py", "--source", "", "--weights", "runs/train/exp50/weights/best.pt", "--img-size", "400", "--save-conf"])
        # 指定目录
        dir_path = "runs/detect/exp-test"

        # 遍历目录下的所有文件，获取所有图片文件的完整路径
        image_paths = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                # 获取文件的后缀名
                ext = os.path.splitext(file)[-1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    image_paths.append(os.path.join(root, file))

        # 所有图片文件的完整路径
        for result_path in image_paths:
            # 加载结果图片，并显示
            self.image = Image.open(result_path)
            self.image = self.image.resize((400, 400), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.result_label.config(image=self.photo)

root = Tk()
gui = GUI(root)
root.mainloop()