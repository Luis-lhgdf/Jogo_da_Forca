import flet as ft


def main(page: ft.Page):

    # Layout do teclado conforme ABNT
    abnt_keyboard_layout = "QWERTYUIOPASDFGHJKLÇZXCVBNM"

    def letter_to_guess(letter):
        return ft.Container(
            col={"xs": 1, "lg": 1},
            bgcolor=ft.colors.BLUE_400,
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

    layout = ft.ResponsiveRow(
        columns=10,
        controls=[letter_to_guess(letter) for letter in abnt_keyboard_layout],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(layout)


ft.app(target=main)
