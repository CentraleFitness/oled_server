from PIL import Image

from objects.container import Container
from objects.graphics.gbutton import GButton
from objects.graphics.glabel import GLabel
from objects.graphics.gscrollbar import GScrollBar
from objects.graphics.gtextbox import GTextBox


BLACK_AND_WHITE = '1'
BLACK = 0


class GContainer(Container):
    """Short for 'Graphic Container'"""

    def __init__(self, size: tuple, pos: tuple, **kwargs):
        """
        size: a tuple containing the size (x, y) of the object
        position: a tuple containing the distance (x, y)
                  from the top-left corner of the display
        kwargs:
            objects: a list of Gobject to store in the container
        """
        self.gsize = size
        self.gpos = pos
        self.actions = dict()
        self.action['U'] = self.cursor.prev()
        self.action['D'] = self.cursor.next()
        return super().__init__(**kwargs)

    def interact(self, input: str) -> None:
        if input in self.actions:
            self.action[input]()
            return None
        return self.cursor().action(input)

    def translate(self, *args, **kwargs) -> Image:
        render = Image.new(
            BLACK_AND_WHITE,
            self.gsize,
            color=BLACK)
        for obj in self.objects:
            assert isinstance(
                obj,
                (GContainer, GButton, GLabel, GScrollBar, GTextBox))
            img, pos = obj.translate(
                selected=(True if obj is self.cursor() else False))
            render.paste(img, pos)
        return render, self.gpos
