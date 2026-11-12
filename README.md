# Rubik Web Solver

A web-based Rubik's Cube solver that uses a webcam to scan the six faces of a 3×3 Rubik's Cube, recognize sticker colors, and generate a solving sequence.

## Features

- Webcam-based scanning of Rubik's Cube faces
- Sticker color recognition using OpenCV
- Cube-state validation and solving
- Step-by-step solving sequence

## Technologies

- Python
- Flask
- OpenCV
- NumPy
- Kociemba
- HTML, CSS, and JavaScript

## Project Structure

```text
rubik-web-live/
├── app.py
├── bridge.py
├── cube_solver_final.py
├── requirements.txt
├── Procfile
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    └── index.html
```

> The structure above describes the expected main files. Update it if your repository uses different filenames or folders.

## Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/laVenight21/rubik-web-live.git
   cd rubik-web-live
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\\Scripts\\activate
   ```

   macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open the local address shown in the terminal (commonly `http://127.0.0.1:5000`).

## Computer Vision Method

This project uses traditional computer vision techniques with OpenCV to locate sticker regions and classify sticker colors. Color recognition is based on image processing (such as HSV color ranges), rather than a trained deep-learning model.

The recognized colors are arranged into a cube state, which is then passed to the Kociemba solver to calculate a solution.

## Dataset and Evaluation

The current color-recognition approach does not train a neural-network model, so it does not produce model-weight files such as `.pt`, `.h5`, or `.onnx`.

A separate test dataset can still be prepared to evaluate color recognition. It can contain images of Rubik's Cube stickers in the six color classes:

- Red
- Orange
- Yellow
- Green
- Blue
- White

Include different lighting conditions, camera angles, and image qualities. Record the expected color labels and compare them with the program's predictions. Report evaluation results and examples of recognition errors in the project report.

## Notes

- Recognition quality can be affected by lighting, camera focus, reflections, and webcam quality.
- Make sure the cube is scanned according to the application's on-screen instructions.
- This project is intended for academic and learning purposes.

## License

No license has been specified yet. Contact the repository owner before reusing or distributing this project.
