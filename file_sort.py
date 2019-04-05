from kivy.properties import ObjectProperty
from kivy.uix.filechooser import FileSystemLocal, FileSystemAbstract
from os import path, listdir

file_system = ObjectProperty(FileSystemLocal(), baseclass=FileSystemAbstract)


def alphanumeric_folders_first_reversed(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
            sorted((f for f in files if not filesystem.is_dir(f)), reverse=True))


def date_reversed(files, filesystem):
    """
    file ordering function usable with kivy, filechooser
    ordering according to creation date
    newest first
    :param files:
    :param filesystem:
    :return: ordered file list
    """
    times_files = []  # list of tuples (creation time, file)
    for file in files:
        if __name__ == '__main__':
            times_files.append((path.getctime(path.join(path_, file)), file))
        else:
            times_files.append((path.getctime(file), file))
    date_ordered_paths = sorted(times_files, key=lambda s: s[0], reverse=True)

    files_ = []  # ordered file list
    for each in date_ordered_paths:
        files_.append(each[1])
    # return times_files, date_ordered_paths
    return files_


if __name__ == '__main__':
    path_ = 'C:\\Users\\pkrssak\\AppData\\Roaming\\podcast_downloader\\data'
    print(listdir(path_))
    print(alphanumeric_folders_first_reversed(listdir(path_), FileSystemLocal()))

    paths = date_reversed(listdir(path_), FileSystemLocal())
    print('date ordered: ', paths)
