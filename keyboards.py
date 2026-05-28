from vkbottle import Keyboard, KeyboardButtonColor, Text


def make_keyboard():
    keyboard = Keyboard()
    keyboard.add(Text("Курс"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Анализ"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Конвертер"), color=KeyboardButtonColor.PRIMARY)

    return keyboard