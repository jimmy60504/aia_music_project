import os
import argparse
from functools import partial
from .helpers.utils import get_file_list, make_dirs
from .helpers.parallel import batch_plot, processing
from .settings import MODEL_ROOT_PATH

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--model', required=True, help='model name', type=str)

    ap.add_argument('--batch_size',
                    required=False,
                    default=10,
                    help='files per batch',
                    type=int)

    args = ap.parse_args()

    root_path = os.path.join(MODEL_ROOT_PATH, os.path.basename(args.model))

    if not os.path.isdir(root_path):
        raise FileNotFoundError('Invalid src path')

    src_path = os.path.join(root_path, 'db')
    file_list = get_file_list(src_path)

    image_path = os.path.join(root_path, 'images')
    make_dirs(image_path)
    existing_images = [
        name.split('/')[-1][:-4] for name in get_file_list(image_path)
    ]
    to_draw_list = []
    for idx, path in enumerate(file_list):
        file_name = path.split('/')[-1][:-4]
        if file_name not in existing_images:
            to_draw_list.append(file_list[idx])

    file_list = file_list if not existing_images else to_draw_list

    par = partial(batch_plot, output_dir=image_path)

    processing(file_list, par, args.batch_size)
