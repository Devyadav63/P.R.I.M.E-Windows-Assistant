def Take_Shot():
    from PIL import ImageGrab
    screenshot = ImageGrab.grab()
    screenshot.save("Reader.png")
    screenshot.close()