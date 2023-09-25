class SomeModel:
    def __init__(self):
        pass

    def predict(self, message: str) -> float:
        # Чем больше доля гласных в сообщении, тем положительнее сообщение

        if not isinstance(message, str):
            raise TypeError(f'message must be a string, not {type(message)}')

        message = message.lower()
        vowels_list = ['а', 'е', 'ё', 'ю', 'я', 'и', 'ы', 'о', 'у', 'э',
                       'a', 'e', 'i', 'o', 'u']
        vowels_count = 0
        for vowel in vowels_list:
            if vowel in message:
                vowels_count += 1

        msg_len = len(message)
        return vowels_count / msg_len if msg_len > 0 else 0


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.45,
) -> str:

    if not isinstance(model, SomeModel):
        raise TypeError(
            f'model must be an instance of class SomeModel, not {type(model)}')

    if bad_thresholds > good_thresholds:
        raise RuntimeError('lower threshold is greater than upper threshold')

    pred = model.predict(message)
    if pred < bad_thresholds:
        return 'неуд'
    if pred > good_thresholds:
        return 'отл'
    return 'норм'
