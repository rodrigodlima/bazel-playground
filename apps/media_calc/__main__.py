import csv


def calc_media(notes):
    temp = 0
    for i in range(len(notes)):
        temp = notes[i] + temp
        total = temp / len(notes)

    return total


notas = [7, 10, 8, 6]
name = "Rodrigo"
file_path = "final_result.csv"
result = calc_media(notas)

with open(file_path, "w", newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow([name, int(result)])
