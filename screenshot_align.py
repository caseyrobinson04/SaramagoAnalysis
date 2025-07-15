import os
import eyekit
import textsE


from eyekit.text import TextBlock

left_text_lines = getattr(textsE, f"left_{3}")
right_text_lines = getattr(textsE, f"right_{3}")

left_block = TextBlock(
    left_text_lines,
    position=(92, 182),
    font_face='Times New Roman',
    font_size=32,
    line_height=113.5,
    align='left',
    anchor='left'
)

right_block = TextBlock(
    right_text_lines,
    position=(1000, 182),
    font_face='Times New Roman',
    font_size=32,
    line_height=113.5,
    align='left',
    anchor='left'
)

eyekit.tools.align_to_screenshot(left_block, "stimuli_screenshots\BE.3.png")
# eyekit.tools.align_to_screenshot(right_block, "trial1.png")
