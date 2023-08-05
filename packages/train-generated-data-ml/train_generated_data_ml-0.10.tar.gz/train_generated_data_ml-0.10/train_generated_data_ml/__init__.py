import os
import subprocess
import sys
from configparser import ConfigParser
import pandas as pd
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed

pd_add_less_memory_more_speed()


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def get_config_dfs(configfile):
    config = ConfigParser()
    config.read(configfile)
    dfgeneral = pd.DataFrame(pd.Series(config.__dict__["_sections"]["TRAINING"]))
    dfgeneral = dfgeneral.T
    for col in dfgeneral:
        try:
            dfgeneral[col] = dfgeneral[col].str.replace("""['"]+""", "", regex=True)
        except Exception as fe:
            pass
    dfgeneral = (
        dfgeneral.ds_string_to_mixed_dtype()
        .ds_reduce_memory_size(verbose=False)
        .ds_reduce_memory_size(verbose=False)
    )
    return dfgeneral


def run_yolov5_training(config_file):
    df = get_config_dfs(configfile=config_file)

    model_file = df.model_file.iloc[0]
    personal_yaml = df.personal_yaml.iloc[0]
    hypfile = df.hypfile.iloc[0]
    resolutionsize = df.resolutionsize.iloc[0]
    batch = df.batch.iloc[0]
    epochs = df.epochs.iloc[0]
    ptfile = df.ptfile.iloc[0]
    workers = df.workers.iloc[0]
    generated_pic_folder = df.generated_pic_folder.iloc[0]
    yolovyamel = os.path.join(generated_pic_folder, personal_yaml)
    name_for_set = df.name_for_set.iloc[0]
    save_period = df.save_period.iloc[0]

    allyolofiles = [
        x
        for x in getListOfFiles(
            dirName=os.path.join(os.path.abspath(os.path.dirname(__file__)))
        )
        if "yolo" in x
    ]

    trainpy = [x for x in allyolofiles if (rf"yolov5{os.sep}train.py") in x][0]
    nanomodel = [x for x in allyolofiles if (rf"models{os.sep}{model_file}") in x][0]
    hypfile = [x for x in allyolofiles if (hypfile) in x][0]
    subprocess.run(
        [
            "python",
            trainpy,
            "--img",
            str(resolutionsize),
            "--cfg",
            nanomodel,
            "--hyp",
            hypfile,
            "--batch",
            str(batch),
            "--epochs",
            str(epochs),
            "--data",
            yolovyamel,
            "--weights",
            ptfile,
            "--workers",
            str(workers),
            "--name",
            name_for_set,
            "--save-period",
            str(save_period),
        ]
    )

