import random

import flet as ft


class app:
    def __init__(self, page: ft.Page):
        self.page = page  # Define a página onde o jogo será exibido
        self.page.title = "Jogo da Forca"
        # Sem margem em volta: o fundo ocupa a tela inteira (evita borda branca na web)
        self.page.padding = 0
        self.page.bgcolor = "#1B2A1F"

        self.themes = {
            "Animais": [
                "elefante",
                "girafa",
                "cachorro",
                "gato",
                "pato",
                "tigre",
                "leao",
                "zebra",
                "hipopotamo",
                "rinoceronte",
                "leopardo",
                "macaco",
                "panda",
                "urso",
                "lobo",
                "coala",
                "suricato",
                "camelo",
                "gorila",
                "pinguim",
            ],
            "Cidade": [
                "Sao-Paulo",
                "Rio-de-Janeiro",
                "Paris",
                "Londres",
                "Toquio",
                "Nova-York",
                "Los-Angeles",
                "Pequim",
                "Moscou",
                "Dubai",
                "Sydney",
                "Berlim",
                "Roma",
                "Istambul",
                "Bangkok",
                "Toronto",
                "Chicago",
                "Miami",
                "Tehran",
                "Hong-Kong",
            ],
            "Futebol": [
                "Barcelona",
                "Real-Madrid",
                "Liverpool",
                "Bayern",
                "Juventus",
                "Manchester-United",
                "Chelsea",
                "Manchester-City",
                "Arsenal",
                "Paris-Saint-Germain",
                "Borussia-Dortmund",
                "AC-Milan",
                "Inter-de-Milao",
                "Ajax",
                "Atletico-de-Madrid",
                "Tottenham",
                "Napoli",
                "Boca-Juniors",
                "River-Plate",
                "Flamengo",
            ],
        }

        # Faixa (mínimo, máximo) de letras da palavra em cada dificuldade.
        # O nível difícil não tem teto: com o limite antigo de 12 letras, palavras
        # como "Rio-de-Janeiro" ou "Paris-Saint-Germain" nunca eram sorteadas.
        self.difficulty_levels = {
            "Facil": (4, 6),
            "Medio": (6, 8),
            "Dificil": (8, 99),
        }

        # Quantidade de erros permitidos (imagens hangman_0.png até hangman_7.png)
        self.max_errors = 7

        self.selected_theme = None
        self.selected_difficulty = None

        # Palavra provisória só para montar o layout; a real é sorteada em choose_word()
        self.choiced = "PYTHON"

        # O arquivo se chama TROPICAN.TTF (extensão maiúscula). No GitHub Pages o
        # servidor é Linux e diferencia maiúsculas, então o caminho precisa bater.
        self.page.fonts = {
            "TROPICAN": "fonts/TROPICAN.TTF",
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
                    content=ft.Text(
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

    # Método para abrir um diálogo (vitória ou game over)
    def show_dialog(self, dialog):
        dialog.open = True
        self.page.dialog = dialog
        self.page.update()

    # Método para mostrar um aviso rápido na parte de baixo da tela
    def show_message(self, message):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, size=20),
            open=True,
        )
        self.page.update()

    # Método para criar um botão do teclado virtual
    def create_keyboard_button(self, letter):

        return ft.Container(
            col=1,
            border_radius=ft.border_radius.all(5),
            content=ft.Text(
                value=letter,
                color=ft.colors.WHITE,
                size=25,
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
        self.scene = ft.Image(
            col={
                "xs": 0,
                "sm": 0,
                "md": 12,
            },
            src="images/scene.png",
        )
        self.tiki = ft.Image(
            col={
                "xs": 0,
                "sm": 0,
                "md": 3,
            },
            src="images/tiki.png",
            repeat=ft.ImageRepeat.NO_REPEAT,
        )

        self.victim = ft.Image(
            data=0,  # Contador de erros
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
            col={"xs": 12, "lg": 6},
            padding=ft.padding.all(5),
            margin=ft.margin.all(0),
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
            col={
                "xs": 12,
                "sm": 12,
                "md": 6,
            },
            border_radius=ft.border_radius.all(20),
            bgcolor=ft.colors.with_opacity(0.7, "#C39973"),
            padding=ft.padding.all(5),
            margin=ft.margin.all(10),
            expand=True,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                col=12,
                controls=[
                    ft.Text(
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 12,
                        },
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
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 6,
                        },
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
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 6,
                        },
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
                        col={
                            "xs": 6,
                            "sm": 6,
                            "md": 6,
                        },
                        border_radius=10,
                        bgcolor=ft.colors.with_opacity(0.9, "#4F7550"),
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
                        col={
                            "xs": 6,
                            "sm": 6,
                            "md": 6,
                        },
                        border_radius=10,
                        bgcolor=ft.colors.with_opacity(0.9, "#4E3725"),
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
                        col={
                            "xs": 6,
                            "sm": 6,
                            "md": 6,
                        },
                        content=ft.Text(
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
                        col={
                            "xs": 6,
                            "sm": 6,
                            "md": 6,
                        },
                        content=ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan(
                                    text="JOGAR",
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
            col={"xs": 12, "lg": 6},
            image_src="images/keyboard.png",
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            image_fit=ft.ImageFit.FILL,
            padding=ft.padding.only(top=100, left=40, right=40, bottom=50),
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
            image_fit=ft.ImageFit.COVER,
            image_src="images/background.png",
            image_repeat=ft.ImageRepeat.REPEAT_Y,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=self.view_game[0],
            ),
        )

        # A tela do jogo rola quando não cabe na altura da janela (telas baixas,
        # zoom de 125%/150% no Windows ou celular); antes o teclado ficava cortado.
        self.layout2 = ft.Container(
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            expand=True,
            image_src="images/background.png",
            image_fit=ft.ImageFit.COVER,
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=self.view_game[1],
                    ),
                ],
            ),
        )

        # Adiciona o layout à página
        self.page.add(self.layout)

    # Método para validar a letra clicada pelo usuário
    def validate_letter(self, e):
        letter = e.control.content.value

        # Desativa o botão clicado para a mesma letra não contar duas vezes
        e.control.disabled = True
        e.control.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.GREY, ft.colors.GREY_700],
        )
        e.control.update()

        if letter in self.choiced:  # Se a letra estiver correta
            for pos, char in enumerate(self.choiced):
                if char == letter:
                    self.word.controls[pos] = self.letter_to_guess(letter=char)
            self.word.update()

            if self.check_win():  # Se todas as letras foram preenchidas
                self.show_dialog(self.winner)
        else:  # Se a letra estiver incorreta
            self.victim.data += 1
            self.victim.src = f"images/hangman_{self.victim.data}.png"
            self.victim.update()

            if self.victim.data >= self.max_errors:  # Se o enforcado estiver completo
                self.show_dialog(self.game_over)

    # Método para verificar se o jogador venceu
    def check_win(self):
        return all(button.content.value != "_" for button in self.word.controls)

    # Método para criar o contêiner de uma letra da palavra a ser adivinhada
    def letter_to_guess(self, letter):
        return ft.Container(
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            bgcolor=ft.colors.BROWN_700,
            width=30,
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
        if self.page.web:
            # No navegador não dá para fechar a aba via código
            self.show_message("Para sair, basta fechar esta aba do navegador.")
        else:
            self.page.window_destroy()  # Fecha a janela do jogo

    # Método para voltar ao menu e reiniciar o jogo do zero
    def menu(self, e):
        self.page.dialog.open = False  # Fecha o diálogo atual
        self.page.remove(self.layout2)  # Remove a tela do jogo
        self.__init__(self.page)  # Recria menu, teclado e placar zerados

    def start_game_btn(self, e):
        if not (self.selected_theme and self.selected_difficulty):
            self.show_message("Escolha um tema e uma dificuldade para começar.")
            return

        self.choose_word()
        self.word.controls = [self.letter_to_guess("_") for _ in self.choiced]
        self.page.remove(self.layout)
        self.page.add(self.layout2)

    def radiogroup_theme(self, e):
        self.selected_theme = e.control.value

    def radiogroup_difficulty(self, e):
        self.selected_difficulty = e.control.value

    def choose_word(self):
        words = self.themes[self.selected_theme]
        min_len, max_len = self.difficulty_levels[self.selected_difficulty]
        filtered_words = [word for word in words if min_len <= len(word) <= max_len]
        # Se nenhuma palavra do tema couber na dificuldade, sorteia entre todas
        self.choiced = random.choice(filtered_words or words).upper()


# Inicia o app. A chamada fica no nível do módulo, sem `if __name__ == "__main__"`,
# porque na versão web (publicada com `flet publish`) o arquivo é importado como
# módulo "main" pelo Pyodide e um bloco `__main__` nunca seria executado.
ft.app(target=app, assets_dir="assets")
