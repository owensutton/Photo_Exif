#
# Program Name: Photo_Exif
# Original Developer: Owen Sutton
# Description: This program was developed to view the Exif data of photos
#              along with having the option to remove exif data from a photo.
#              Output information is written to Photo_Exif_Results.txt
#              Developed in Python3.
#
# Upcoming enhancements: The ability to edit the exif data and place your own messages inside.
#
# Change Log
#
# Version #   Developer     Date of Change   Description of Change
# ---------   -----------   --------------   ----------------------
# 1.0         Owen Sutton   01/09/2022       New Program
# 1.01        Owen Sutton   01/11/2022       Added the option to write output to the command line instead of file.
# 1.02        Owen Sutton   01/18/2022       Restructured Program
#


# Make sure to install Pillow - see ReadMe for instructions
import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


print("""

________  __    __    ____    _______    ____     ______  __   __   ___   _____   
|  __  | |  |  |  |  /    \  |__   __|  /    \    |  ___  \ \ / /  |_ _| |  ___|
| |__| | |  |__|  | |  __  |   |   |   |  __  |   | |__    \ V /    | |  | |_
|   ___| |   __|  | | |  | |   |   |   | |  | |   |  __|   /   \    | |  |  _|
|  |     |  |  |  | | |__| |   |   |   | |__| |   | |___  / /^\ \   _ _  | |
|__|     |__|  |__|  \____/    |___|    \____/    \_____ /_/   \_\ |___| |_|

Created By: Owen Sutton
Email: Owensutton7@gmail.com

""")

#Checks if the output file exists and delete's it, if it does.
def Check_Output_File():
        # Check if the output file exists.
        Output_file_exists = os.path.exists("Photo_Exif_Results.txt")

        if Output_file_exists == True:
            # Delete output file if it already exists.
            os.remove("Photo_Exif_Results.txt")

        # Create/ move print messages to output file.
        sys.stdout = open("Photo_Exif_Results.txt", "w")

# Check if the Photos folder exists
def Check_Photo_Folder_Exists():
    Photo_folder_exists = os.path.exists("Photos")

    if Photo_folder_exists == False:
        print("Photos Folder does not Exist. Please create a Photos folder and place your pictures inside.")
        exit()


# Choose to view exif data or to remove exif data from photo.
# Warning, once a remove exif data from a photo, you cannot recover it.
while True:
    option = input("Do you want to view, remove, or edit exif data?:\n\n1 - View exif data\n2 - Remove exif data\n3 - Edit exif data\nEnter choice here: ")
    try:
        convert_toInt = int(option)
        if convert_toInt == 1:
            print("View exif data has been selected.")

            while True:
                print("")
                option2 = input("Would you like the output in the command line or a file?:\n\n1 - Output to command line\n2 - Output to file\nEnter choice here: ")
                try:
                    option_toInt = int(option2)
                    if option_toInt == 1:
                        print("")
                        break
                    elif option_toInt == 2:
                        print("Check output file for final results.")
                        break
                    else:
                        print("You have entered an invalid input, please try again.")
                except:
                    print("You have entered an invalid input, please try again.")

            break
        elif convert_toInt == 2:
            print("remove exif data has been selected. Check output file for final results")
            break

        elif convert_toInt == 3:
            print("Edit exif data has been selected.")

            break
        else:
            print("You entered an invalid input, please try again.")

    except:
        print("You have entered an invalid input, please try again.")


#Check if the output file exits, delete if it does.
if option_toInt == 2:
    Check_Output_File()

#Check if any Photo's folder exists.
Check_Photo_Folder_Exists()

# Move current working directory to the Photos folder that contains your photos.
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "Photos"))
files = os.listdir()

# Check if any pictures are in your photos folder
if len(files) == 0:
    print("You don't have any photos located in your photos folder.")
    print("Please move photos into your photos folder and try again.")
    exit()

# loop through each photo that exists in the files folder.
for file in files:
    try:
        # If view exif data was selected
        if convert_toInt == 1:
            viewPhoto = Image.open(file)
            # Check if the file has exif data
            if viewPhoto._getexif() == None:
                print(f"{file}, contains no exif data.")
            else:
                # loop through each of the exif data items, printing them to the output file
                for tag, value in viewPhoto._getexif().items():
                    tag_name = TAGS.get(tag)
                    print(f"{tag_name} - {value}")
        # If remove exi data was selected
        elif convert_toInt == 2:
            removePhoto = Image.open(file)

            # We overwrite the original photo only saving pixel data.
            Photo_data = list(removePhoto.getdata())
            Photo_no_Exif = Image.new(removePhoto.mode, removePhoto.size)
            Photo_no_Exif.putdata(Photo_data)
            Photo_no_Exif.save(file)

            print(f"{file}, exif data successfully removed.")

        else:
            print("error occurred, incorrect option entered.")
            exit()

    except IOError:
        print(f"{file}, file format is not supported!")

# Close output file
if option_toInt == 2:
    sys.stdout.close()

os.chdir(cwd)