# Age detect

Project for detecting person age on images.

[Used Dataset](https://www.kaggle.com/datasets/abhikjha/appa-real-face-cropped)

`train_model.py` and `split_data.ipynb` contains code for training similar model.

## How to launch
1. [Download and install Python](https://www.python.org/downloads/)
2. Clone the GitHub repository: 
```
git clone https://github.com/DogeOk/age_detector.git
```
3. Navigate to the project directory:
```
cd age_detector
```
4. (Recommended) Create a virtual environment to manage Python packages for your project:
```
python -m venv age_detector
```
5. Activate the virtual environment:
   - On Windows:
   ```
   .\venv\Scripts\activate
   ```
   - On macOS and Linux:
   ```
   source venv/bin/activate
   ```
6. Install the required Python packages from `requirements.txt`:
```
pip install -r requirements.txt
```
7. Launch project:
```
python main.py
```
