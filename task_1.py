import argparse
import asyncio
import logging
from pathlib import Path
import aiofiles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(file_path, output_folder):
    """
    Copies a file to a given output folder.

    :param file_path: The path of the file to be copied.
    :param output_folder: The folder where the copied file will be saved.
    :return: None
    """
    try:
        destination_folder = output_folder / file_path.suffix.replace('.', '')
        destination_folder.mkdir(exist_ok=True)

        async with aiofiles.open(file_path, 'rb') as src:
            content = await src.read()
            async with aiofiles.open(destination_folder / file_path.name, 'wb') as dst:
                await dst.write(content)
        logging.info(f"File {file_path.name} copied to {destination_folder}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path.name}: {e}")


async def read_folder(source_folder, output_folder):
    """
    Asynchronously reads all files from the source folder and copies them to the output folder.

    :param source_folder: The path to the source folder.
    :param output_folder: The path to the output folder where the files will be copied to.
    :return: None

    """
    tasks = []
    for file_path in Path(source_folder).rglob('*.*'):
        if file_path.is_file():
            tasks.append(asyncio.create_task(copy_file(file_path, output_folder)))
        else:
            logging.error(f"Skipping {file_path} as it is not a file.")
    await asyncio.gather(*tasks)


async def main():
    """
    Asynchronously copies files based on their extensions.

    :return: None
    """
    parser = argparse.ArgumentParser(description="Asynchronously copy files based on their extensions.")
    parser.add_argument('--source', type=str, required=True, help="Source folder path")
    parser.add_argument('--destination', type=str, required=True, help="Destination folder path")

    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.destination)

    output_folder.mkdir(exist_ok=True)

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    asyncio.run(main())