def print_config_file():
    r"""

    Example of a config file;

    [GENERAL] #not necessary for training data
    image_background_folder="C:\Users\Gamer\anaconda3\envs\dfdir\alltrainingdata"
    image_button_folder = "C:\yolovtest\buttonimages"
    save_path_generated_pics = "C:\trainingset\generated_pics"
    save_path_generated_pics_separate = "C:\trainingset\generated_pics_sep"
    maximum_buttons_on_pic=3
    number_of_pictures_to_generate=100
    max_overlapping_avoid=50000
    yaml_file="royal_halloween.yaml"

    [TRAINING]
    model_file ='yolov5s.yaml'
    personal_yaml="royal_halloween.yaml"
    hypfile = "hyp.scratch-low.yaml"
    resolutionsize=640
    batch=30
    epochs=4
    ptfile="C:\Users\Gamer\anaconda3\envs\dfdir\yolov5\yolov5s.pt"
    workers=4
    generated_pic_folder = "C:\trainingset\generated_pics_sep"
    name_for_set = "royal_halloweennew"
    save_period=10


    [BUTTON0] #not necessary for training data
    class_name="play_apple_game"
    allowed_min_distance_from_zero_x=1
    allowed_min_distance_from_zero_y=1
    allowed_max_distance_from_zero_x=70
    allowed_max_distance_from_zero_y=70
    max_x=25
    max_y=25
    min_x=15
    min_y=15
    transparency_min=1
    transparency_max=50
    max_negativ_rotation=-10
    max_positiv_rotation=10
    add_pixelboarder=1
    add_pixelboarder_percentage=10
    unsharp_border=1
    unsharp_border_percentage=10
    random_crop=1
    random_crop_percentage=30
    random_crop_min=0
    random_crop_max=2
    random_blur=1
    random_blur_percentage=20
    random_blur_min=0.001
    random_blur_max=0.05


    [BUTTON1] #not necessary for training data
    class_name="won_apples"
    allowed_min_distance_from_zero_x=1
    allowed_min_distance_from_zero_y=1
    allowed_max_distance_from_zero_x=70
    allowed_max_distance_from_zero_y=70
    max_x=50
    max_y=50
    min_x=40
    min_y=40
    transparency_min=1
    transparency_max=10
    max_negativ_rotation=-10
    max_positiv_rotation=10
    add_pixelboarder=1
    add_pixelboarder_percentage=10
    unsharp_border=1
    unsharp_border_percentage=10
    random_crop=0
    random_crop_percentage=30
    random_crop_min=0
    random_crop_max=1
    random_blur=0
    random_blur_percentage=10
    random_blur_min=0.001
    random_blur_max=0.05


    Explanation

    Download https://github.com/ultralytics/yolov5 to /yolov5/ in your env, install all requirements
    [GENERAL] image_background_folder - folder where your background images are located
    [GENERAL] image_button_folder - folder where the buttons that you want to detect are located. Each button can have several different images. Each button's images must be in it's own folder. Folders must be consecutively numbered
    [GENERAL] save_path_generated_pics - Temp folder for generated files
    [GENERAL] save_path_generated_pics_separate - Finished generated training data
    [GENERAL] maximum_buttons_on_pic - Max number of random buttons on a generated image
    [GENERAL] number_of_pictures_to_generate - Total number of training images
    [GENERAL] max_overlapping_avoid - Number of times to try to not overlap buttons (if maximum_buttons_on_pic > 1)
    [GENERAL] yaml_file - choose a filename with ending '.yaml', e.g. 'mygeneratedfiles.yaml'
    [TRAINING] model_file - One of https://github.com/ultralytics/yolov5#pretrained-checkpoints  , you might have to download them and put them into the yolov5 folder, maybe they get downloaded automatically
    [TRAINING] personal_yaml - copy what you wrote in [GENERAL] yaml_file
    [TRAINING] hypfile - I usually use "hyp.scratch-low.yaml" - check out the official documentation: https://github.com/ultralytics/yolov5
    [TRAINING] resolutionsize - Use 640, I haven't tested it with other values
    [TRAINING] batch - I use 30 with a RTX 2060 8 GB
    [TRAINING] epochs - 100 is good to start with - check out the official documentation: https://github.com/ultralytics/yolov5
    [TRAINING] ptfile - I start new models with yolov5s.pt and use later my own pretrained files - check out: https://github.com/ultralytics/yolov5#pretrained-checkpoints
    [TRAINING] workers - number of CPUs to use
    [TRAINING] generated_pic_folder - copy what you wrote in [GENERAL] save_path_generated_pics_separate
    [TRAINING] name_for_set - choose name for the set
    [BUTTON0] - each button must have its own section named BUTTON + next consecutively number
    [BUTTON0] class_name - choose a unique class name
    [BUTTON0] allowed_min_distance_from_zero_x - the minimum x distance in percent that the button can show up on the picture
    [BUTTON0] allowed_min_distance_from_zero_y - the minimum y distance in percent that the button can show up on the picture
    [BUTTON0] allowed_max_distance_from_zero_x - the maximum x distance in percent that the button can show up on the picture
    [BUTTON0] allowed_max_distance_from_zero_y - the maximum y distance in percent that the button can show up on the picture
    [BUTTON0] max_x - the max x size of the button in percent relative to the background picture, e.g. if you put 10 and your image has a width of 640, the max x size is 64
    [BUTTON0] max_y - the max y size of the button in percent relative to the background picture
    [BUTTON0] min_x - the min x size of the button in percent relative to the background picture, e.g. if you put 10 and your image has a width of 640, the min x size is 64
    [BUTTON0] min_y - the min y size of the button in percent relative to the background picture
    [BUTTON0] transparency_min  for random transparency, value will be substracted from alpha channel
    [BUTTON0] transparency_max - for random transparency, value will be substracted from alpha channel
    [BUTTON0] max_negativ_rotation - degrees to rotate button for random.randrange
    [BUTTON0] max_positiv_rotation - degrees to rotate button for random.randrange
    [BUTTON0] add_pixelboarder - 1 to enable, 0 to disable (for fuzzy border)
    [BUTTON0] add_pixelboarder_percentage - percentage of images to add the fuzzy border to
    [BUTTON0] unsharp_border - how many percent of the picture should become a fuzzy border (minimum)
    [BUTTON0] unsharp_border_percentage - how many percent of the picture should become a fuzzy border (maximum)
    [BUTTON0] random_crop - 1 to enable, 0 to disable, don't disable it for now, might cause problems
    [BUTTON0] random_crop_percentage - percentage of all images the crop should be applied to
    [BUTTON0] random_crop_min - how many pixels should be cropped (minimum)
    [BUTTON0] random_crop_max - how many pixels should be cropped (maximum)
    [BUTTON0] random_blur - 1 to enable, 0 to disable
    [BUTTON0] random_blur_percentage - percentage of all images the blur should be applied to
    [BUTTON0] random_blur_min - 0.001
    [BUTTON0] random_blur_max - 0.005

    """

if __name__ == "__main__":
    try:
        run_yolov5_training(config_file=sys.argv[1])
    except Exception:
        print('There is something wrong! Is your config file okay?')
        print_config_file()