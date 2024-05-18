import flet as ft
import random


class app:
    def __init__(self, page: ft.Page):
        self.page = page  # Define a página onde o jogo será exibido

        self.themes = {
            "Animais": ["elefante", "girafa", "cachorro", "gato", "pato"],
            "Cidade": ["São Paulo", "Rio-de-Janeiro", "Paris", "Londres", "Tóquio"],
            "Futebol": ["Barcelona", "Real-Madrid", "Liverpool", "Bayern", "Juventus"],
        }

        self.difficulty_levels = {
            "Facil": (4, 6),
            "Medio": (6, 8),
            "Dificil": (8, 12),
        }

        self.selected_theme = None
        self.selected_difficulty = None

        self.choiced = "PYTHON"

        # Lista de palavras disponíveis para o jogo
        self.available_words = ["python", "flet", "programador", "aventureiro"]
        # Escolhe uma palavra aleatória da lista e a converte para maiúsculas

        self.page.fonts = {
            "TROPICAN": "fonts/TROPICAN.ttf",
        }

        self.page.theme = ft.Theme(font_family="TROPICAN")

        self.create_dialogs()
        self.create_layout()

    # Método para criar os diálogos do jogo
    def create_dialogs(self):
        # Cria o diálogo para o vencedor
        self.winner = self.create_dialog(
            title="PARABÉNS, VOCÊ GANHOU!",
            content="Quer jogar novamente?",
        )

        # Cria o diálogo para o game over
        self.game_over = self.create_dialog(
            title="GAME OVER",
            content="Quer tentar novamente?",
        )

    # Método para criar um diálogo genérico
    def create_dialog(self, title, content):
        return ft.AlertDialog(
            bgcolor=ft.colors.with_opacity(0.7, "#C39973"),
            open=True,  # Define o diálogo como aberto
            title=ft.Text(
                value=title,
                text_align=ft.TextAlign.CENTER,
                size=40,
            ),  # Define o título do diálogo
            content=ft.Text(
                value=content,
                text_align=ft.TextAlign.CENTER,
                size=30,
            ),  # Define o conteúdo do diálogo
            content_padding=ft.padding.all(
                30
            ),  # Define o preenchimento interno do conteúdo
            inset_padding=ft.padding.all(
                10
            ),  # Define o preenchimento externo do conteúdo
            modal=True,  # Define o diálogo como modal (bloqueia a interação com o resto da página)
            shape=ft.RoundedRectangleBorder(radius=10),  # Define a forma do diálogo
            actions=[  # Define as ações disponíveis no diálogo (botões)
                ft.Container(
                    margin=ft.margin.only(top=50),
                    col=5,
                    content=ft.Text(
                        col=5,
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(
                                text="NOVO JOGO",
                                style=ft.TextStyle(
                                    color="#4F7550",
                                    size=50,
                                ),
                            ),
                        ],
                    ),
                    ink=True,
                    on_click=self.menu,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,  # Alinha as ações no centro do diálogo
        )

    # Método para criar os elementos do jogo

    # Método para criar um botão do teclado virtual
    def create_keyboard_button(self, letter):

        return ft.Container(
            col={"xs": 1, "lg": 1},
            border_radius=ft.border_radius.all(5),
            content=ft.Text(
                value=letter,
                color=ft.colors.WHITE,
                size=30,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.AMBER, ft.colors.DEEP_ORANGE],
            ),
            on_click=self.validate_letter,  # Define a função a ser executada quando o botão é clicado
        )

    # Método para criar o layout da página
    def create_layout(self):
        # Cria a imagem de fundo da cena
        self.scene = ft.Image(col=12, src="images/scene.png")
        self.tiki = ft.Image(col=3, src="images/tiki.png")

        self.victim = ft.Image(
            data=0,
            src="images/hangman_0.png",
            repeat=ft.ImageRepeat.NO_REPEAT,
            height=300,
        )

        # Cria a palavra a ser adivinhada
        self.word = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
            controls=[self.letter_to_guess("_") for _ in self.choiced],
        )

        # Cria o contêiner do jogo
        self.game = ft.Container(
            col={"xs": 10, "lg": 5},
            padding=ft.padding.all(50),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.victim,
                    self.word,
                ],  # Adiciona a imagem do enforcado e a palavra ao contêiner
            ),
        )

        self.start_game = ft.Container(
            col=6,
            border_radius=ft.border_radius.all(20),
            bgcolor=ft.colors.with_opacity(0.7, "#C39973"),
            # image_src="images/keyboard_2.png",
            # image_fit=ft.ImageFit.CONTAIN,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                col=10,
                width=500,
                height=500,
                controls=[
                    ft.Text(
                        col=10,
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(
                                text="HANG",
                                style=ft.TextStyle(
                                    color="#4F7550",
                                    size=70,
                                ),
                            ),
                            ft.TextSpan(
                                text="MAN",
                                style=ft.TextStyle(
                                    color="#4E3725",
                                    size=70,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        col=5,
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(
                                text="SELECT THEME",
                                style=ft.TextStyle(
                                    color="#4F7550",
                                    size=30,
                                ),
                            )
                        ],
                    ),
                    ft.Text(
                        col=5,
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(
                                text="SELECT DIFFICULTY",
                                style=ft.TextStyle(
                                    color="#4E3725",
                                    size=30,
                                ),
                            )
                        ],
                    ),
                    ft.Container(
                        border_radius=10,
                        bgcolor=ft.colors.with_opacity(0.9, "#4F7550"),
                        col=5,
                        content=ft.RadioGroup(
                            content=ft.Column(
                                [
                                    ft.Radio(value="Animais", label="Animais"),
                                    ft.Radio(value="Cidade", label="Cidade"),
                                    ft.Radio(value="Futebol", label="Futebol"),
                                ]
                            ),
                            on_change=self.radiogroup_theme,
                        ),
                    ),
                    ft.Container(
                        border_radius=10,
                        bgcolor=ft.colors.with_opacity(0.9, "#4E3725"),
                        col=5,
                        content=ft.RadioGroup(
                            content=ft.Column(
                                [
                                    ft.Radio(value="Facil", label="Facil"),
                                    ft.Radio(value="Medio", label="Medio"),
                                    ft.Radio(value="Dificil", label="Dificil"),
                                ]
                            ),
                            on_change=self.radiogroup_difficulty,
                        ),
                    ),
                    ft.Container(
                        margin=ft.margin.only(top=50),
                        col=5,
                        content=ft.Text(
                            col=5,
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan(
                                    text="SAIR",
                                    style=ft.TextStyle(
                                        color="#4E3725",
                                        size=50,
                                    ),
                                ),
                            ],
                        ),
                        ink=True,
                        on_click=self.close_game,
                    ),
                    ft.Container(
                        margin=ft.margin.only(top=50),
                        col=5,
                        content=ft.Text(
                            col=5,
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan(
                                    text="CONTINUAR",
                                    style=ft.TextStyle(
                                        color="#4F7550",
                                        size=50,
                                    ),
                                ),
                            ],
                        ),
                        ink=True,
                        on_click=self.start_game_btn,
                    ),
                ],
            ),
        )

        abnt_keyboard_layout = "QWERTYUIOPASDFGHJKLÇZXCVBNM-"

        self.keyboard = ft.Container(
            col={"xs": 10, "lg": 5},
            image_src="images/keyboard.png",
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            image_fit=ft.ImageFit.FILL,
            padding=ft.padding.only(top=200, left=10, right=10, bottom=50),
            content=ft.ResponsiveRow(
                columns=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.create_keyboard_button(letter)
                    for letter in abnt_keyboard_layout  # Cria um botão para cada letra do teclado
                ],
            ),
        )

        self.view_game = [
            [self.tiki, self.start_game, self.tiki],
            [self.scene, self.game, self.keyboard, self.scene],
        ]

        # Define o layout da página com os contêineres e a imagem de fundo
        self.layout = ft.Container(
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            expand=True,
            image_src="images/background.png",
            image_fit=ft.ImageFit.COVER,
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=self.view_game[0],
            ),
        )

        self.layout2 = ft.Container(
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            expand=True,
            image_src="images/background.png",
            image_fit=ft.ImageFit.COVER,
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=self.view_game[1],
            ),
        )

        # Adiciona o layout à página
        self.page.add(self.layout)

    # Método para validar a letra clicada pelo usuário
    def validate_letter(self, e):
        for pos, letter in enumerate(self.choiced):
            if e.control.content.value == letter:  # Se a letra estiver correta
                self.word.controls[pos] = self.letter_to_guess(letter=letter)
                self.word.update()

        if e.control.content.value not in self.choiced:  # Se a letra estiver incorreta
            self.victim.data += 1

            if self.victim.data >= 7:  # Se o enforcado estiver completo
                self.page.dialog = self.game_over
                self.page.update()

            errors = self.victim.data
            self.victim.src = f"images/hangman_{errors}.png"
            self.victim.update()

        e.control.disabled = True  # Desativa o botão clicado
        e.control.gradient = ft.LinearGradient(colors=[ft.colors.GREY])
        e.control.update()

        if all(
            button.content.value != "_" for button in self.word.controls
        ):  # Se todas as letras foram preenchidas
            self.check_win()

    # Método para verificar se o jogador venceu
    def check_win(self):
        if all(button.content.value != "_" for button in self.word.controls):
            self.page.dialog = self.winner
            self.page.update()

    # Método para criar o contêiner de uma letra da palavra a ser adivinhada
    def letter_to_guess(self, letter):
        return ft.Container(
            bgcolor=ft.colors.BROWN_700,
            height=50,
            width=50,
            border_radius=ft.border_radius.all(5),
            content=ft.Text(
                value=letter,
                color=ft.colors.WHITE,
                size=30,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
        )

    # Método para fechar o jogo
    def close_game(self, e):
        self.page.window_destroy()  # Fecha a janela do jogo

    def menu(self, e):
        self.page.remove(self.layout2)  # Remove o layout atual
        self.page.dialog.open = False  # Fecha o diálogo atual
        self.__init__(self.page)  # Reinicia o jogo

    def start_game_btn(self, e):
        self.choose_word()
        self.word.controls = [self.letter_to_guess("_") for _ in self.choiced]
        self.page.remove(self.layout)
        self.page.add(self.layout2)
        print("Palavra escolhida:", self.choiced)  # Print para depuração

    def radiogroup_theme(self, e):
        self.selected_theme = e.control.value

    def radiogroup_difficulty(self, e):
        self.selected_difficulty = e.control.value

    def choose_word(self):
        if self.selected_theme and self.selected_difficulty:
            words = self.themes[self.selected_theme]
            min_len, max_len = self.difficulty_levels[self.selected_difficulty]
            filtered_words = [word for word in words if min_len <= len(word) <= max_len]
            if filtered_words:
                self.choiced = random.choice(filtered_words).upper()
            else:
                self.choiced = random.choice(words).upper()
        else:
            self.choiced = random.choice(
                ["PYTHON", "FLET", "PROGRAMADOR", "AVENTUREIRO"]
            )
        print("Palavra escolhida no choose_word:", self.choiced)  # Print para depuração


# Função principal que inicia o jogo
if __name__ == "__main__":
    ft.app(target=app, assets_dir="assets")
