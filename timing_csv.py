import main
import csv


def get_notes_array(music_title):
    if music_title in music_list:
        return list_convart(music_title)
    else:
        return [0]


music_list = [
    "gomakasi",
    "maware",
    "watashinotensi",
    "AngelicAngel",
    "nopoi",
    "sukida",
    "tentaikansoku",
    "Catch the Moment"
]


def list_convart(filename):
    return_list = []
    with open(main.folder_name+"csv/"+filename+".csv") as file_name:
        file_read = csv.reader(file_name)
        for i in file_read:
            return_list.append(int(i[0]))
    # print(return_list)
    return return_list
