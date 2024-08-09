import pygame
import math
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Light Reflection Simulation")

clock = pygame.time.Clock()
background = (0, 0, 0)

# Declare global variables
n1 = 1
n2 = 1
angle = 45


class PygameWidget(Widget):
    def on_update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.init_interface()
        pygame.display.flip()
        clock.tick(60)

    def draw_bottom_line(self, angle: float, color=(255, 0, 0)):
        x = math.tan(angle * math.pi / 180) * height // 2
        pygame.draw.line(screen, color, (width // 2 - x, height), (width // 2, height // 2), 3)

    def draw_top_line(self, angle: float, color=(0, 255, 0)):
        x = math.tan(angle * math.pi / 180) * height // 2
        pygame.draw.line(screen, color, (width // 2, height // 2), (width // 2 + x, 0), 3)

    def draw_dashed_line(self, start_point, end_point):
        t = 50
        w = 1
        color = (125, 125, 125)

        x = math.fabs(end_point[0] - start_point[0]) // t
        y = math.fabs(end_point[1] - start_point[1]) // t

        x_sum = 0
        y_sum = 0
        for i in range(t // 2):
            pygame.draw.line(screen, color, (start_point[0] + x_sum, start_point[1] + y_sum),
                             (start_point[0] + x_sum + x, start_point[1] + y_sum + y), w)
            x_sum += x * 2
            y_sum += y * 2

        pygame.draw.line(screen, color, (start_point[0] + x_sum, start_point[1] + y_sum), end_point, w)

    def draw_line(self, color=(255, 0, 0)):
        self.draw_bottom_line(angle, color)

        a2 = angle * n1 / n2

        self.draw_top_line(a2, color)

    def init_interface(self):
        screen.fill(background)

        # bottom half
        pygame.draw.rect(screen, (50, 50, 50), (0, height // 2, width, height // 2))
        # line
        pygame.draw.line(screen, (255, 255, 255), (0, height // 2), (width, height // 2), 3)

        self.draw_line()


class SliderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        def update_values(instance, value, variable_name):
            global n1, n2, angle
            if variable_name == 'n1':
                n1 = value
            elif variable_name == 'n2':
                n2 = value
            elif variable_name == 'angle':
                angle = value

        # Slider 1 (Range: 1 to 10)
        slider_1 = Slider(min=1, max=10, value=n1, orientation='horizontal')
        label_1 = Label(text="n2 Value: {}".format(int(slider_1.value)))
        slider_1.bind(value=lambda instance, value: (
            setattr(label_1, 'text', "v2 Value: {}".format(int(value))),
            update_values(instance, value, 'n1')
        ))

        # Slider 2 (Range: 1 to 10)
        slider_2 = Slider(min=1, max=10, value=n2, orientation='horizontal')
        label_2 = Label(text="n1 Value: {}".format(int(slider_2.value)))
        slider_2.bind(value=lambda instance, value: (
            setattr(label_2, 'text', "n2 Value: {}".format(int(value))),
            update_values(instance, value, 'n2')
        ))

        # Slider 3 (Range: 0 to 90)
        slider_3 = Slider(min=0, max=90, value=angle, orientation='horizontal')
        label_3 = Label(text="angle Value: {}".format(int(slider_3.value)))
        slider_3.bind(value=lambda instance, value: (
            setattr(label_3, 'text', "angle Value: {}".format(int(value))),
            update_values(instance, value, 'angle')
        ))

        layout.add_widget(slider_1)
        layout.add_widget(label_1)
        layout.add_widget(slider_2)
        layout.add_widget(label_2)
        layout.add_widget(slider_3)
        layout.add_widget(label_3)

        pygame_widget = PygameWidget()
        layout.add_widget(pygame_widget)

        Clock.schedule_interval(pygame_widget.on_update, 1.0 / 60.0)

        return layout


if __name__ == '__main__':
    SliderApp().run()
