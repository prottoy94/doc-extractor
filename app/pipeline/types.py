class Word:
    def __init__(self, text, confidence, left, top, width, height, line_number):
        self.text = text
        self.confidence = confidence
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.line_number = line_number

    def __repr__(self):
        return (
            "Word(text="
            + repr(self.text)
            + ", confidence="
            + str(self.confidence)
            + ", line_number="
            + str(self.line_number)
            + ")"
        )


class Field:
    def __init__(self, name, value, confidence, needs_review, reason):
        self.name = name
        self.value = value
        self.confidence = confidence
        self.needs_review = needs_review
        self.reason = reason

    def __repr__(self):
        return (
            "Field(name="
            + repr(self.name)
            + ", value="
            + repr(self.value)
            + ", confidence="
            + str(self.confidence)
            + ", needs_review="
            + str(self.needs_review)
            + ")"
        )
