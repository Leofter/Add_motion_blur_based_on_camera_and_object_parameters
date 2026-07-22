# Add_motion_blur_based_on_camera_and_object_parameters
Add motion blur on your image or object, based on camera parameters such as: Focal length; Pixel density; resolution; FPS; sensor size. And Object parametrs, such as: object Speed. 

# Add_motion_blur_Interactive_Segmentation
Add motion blur to objects based on physical camera parameters (Focal length, resolution, FPS, sensor size) and object speed, using an interactive UI for object segmentation.

## Prerequisites

Make sure you have Python 3.x installed on your machine.

## 1. Clone the Repository and Access the Folder

Open your terminal or command prompt and run the commands below to download the code to your machine and enter the project directory:

```bash
git clone [https://github.com/your-username/repository-name.git](https://github.com/your-username/repository-name.git)
cd repository-name
```

## 2. Install Dependencies

The code requires two main libraries to work. Choose the installation method according to your preferred package manager.

**Using PIP (Recommended for standard installations):**
```bash
pip install numpy opencv-python
```

**Using Conda (If you use Anaconda or Miniconda environments):**
```bash
conda install numpy opencv
```

## 3. Configure the Parameters

Open the Python script file and change the variables at the top of the code according to your scene specifications.

**Main Parameters:**
*   `CAMINHO_IMAGEM`: The file path and name of your image (e.g., `'carro.jpg'`).
*   `VELOCIDADE_KMH`: The exact speed of the vehicle in the scene, in km/h (e.g., `50.0`).
*   `FPS`: The frame rate of the virtual camera (e.g., `60.0`).
*   `DISTANCIA_OBJETO_M`: The linear distance between the camera and the car in meters (e.g., `15.0`).

**Camera Parameters:**
*   `RESOLUCAO_LARGURA`: Rendered image width in pixels (e.g., `1920`).
*   `LARGURA_SENSOR_MM`: Physical width of the sensor in millimeters (e.g., `13.2` equals a 1" sensor).
*   `DISTANCIA_FOCAL_MM`: The focal length (lens) used for the capture in millimeters (e.g., `50.0`).
*   `ANGULO_OBTURADOR`: The shutter angle that defines the exposure time. The cinematic standard is `180.0`.
*   `ANGULO_MOVIMENTO_GRAUS`: The vector direction of the blur. Leave `0.0` for strictly horizontal motion.

## 4. Running the Script

With all configurations saved, return to your terminal and run the code:

```bash
python apply_motion_blur.py
```

## 5. How to Use the Interface

1. When you run the script, the image will open in a new window.
2. With the mouse, **click, hold, and drag** to draw a tight rectangle around the car only.
3. Release the click and press **Enter** (or Space).
4. The script will automatically segment the object, apply the motion blur exclusively to the car's silhouette, and display the final result.