# Batch Model Merger

Python based application to automate the creation of model checkpoint merges. Supports various interpolation models in an
attempt to smooth the transition between merge steps. (Also supports the typical weighted average model).

Automated installation is provided for Windows users of [Automatic's Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

## Installation

### Automated Windows Installation

- Save [install.bat](https://raw.githubusercontent.com/lodimasq/batch-model-merge/master/create_shortcut.bat) (Right Click > Save As) into your
"stable-diffusion-webui" folder
- Run `install.bat` which will carry out the below steps:
  - Activate existing venv
  - Install the batch_model_merger package via pip
  - Create a shortcut in your "stable-diffusion-webui" directory named "Batch Model Merger"
  - Deletes itself
- Run the shortcut "Batch Model Merger" to start the application

### Manual Installation for Windows

- Activate your chosen `venv`
- `pip install batch-checkpoint-merger`
- Navigate to `Lib\site-packages\batch_checkpoint_merger` inside your `venv`
- Rename `batch_checkpoint_merger.py` to `batch_checkpoint_merger.pyw`
- Create a shortcut for the `.pyw` file and move it to somewhere convenient

If you do not want to install it as a pip package, there is a requirements.txt file in the repo for you to install dependencies from.

### Manual Installation for Linux/Mac

## Usage

### Bat file Method for Windows Users

If you are using Windows and [Automatics Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which I highly recommend, the easiest way to use this script is to use the .bat file.

- Download this repo as a zip file
- Extract the folder and place it in the main folder of your stable-diffusion install
  - Copy the two models you want to merge into the folder you just created
  - Run `merge.bat`
  - The .bat file should guide you through the merge process

### Running merge.py Directly

If you aren't using Automatic's web UI or are comfortable with the command line, you can also run `merge.py` directly.
Just like with the .bat method, I'd recommend creating a folder within your stable-diffusion installation's main folder. This script requires torch to be installed, which you most likely will have installed in a venv inside your stable-diffusion webui install.

- Navigate to the merge folder in your terminal
- Activate the venv
  - For users of Automatic's Webui use
    - `..\venv\Scripts\activate`
  - For users of [sd-webui](https://github.com/sd-webui/stable-diffusion-webui) (formerly known as HLKY) you should just be able to do
    - `conda activate ldm`
- run merge.py with arguments
  - `py merge.py model0 model1 --alpha 0.5 --output merged`
    - Optional: `--alpha` controls how much weight is put on the second model. Defaults to 0.5, if omitted
    - Optional: `--output` is the filename of the merged file, without file extension. Defaults to "merged", if omitted
    - Optional: `--device` is the device that's going to be used to merge the models. Unless you have a ton of VRAM, you should probably just ignore this. Defaults to 'cpu', if omitted.
      - Required VRAM seems to be roughly equivalent to the size of `(size of both models) * 1.15`. Merging 2 models at 3.76GB resulted in rougly 8.6GB of VRAM usage on top of everything else going on.
      - If you have enough VRAM to merge on your GPU you can use `--device "cuda:x"` where x is the card corresponding to the output of `nvidia-smi -L`

## Potential Problems & Troubleshooting

- Depending on your operating system and specific installation of python you might need to replace `py` with `python`, `python3`, `conda` or something else entirely.

## Credits

- Thanks to Automatic and his fantastic Webui, I stole some of the code for the `merge.bat` from him.
- I got the merging logic in `merge.py` from [this post](https://discord.com/channels/1010980909568245801/1011008178957320282/1018117933894996038) by r_Sh4d0w, who seems to have gotten it from [mlfoundations/wise-ft](https://github.com/mlfoundations/wise-ft)

![img_1.png](img_1.png)