
# PCB Defect Detection – Milestone 1

## 1. Project Context

This repository contains my work for **Milestone 1** of the “PCB Defect Detection and Classification” internship project.

The main idea in this phase is to use **classical image processing** (no deep learning yet) to compare a defect‑free PCB (golden template) with a test PCB image and automatically highlight the areas where they differ. These regions are the candidate defect locations, which will later be used for dataset creation and CNN training in the next milestones.

---

## 2. Milestone 1 Goals

In simple terms, Milestone 1 is split into two parts:

1. **Defect localisation using image processing (Module 1)**  
   - Build a basic pipeline to:
     - Load a template PCB image and a test PCB image.
     - Align them.
     - Subtract them.
     - Generate a difference map and a binary defect mask.

2. **Preparing data for learning (Module 2 – planned)**  
   - Use DeepPCB annotations to crop defect regions (ROIs).
   - Organise these ROIs into folders according to defect class.
   - This data will be used later when I move to CNN‑based classification.

In this milestone, I focused mainly on getting Module 1 working end‑to‑end and laying the basic structure for Module 2.

---

## 3. Technical Approach

### 3.1 Detection pipeline (Module 1)

Files: `src/processing.py`, `main.py`

For now, I implemented a simple demo using one pair of PCB images: a defect‑free **template** and a **test** image with a “Missing Hole”‑type defect.

The steps are:

1. **Read input images**
   - `read_images(template_path, test_path)`
   - Uses `cv2.imread` to load:
     - a golden template image
     - a test PCB image
   - Basic checks are included to make sure the paths are valid.

2. **Convert to grayscale and align**
   - `to_gray_and_align(template, test)`
   - Converts both images to grayscale using `cv2.cvtColor`.
   - Resizes the test image to match the template size using `cv2.resize`.
   - This ensures that each pixel position corresponds between the two images.

3. **Compute absolute difference**
   - `compute_difference(template_gray, test_gray_resized)`
   - Uses `cv2.absdiff` for pixel‑wise absolute difference:
     - Small differences → dark pixels (background / no defect).
     - Large differences → bright pixels (possible defect).

4. **Otsu thresholding**
   - `threshold_otsu(diff)`
   - Applies `cv2.threshold` with `THRESH_BINARY + THRESH_OTSU`.
   - Otsu automatically chooses a threshold value based on the histogram.
   - Output is a **binary mask**:
     - 0 → non‑defect area
     - 255 → potential defect area

5. **Saving outputs**
   - In `main.py`, the script saves:
     - `template_gray.png` – grayscale template
     - `test_gray_resized.png` – aligned grayscale test image
     - `diff_map.png` – absolute difference map
     - `binary_mask.png` – thresholded defect mask
   - All outputs are written into the `img/` folder.

This pipeline shows that even without deep learning, simple image processing can already highlight clear defects such as missing holes.

---

### 3.2 Planned ROI extraction (Module 2)

File: `src/extraction.py` (to be implemented/extended)

The next step after localising defects is to convert the dataset annotations into actual image crops:

1. **Read annotation files**
   - Parse the DeepPCB ground truth (JSON/XML) that contains:
     - Defect coordinates (bounding boxes).
     - Defect type / category.

2. **Crop ROIs**
   - For each bounding box:
     - Crop the corresponding patch from the PCB image.
     - Save it as a small image.

3. **Organise by class**
   - Store crops into separate folders, for example:
     - `Missing_Hole/`
     - `Mouse_Bite/`
     - `Open_Circuit/`
     - `Short/`
     - etc.
   - This will create a labelled dataset for training a CNN in Milestone 2.

Right now, I have mainly set up the structure for this module and will complete the ROI extraction logic in the next phase.

---

## 4. Repository Structure

Current structure for Milestone 1:

Milestone1/

├── img/
│ ├── Missing_hole_Demonstration_1_Template.jpg # example template image
│ ├── Missing_hole_Demonstration_2_Test.jpg # example test image
│ ├── template_gray.png # saved grayscale template
│ ├── test_gray_resized.png # saved grayscale test
│ ├── diff_map.png # absolute difference map
│ └── binary_mask.png # binary defect mask
├── src/
│ └── processing.py # image loading, grayscale, resize, diff, threshold
├── main.py # simple demo script calling the pipeline
├── requirements.txt # Python dependencies
└── README.md # documentation (this file)



As I extend the project, I will add:
- `src/extraction.py` for ROI cropping
- possibly a `config.py` for paths

---

## 5. How to Run the Demo

### 5.1 Prerequisites

- Python 3.x
- `opencv-python`
- `numpy`

Install dependencies (from inside the `Milestone1` folder):

pip install -r requirements.txt



`requirements.txt` contains:

opencv-python
numpy



### 5.2 Execution

1. Make sure the example PCB images are present in the `img/` folder with these names:
   - `Missing_hole_Demonstration_1_Template.jpg`
   - `Missing_hole_Demonstration_2_Test.jpg`

2. From the `Milestone1` directory, run:

python main.py



3. After execution, check the `img/` folder for:
   - `template_gray.png`
   - `test_gray_resized.png`
   - `diff_map.png`
   - `binary_mask.png`

These images show the different stages of the pipeline for one PCB pair.

---

## 6. Status and Next Steps

Current Milestone 1 status:

- [x] Implemented basic defect localisation using template subtraction and Otsu thresholding.
- [x] Tested the pipeline on a sample “Missing Hole” PCB pair and saved intermediate outputs.
- [ ] Generalise the code to handle multiple image pairs automatically.
- [ ] Implement ROI extraction script for DeepPCB annotations (Module 2).
- [ ] Prepare class‑wise folders of cropped defects for CNN training in the next milestone.

This milestone gives me a working starting point: I can already see where the PCB differs from the golden template, and I have a clear plan for turning those differences into labelled training data.
