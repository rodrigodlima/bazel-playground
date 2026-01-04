def calc_media(notes):
    temp = 0
    for i in range(len(notes)):
        temp = notes[i] + temp
        total = temp / len(notes)

    return total


notas = [7, 10, 8, 6]
result = calc_media(notas)

with open("final_result.txt", "w") as file:
    file.write(f"The media is: {result}")
