import flet as ft


def main(page: ft.Page):
    page.padding = ft.padding.all(0)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {
        "TROPICAN": "fonts/TROPICAN.ttf",
    }

    page.theme = ft.Theme(font_family="TROPICAN")

    page.add(
        ft.Container(
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            expand=True,
            image_src="images/background.png",
            image_fit=ft.ImageFit.COVER,
            image_repeat=ft.ImageRepeat.NO_REPEAT,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(col=3, src="images/tiki.png"),
                    ft.Container(
                        col=6,
                        border_radius=ft.border_radius.all(20),
                        bgcolor=ft.colors.with_opacity(0.7, "#C39973"),
                        # image_src="images/keyboard_2.png",
                        # image_fit=ft.ImageFit.CONTAIN,
                        content=ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            col=12,
                            width=500,
                            height=500,
                            controls=[
                                ft.Text(
                                    col=12,
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
                                    col=6,
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
                                    col=6,
                                    text_align=ft.TextAlign.CENTER,
                                    spans=[
                                        ft.TextSpan(
                                            text="SELECT DIFFICULT",
                                            style=ft.TextStyle(
                                                color="#4E3725",
                                                size=30,
                                            ),
                                        )
                                    ],
                                ),
                                ft.Container(
                                    col=6,
                                    content=ft.Column(
                                        controls=[
                                            ft.TextButton(col=2, text="Animais"),
                                            ft.TextButton(col=2, text="Cidade"),
                                            ft.TextButton(col=2, text="Futebol"),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    col=6,
                                    content=ft.Column(
                                        controls=[
                                            ft.TextButton(col=2, text="Facil"),
                                            ft.TextButton(col=2, text="Medio"),
                                            ft.TextButton(col=2, text="Dificil"),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Container(
                                    col=6,
                                    content=ft.Text(
                                        col=6,
                                        text_align=ft.TextAlign.CENTER,
                                        spans=[
                                            ft.TextSpan(
                                                text="PLAY GAME",
                                                style=ft.TextStyle(
                                                    color="#4F7550",
                                                    size=30,
                                                ),
                                            )
                                        ],
                                    ),
                                    on_click=True,
                                ),
                            ],
                        ),
                    ),
                    ft.Image(col=3, src="images/tiki.png"),
                ],
            ),
        )
    )
    page.update()


ft.app(target=main, assets_dir="assets")
