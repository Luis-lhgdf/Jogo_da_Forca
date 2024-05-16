import flet as ft
import random


class app:
    def __init__(self, page: ft.Page):
        self.page = page  # Define a página onde o jogo será exibido
        self.page.scroll = ft.ScrollMode.AUTO  # Define o modo de rolagem da página
        self.page.bgcolor = ft.colors.BROWN_600  # Define a cor de fundo da página

        # Lista de palavras disponíveis para o jogo
        self.available_words = ["python", "flet", "programador", "aventureiro"]
        # Escolhe uma palavra aleatória da lista e a converte para maiúsculas
        self.choiced = random.choice(self.available_words).upper()

        # Chama o método para criar a interface do jogo
        self.view_game()

    # Método para criar a interface do jogo
    def view_game(self):
        # Cria os diálogos para o vencedor e o game over
        self.create_dialogs()
        # Cria os elementos do jogo (imagem do enforcado, palavra a ser adivinhada)
        self.create_game_elements()
        # Cria o teclado virtual
        self.create_keyboard()
        # Cria o layout da página
        self.create_layout()

    # Método para criar os diálogos do jogo
    def create_dialogs(self):
        # Cria o diálogo para o vencedor
        self.winner = self.create_dialog(
            title="PARABENS VOCE ACERTOU!!!",
            content="QUER TENTAR NOVAMENTE?",
            on_click=self.restart_game,
        )

        # Cria o diálogo para o game over
        self.game_over = self.create_dialog(
            title="GAME OVER",
            content="QUER TENTAR NOVAMENTE?",
            on_click=self.restart_game,
        )

    # Método para criar um diálogo genérico
    def create_dialog(self, title, content, on_click):
        return ft.AlertDialog(
            open=True,  # Define o diálogo como aberto
            title=ft.Text(value=title),  # Define o título do diálogo
            content=ft.Text(value=content),  # Define o conteúdo do diálogo
            content_padding=ft.padding.all(
                30
            ),  # Define o preenchimento interno do conteúdo
            inset_padding=ft.padding.all(
                10
            ),  # Define o preenchimento externo do conteúdo
            modal=True,  # Define o diálogo como modal (bloqueia a interação com o resto da página)
            shape=ft.RoundedRectangleBorder(radius=5),  # Define a forma do diálogo
            actions=[  # Define as ações disponíveis no diálogo (botões)
                ft.TextButton(
                    text="SAIR",
                    style=ft.ButtonStyle(color=ft.colors.RED),
                    on_click=self.close_game,  # Define a função a ser executada quando o botão é clicado
                ),
                ft.TextButton(
                    text="NOVO JOGO",
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE, bgcolor=ft.colors.GREEN
                    ),
                    on_click=on_click,  # Define a função a ser executada quando o botão é clicado
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,  # Alinha as ações no centro do diálogo
        )

    # Método para criar os elementos do jogo
    def create_game_elements(self):
        # Cria a imagem do enforcado
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
            controls=[self.letter_to_guess("_") for letter in self.choiced],
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

    # Método para criar o teclado virtual
    def create_keyboard(self):
        # Layout do teclado conforme ABNT
        abnt_keyboard_layout = "QWERTYUIOPASDFGHJKLÇZXCVBNM"

        self.keyboard = ft.Container(
            col={"xs": 10, "lg": 5},
            image_src="images/keyboard.png",
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            image_fit=ft.ImageFit.FILL,
            padding=ft.padding.only(top=150, left=45, right=45, bottom=50),
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

        # Define o layout da página com os contêineres e a imagem de fundo
        self.layout = ft.ResponsiveRow(
            columns=10,
            controls=[self.scene, self.game, self.keyboard, self.scene],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
            bgcolor=ft.colors.AMBER_500,
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

    # Método para reiniciar o jogo
    def restart_game(self, e):
        self.page.remove(self.layout)  # Remove o layout atual
        self.page.dialog.open = False  # Fecha o diálogo atual
        self.__init__(self.page)  # Reinicia o jogo

    # Método para fechar o jogo
    def close_game(self, e):
        self.page.window_destroy()  # Fecha a janela do jogo


# Função principal que inicia o jogo
if __name__ == "__main__":
    ft.app(target=app, assets_dir="assets")
