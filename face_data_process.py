import base64
import csv
from PIL import Image
import os
import cv2


def read_MS_Celeb_1M(filename, outputDir):
    with open(filename, 'r') as tsvF:
        reader = csv.reader(tsvF, delimiter='\t')
        i = 0
        for row in reader:
            MID, imgSearchRank, faceID, data = row[0], row[1], row[4], base64.b64decode(row[-1])

            saveDir = os.path.join(outputDir, MID)
            savePath = os.path.join(saveDir, "{}-{}.jpg".format(imgSearchRank, faceID))

            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
                # print("makedirs {}".format(saveDir))
            with open(savePath, 'wb') as f:
                f.write(data)

            i += 1
            if i % 1000 == 0:
                print("Extract {} images".format(i))


def video_2_images(video_folder, output_folder):
    img_num = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # loop over each folder
    for subfolder_name in os.listdir(video_folder):
        subfolder_path = os.path.join(video_folder, subfolder_name)

        # loop over each video
        for video_filename in os.listdir(subfolder_path):
            video_path = os.path.join(subfolder_path, video_filename)
            print(f"processing {video_path}")

            # Check if the file is a video file
            if video_filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                cap = cv2.VideoCapture(video_path)  # Open the video file
                fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second (fps) of the video
                frame_number = 0  # Initialize variables

                while True:
                    ret, frame = cap.read()  # Read the frame
                    if not ret:  # Break the loop if the end of the video is reached
                        break

                    # Save one frame per second
                    if frame_number % int(fps) == 0:
                        output_filename = f"{img_num}_{video_filename}_frame_{frame_number // int(fps)}.jpg"
                        output_path = os.path.join(output_folder, output_filename)
                        frame = cv2.resize(frame, (224, 224))
                        cv2.imwrite(output_path, frame)
                        img_num += 1

                    frame_number += 1

                cap.release()  # Release the video capture object

    print(f"{img_num} images extracted into {output_folder}")


def resize_dataset(folder_path):
    """
    delete the image (w<224 or h<224)
    resize the other images into 224x224
    """

    total_images = 0
    delete_images = 0
    resized_images = 0

    # Loop over all folders in the given directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)

                # Open the image using Pillow
                img = Image.open(file_path)
                total_images += 1

                # Get the width and height of the image
                width, height = img.size

                # # deal with noisy dataset
                # if width < 224 or height < 224:
                #     os.remove(file_path)
                #     delete_images += 1
                # elif width / height > 1.5 or height / width > 1.5:
                #     os.remove(file_path)
                #     delete_images += 1
                # else:
                #     # Resize to 224x224 for other images
                #     img_resized = img.resize((224, 224))
                #     img_resized.save(file_path, format="JPEG")
                #     resized_images += 1

                if width < 100 or height < 100:
                    os.remove(file_path)
                    delete_images += 1
                else:
                    img_resized = img.resize((224, 224))
                    img_resized.save(file_path, format="JPEG")
                    # os.remove(file_path)
                    resized_images += 1

        print(f"{total_images} total images, {delete_images} images deleted, {resized_images} images resized")


if __name__ == "__main__":
    # read_MS_Celeb_1M('/home/mang/Downloads/MS-Celeb-1M/data/croped_face_images/FaceImageCroppedWithOutAlignment.tsv',
    #                  '/home/mang/Downloads/MS-Celeb-1M/imgs')
    # video_2_images('/home/mang/Downloads/BP4D+',
    #                '/home/mang/Downloads/BP4D+_imgs')
    resize_dataset('/home/mang/Downloads/face_datasets/celeba')