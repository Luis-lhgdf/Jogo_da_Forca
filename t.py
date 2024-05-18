import random

themes = {
    "Animais": ["elefante", "girafa", "cachorro", "gato", "pato"],
    "Cidade": ["São Paulo", "Rio de Janeiro", "Paris", "Londres", "Tóquio"],
    "Futebol": ["Barcelona", "Real Madrid", "Liverpool", "Bayern", "Juventus"],
}

difficulty_levels = {
    "Facil": (4, 6),
    "Medio": (6, 8),
    "Dificil": (8, 12),
}


selected_theme = "Futebol"
selected_difficulty = "Dificil"
if selected_theme and selected_difficulty:
    words = themes[selected_theme]
    print(words)
    min_len, max_len = difficulty_levels[selected_difficulty]
    print(min_len, max_len)
    filtered_words = [word for word in words if min_len <= len(word) <= max_len]
    print(filtered_words)
    if filtered_words:
        choiced = random.choice(filtered_words).upper()
        print(choiced)
    else:
        choiced = random.choice(words).upper()
        print(choiced)
else:
    choiced = random.choice(["PYTHON", "FLET", "PROGRAMADOR", "AVENTUREIRO"])
    print(choiced)
