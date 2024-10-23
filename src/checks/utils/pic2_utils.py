import base64
import os
images_dir = '/images'

def save_base64_image(base64_string, directory, filename):
    """
    Save a base64-encoded image to the specified directory and filename.

    :param base64_string: Base64-encoded string representing the image data.
    :param directory: Directory where the image should be saved.
    :param filename: Filename of the image.
    """
    try:
        # 确保目录存在
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 构建完整的文件路径
        image_path = os.path.join(directory, filename)

        # 创建并写入文件
        with open(image_path, 'wb') as tmp:
            tmp.write(base64.b64decode(base64_string))

        return image_path
    except FileNotFoundError as e:
        print(f"Directory not found: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        return None

# # 使用示例
# base64_string = "your_base64_encoded_string_here"  # 替换为实际的Base64编码字符串
# directory = '/images'
# filename = 'excel.png'
#
# image_path = save_base64_image(base64_string, directory, filename)
# if image_path:
#     print(f"Image saved to {image_path}")
# else:
#     print("Failed to save the image.")