class Animation():
    current_frame = 0
    current_image = -1
    def __init__(self,name,images,interval = 5):
        self.name = name
        self.images = images
        self.interval = interval

all_animation = {}


def animation_frame(name, images, interval):
    if all_animation.get():
        animation = all_animation[name]
    else:
        animation = Animation(name, images, interval)
        all_animation.update({name:animation})
    if animation.current_frame % interval == 0:
        animation.current_image = (animation.current_image + 1) % len(images)
    animation.current_frame += 1


def is_finished(name):
    animation = all_animation.get(name)
    if animation.current_frame >= animation.interval * len(animation.images):
        return True
    else:
        return False


        me.reset()

