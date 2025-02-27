# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import OptionProperty, DictProperty, ListProperty
from kivy.uix.label import Label
from kivymd.material_resources import DEVICE_TYPE
from kivymd.theming import ThemableBehavior
from kivymd.theming_dynamic_text import get_contrast_text_color

Builder.load_string('''
<MDLabel>
    disabled_color: self.theme_cls.disabled_hint_text_color
    text_size: (self.width, None)
''')


class MDLabel(ThemableBehavior, Label):
    font_style = OptionProperty(
        'Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                          'Headline', 'Display1', 'Display2', 'Display3',
                          'Display4', 'Button', 'Icon'])

    # Font, Bold, Mobile size, Desktop size (None if same as Mobile)
    _font_styles = DictProperty({'Body1': ['DefaultJapaneseFont', False, 14, 13],
                                 'Body2': ['DefaultJapaneseFont', True, 14, 13],
                                 'Caption': ['DefaultJapaneseFont', False, 12, None],
                                 'Subhead': ['DefaultJapaneseFont', False, 16, 15],
                                 'Title': ['DefaultJapaneseFont', True, 20, None],
                                 'Headline': ['DefaultJapaneseFont', False, 24, None],
                                 'Display1': ['DefaultJapaneseFont', False, 34, None],
                                 'Display2': ['DefaultJapaneseFont', False, 45, None],
                                 'Display3': ['DefaultJapaneseFont', False, 56, None],
                                 'Display4': ['DefaultJapaneseFont', False, 112, None],
                                 'Button': ['DefaultJapaneseFont', True, 14, None],
                                 'Icon': ['Icons', False, 24, None]})

    theme_text_color = OptionProperty(None, allownone=True,
            options=['Primary', 'Secondary', 'Hint', 'Error', 'Custom',
                     'ContrastParentBackground']
            )

    text_color = ListProperty(None, allownone=True)

    parent_background = ListProperty(None, allownone=True)

    _currently_bound_property = {}

    def __init__(self, **kwargs):
        super(MDLabel, self).__init__(**kwargs)
        self.on_theme_text_color(None, self.theme_text_color)
        self.on_font_style(None, self.font_style)
        self.on_opposite_colors(None, self.opposite_colors)

    def on_font_style(self, instance, style):
        info = self._font_styles[style]
        self.font_name = info[0]
        self.bold = info[1]
        if DEVICE_TYPE == 'desktop' and info[3] is not None:
            self.font_size = sp(info[3])
        else:
            self.font_size = sp(info[2])

    def on_theme_text_color(self, instance, value):
        t = self.theme_cls
        op = self.opposite_colors
        setter = self.setter('color')
        t.unbind(**self._currently_bound_property)
        attr_name = {'Primary': 'text_color' if not op else
                                'opposite_text_color',
                     'Secondary': 'secondary_text_color' if not op else
                                  'opposite_secondary_text_color',
                     'Hint': 'disabled_hint_text_color' if not op else
                             'opposite_disabled_hint_text_color',
                     'Error': 'error_color',
                    }.get(value, None)
        if attr_name:
            c = {attr_name: setter}
            t.bind(**c)
            self._currently_bound_property = c
            self.color = getattr(t, attr_name)
        else:
            # 'Custom' and 'ContrastParentBackground' lead here, as well as the
            # generic None value it's not yet been set
            if value == 'Custom' and self.text_color:
                self.color = self.text_color
            elif value == 'ContrastParentBackground' and self.parent_background:
                self.color = get_contrast_text_color(self.parent_background)
            else:
                self.color = [0, 0, 0, 1]

    def on_text_color(self, *args):
        if self.theme_text_color == 'Custom':
            self.color = self.text_color

    def on_opposite_colors(self, instance, value):
        self.on_theme_text_color(self, self.theme_text_color)
