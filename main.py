import tensorflow as tf
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
import requests
from tqdm import tqdm


class Root(tk.Tk):
    def __init__(self):
        super(Root, self).__init__()

        try:
            self.model = tf.keras.models.load_model("age_detect.h5")
        except OSError:
            url = "http://b98766hs.beget.tech/age_detector/age_detect.h5"
            response = requests.get(
                url,
                stream=True,
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
            )
            downloading_progress_bar = tqdm(
                desc="Downloading model",
                total=int(response.headers.get('content-length', 0)),
                unit='iB',
                unit_scale=True
            )
            with open("age_detect.h5", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        downloading_progress_bar.update(len(chunk))
                        file.write(chunk)
            self.model = tf.keras.models.load_model("age_detect.h5")

        self.title("Age Detect")
        self.minsize(400, 300)
        self.resizable(width=False, height=False)
        self.imageLabel = tk.Label(self)
        self.imageLabel.pack()
        self.output = tk.Label(self, text="Age Detect", font=("Tahoma", 16))
        self.output.pack()
        self.age_detect_button = tk.Button(
            self,
            text="Open image and detect age",
            command=self.age_detect,
            font=("Tahoma", 12)
        )
        self.age_detect_button.pack()

    def age_detect(self):
        image = Image.open(fd.askopenfilename())
        image = image.resize((224, 224))
        image_tk = ImageTk.PhotoImage(image)
        self.imageLabel.config(image=image_tk)
        self.imageLabel.image = image_tk
        image = np.array(image) / 255
        image = np.array([image])
        self.output.config(text=f"Age: {int(self.model.predict(image))}")


root = Root()
root.mainloop()
