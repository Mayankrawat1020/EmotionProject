import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from PIL import Image as PILImage
import os
import random

kivy.require('2.0.0')

# Resize the image using Pillow
original_image_path = "images\image.jpg"
resized_image_path = "images\human-body-resized.png"

if not os.path.exists(original_image_path):
    print(f"Error: The image path {original_image_path} does not exist.")
else:
    try:
        with PILImage.open(original_image_path) as img:
            resized_img = img.resize((400, 404))
            resized_img.save(resized_image_path)
            print(f"Image resized and saved to {resized_image_path}.")
    except Exception as e:
        print(f"Error resizing image: {e}")

class DemographicPage(Screen):
    def __init__(self, **kwargs):
        super(DemographicPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.name_input = TextInput(hint_text='Name', multiline=False, size_hint=(1, None), height=40)
        self.age_input = TextInput(hint_text='Age (1-100)', multiline=False, size_hint=(1, None), height=40)
        self.gender_input = Spinner(
            text='Select Gender',
            values=['Male', 'Female', 'Other'],
            size_hint=(1, None),
            height=40
        )
        self.education_input = Spinner(
            text='Select Education Level',
            values=['10th level', '12th level', 'Undergraduate', 'Postgraduate', 'Other'],
            size_hint=(1, None),
            height=40
        )
        self.autism_input = Spinner(
            text='Diagnosed with Autism?',
            values=['Yes', 'No'],
            size_hint=(1, None),
            height=40
        )

        layout.add_widget(Label(text='Enter your Name:'))
        layout.add_widget(self.name_input)
        layout.add_widget(Label(text='Enter your Age:'))
        layout.add_widget(self.age_input)
        layout.add_widget(Label(text='Select your Gender:'))
        layout.add_widget(self.gender_input)
        layout.add_widget(Label(text='Select your Education Level:'))
        layout.add_widget(self.education_input)
        layout.add_widget(Label(text='Have you been diagnosed clinically with autism?'))
        layout.add_widget(self.autism_input)

        next_button = Button(text='Next', size_hint=(1, None), height=50)
        next_button.bind(on_press=self.next_page)
        layout.add_widget(next_button)

        #previous_button = Button(text='Previous', size_hint=(1, None), height=50)
        #previous_button.bind(on_press=self.previous_page)
        #layout.add_widget(previous_button)

        self.add_widget(layout)

    def show_error_popup(self, message):
        popup = Popup(title='Error going to next page',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def next_page(self, instance):

        if not self.name_input.text:
            print("Error: Name is invalid.")
            self.show_error_popup("Enter valid name")
            return
        try:
            age = int(self.age_input.text)
            if not 1 <= age <= 100:
                raise ValueError
        except ValueError:
            print("Error: Enter valid age")
            self.show_error_popup("Enter a valid age between 1 and 100")
            return
        if self.gender_input.text == 'Select Gender':
            print("Error: Select gender")
            self.show_error_popup("Select gender")
            return
        if self.education_input.text == 'Select Education Level':
            print("Error: Select education level")
            self.show_error_popup("Select education level")
            return
        if self.autism_input.text == 'Diagnosed with Autism?':
            print("Error: Select autism diagnosis")
            self.show_error_popup("Select autism diagnosis")
            return

        

        app = App.get_running_app()
        app.user_data = {
            "Name": self.name_input.text,
            "Age": self.age_input.text,
            "Gender": self.gender_input.text,
            "Education": self.education_input.text,
            "AutismDiagnosis": self.autism_input.text
        }
        print("Demographic data recorded")

        self.manager.current = 'questionnaire'

    #def previous_page(self, instance):
        # This is the first page, so we don't do anything
     #   pass

class QuestionnairePage(Screen):
    touch_point = ListProperty([0, 0])
    emotion = StringProperty('')

    def __init__(self, **kwargs):
        super(QuestionnairePage, self).__init__(**kwargs)
        self.emotions = ['Happiness', 'Sadness', 'Fear', 'Anger', 'Surprise', 'Disgust']
        random.shuffle(self.emotions)
        self.current_emotion_index = 0
        self.emotion = self.emotions[self.current_emotion_index]
        self.selected_choice = None
        self.selected_activation = None
        self.emotion_data = {}

        self.layout = FloatLayout()
        self.create_layout()
        self.add_widget(self.layout)


    def create_layout(self):
        self.layout.clear_widgets()

        # Emotion label at the top
        self.layout.add_widget(Label(text=f'Emotion: {self.emotion}', size_hint=(0.2, 0.1), pos_hint={'top': 1}))

        if os.path.exists(resized_image_path):
            self.image = Image(source=resized_image_path, allow_stretch=False, keep_ratio=True, 
                               size_hint=(None, None), size=(400, 404), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        else:
            print(f"Error: The resized image path {resized_image_path} does not exist.")
            self.image = Label(text="Image not found.")

        self.layout.add_widget(self.image)

        # Question label for positive/negative
        question_label = Label(text='Do you find the somatic response to the emotion activating or deactivating in nature?', 
                               size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'y': 0.35})
        self.layout.add_widget(question_label)

        # Positive and Negative buttons
        self.positive_button = Button(text='Activating', size_hint=(0.4, 0.08), pos_hint={'center_x': 0.3, 'y': 0.27})
        self.negative_button = Button(text='Deactivating', size_hint=(0.4, 0.08), pos_hint={'center_x': 0.7, 'y': 0.27})
        
        self.positive_button.bind(on_press=lambda x: self.select_choice('Activating'))
        self.negative_button.bind(on_press=lambda x: self.select_choice('Deactivating'))
        
        self.layout.add_widget(self.positive_button)
        self.layout.add_widget(self.negative_button)

        # New question label for intensity of emotion
        activation_label = Label(text='How intensely do you feel the emotion?', 
                                 size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'y': 0.18})
        self.layout.add_widget(activation_label)

        # Dropdown for intensity of emotion felt
        self.activation_dropdown = Spinner(
            text='Select intensity of emotion felt',
            values=['1','2','3','4','5'],
            size_hint=(0.4, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        self.activation_dropdown.bind(text=self.on_activation_select)
        self.layout.add_widget(self.activation_dropdown)

        # Previous button
        self.prev_button = Button(text='Previous', size_hint=(0.4, 0.08), pos_hint={'x': 0.1, 'y': 0})
        self.prev_button.bind(on_press=self.prev_page)
        self.layout.add_widget(self.prev_button)

        # Next button
        self.next_button = Button(text='Next', size_hint=(0.4, 0.08), pos_hint={'right': 0.9, 'y': 0})
        self.next_button.bind(on_press=self.next_page)
        self.layout.add_widget(self.next_button)

        if isinstance(self.image, Image):
            self.image.bind(pos=self.update_ellipse, size=self.update_ellipse)
            self.image.bind(on_touch_down=self.on_image_touch_down)

        # Load previous data if available
        if self.emotion in self.emotion_data:
            self.touch_point = self.emotion_data[self.emotion]['touch_point']
            self.selected_choice = self.emotion_data[self.emotion]['selected_choice']
            self.selected_activation = self.emotion_data[self.emotion]['selected_activation']
            self.update_ellipse()
            self.select_choice(self.selected_choice)
            self.activation_dropdown.text = self.selected_activation

    def on_activation_select(self, spinner, text):
        self.selected_activation = text

    def select_choice(self, choice):
        self.selected_choice = choice
        self.positive_button.background_color = (1, 1, 1, 1)
        self.negative_button.background_color = (1, 1, 1, 1)
        if choice == 'Activating':
            self.positive_button.background_color = (0, 1, 0, 1)
        else:
            self.negative_button.background_color = (1, 0, 0, 1)

    def on_image_touch_down(self, instance, touch):
        if self.image.collide_point(*touch.pos):
            x = int((touch.x - self.image.x) / self.image.width * 400)
            y = int((1 - (touch.y - self.image.y) / self.image.height) * 404)

            self.touch_point = [x, y]
            self.update_ellipse()
            
            print(f"Touch at: {self.touch_point} recorded for emotion: {self.emotion}")

    def update_ellipse(self, *args):
        self.canvas.after.clear()
        if self.touch_point != [0, 0]:
            with self.canvas.after:
                Color(1, 0, 0)
                d = 10
                x = self.image.x + self.touch_point[0] / 400 * self.image.width - d / 2
                y = self.image.y + (1 - self.touch_point[1] / 404) * self.image.height - d / 2
                Ellipse(pos=(x, y), size=(d, d))
                

    def next_page(self, instance):
        
        if not self.touch_point or not self.selected_choice or not self.selected_activation:
            self.show_error_popup("Please answer all the questions before proceeding.")
            return
        
        self.emotion_data[self.emotion] = {
            'touch_point': self.touch_point,
            'selected_choice': self.selected_choice,
            'selected_activation': self.selected_activation
        }

        if self.current_emotion_index < len(self.emotions) - 1:
            self.current_emotion_index += 1
            self.emotion = self.emotions[self.current_emotion_index]
            self.touch_point = [0, 0]
            self.selected_choice = None
            self.selected_activation = None
            self.create_layout()
        else:
            app = App.get_running_app()
            app.questionnaire_data = self.emotion_data
            self.manager.current = 'storypage'
            

    def prev_page(self, instance):
        if self.current_emotion_index > 0:
            self.current_emotion_index -= 1
            self.emotion = self.emotions[self.current_emotion_index]
            self.create_layout()
        else:
            self.manager.current = 'demographic'

    def show_error_popup(self, message):
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

class StoryPage(Screen):
    touch_point = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(StoryPage, self).__init__(**kwargs)
        self.stories = {
            1: "Story 1 text...",
            2: "Story 2 text...",
            3: "Story 3 text...",
            4: "story 4",
            5: "Story 5 text...",
            6: "Story 6 text...",
            7: "Story 7 text...",
            8: "story 8",
            9: "Story 9 text...",
            10: "Story 10 text...",
            11: "Story 11 text...",
            12: "story 12",
            13: "Story 13 text...",
            14: "Story 14 text...",
            15: "Story 15 text...",
            16: "story 16",
            17: "Story 17 text...",
            18: "Story 18 text...",
        }
        self.story_order = list(range(1, 19))
        random.shuffle(self.story_order)
        self.current_story_index = 0
        self.story = self.stories[self.story_order[self.current_story_index]]
        self.story_data = {}
        
        self.layout = FloatLayout()
        self.create_layout()
        self.add_widget(self.layout)
        

    def create_layout(self):
        self.layout.clear_widgets()


        story_label = Label(text=f"Story:", size_hint=(1, 0.1), pos_hint={'top': 1})
        self.layout.add_widget(story_label)
        
        story_text_label = Label(text=self.story, size_hint=(1, 0.1), pos_hint={'center_x': 0.1, 'top': 0.9})
        self.layout.add_widget(story_text_label)

        self.image = Image(source=resized_image_path, allow_stretch=False, keep_ratio=True, 
                           size_hint=(None, None), size=(400, 404), pos_hint={'center_x': 0.5, 'center_y': 0.64})
        self.layout.add_widget(self.image)
        self.image.bind(pos=self.update_ellipse, size=self.update_ellipse)
        self.image.bind(on_touch_down=self.on_image_touch_down)

        question_label = Label(text="What emotion do you feel after reading this story?", 
                               size_hint=(0.1, 0.1), pos_hint={'center_x': 0.5, 'y': 0.29})
        self.layout.add_widget(question_label)

        self.emotion_input = Spinner(
            text='Select Emotion',
            values=['Happiness', 'Sadness', 'Fear', 'Anger', 'Surprise', 'Disgust'],
            size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'y': 0.26}
        )
        self.layout.add_widget(self.emotion_input)

        activation_label = Label(text="Do you find the somatic response to the emotion activating or deactivating in nature?", 
                                 size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'y': 0.22})
        self.layout.add_widget(activation_label)

        self.activation_input = Spinner(
            text='Select Response',
            values=['Activating', 'Deactivating'],
            size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'y': 0.16}
        )
        self.layout.add_widget(self.activation_input)

        intensity_label = Label(text="How intense is this emotion?", 
                                size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'y': 0.12})
        self.layout.add_widget(intensity_label)

        self.intensity_input = Spinner(
            text='Select Intensity',
            values=['1', '2', '3', '4', '5'],
            size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'y': 0.08}
        )
        self.layout.add_widget(self.intensity_input)

        next_button = Button(text='Next', size_hint=(0.4, 0.08), pos_hint={'right': 0.9, 'y': 0})
        next_button.bind(on_press=self.next_page)
        self.layout.add_widget(next_button)

        prev_button = Button(text='Previous', size_hint=(0.4, 0.08), pos_hint={'x': 0.1, 'y': 0})
        prev_button.bind(on_press=self.prev_page)
        self.layout.add_widget(prev_button)

    def on_image_touch_down(self, instance, touch):
        if self.image.collide_point(*touch.pos):
            x = int((touch.x - self.image.x) / self.image.width * 400)
            y = int((1 - (touch.y - self.image.y) / self.image.height) * 404)
            self.touch_point = [x, y]
            self.update_ellipse()

    def update_ellipse(self, *args):
        self.canvas.after.clear()
        if self.touch_point != [0, 0]:
            with self.canvas.after:
                Color(1, 0, 0)
                d = 10
                x = self.image.x + self.touch_point[0] / 400 * self.image.width - d / 2
                y = self.image.y + (1 - self.touch_point[1] / 404) * self.image.height - d / 2
                Ellipse(pos=(x, y), size=(d, d))

    def next_page(self, instance):
        

        if self.touch_point == [0, 0] or self.emotion_input.text == 'Select Emotion' or \
           self.activation_input.text == 'Select Response' or self.intensity_input.text == 'Select Intensity':
            self.show_error_popup("Please answer all the questions before proceeding.")
            return

        self.story_data[self.story_order[self.current_story_index]] = {
            'touch_point': self.touch_point,
            'emotion': self.emotion_input.text,
            'activation': self.activation_input.text,
            'intensity': self.intensity_input.text
        }

        if self.current_story_index < len(self.story_order) - 1:
            self.current_story_index += 1
            self.story = self.stories[self.story_order[self.current_story_index]]
            self.touch_point = [0, 0]
            self.emotion_input.text = 'Select Emotion'
            self.activation_input.text = 'Select Response'
            self.intensity_input.text = 'Select Intensity'
            self.create_layout()
        else:
            app = App.get_running_app()
            app.story_data = self.story_data
            self.save_all_data()
            self.manager.current = 'thank_you'

    def prev_page(self, instance):
        if self.current_story_index > 0:
            self.current_story_index -= 1
            self.story = self.stories[self.story_order[self.current_story_index]]
            self.create_layout()
        else:
            self.manager.current = 'questionnaire'

    def save_all_data(self):
        app = App.get_running_app()
        with open('records.txt', 'a') as f:
            f.write(f"\nUser Data:\n")
            for key, value in app.user_data.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\nQuestionnaire Data:\n")
            for emotion, data in app.questionnaire_data.items():
                f.write(f"{emotion}:\n")
                f.write(f"  Touch Point: {data['touch_point']}\n")
                f.write(f"  Selected Choice: {data['selected_choice']}\n")
                f.write(f"  Selected Activation: {data['selected_activation']}\n")
            
            f.write("\nStory Data:\n")
            for story_number, data in app.story_data.items():
                f.write(f"Story {story_number}:\n")
                f.write(f"  Touch Point: {data['touch_point']}\n")
                f.write(f"  Emotion: {data['emotion']}\n")
                f.write(f"  Activation: {data['activation']}\n")
                f.write(f"  Intensity: {data['intensity']}\n")

    def show_error_popup(self, message):
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()




class ThankYouPage(Screen):
    def __init__(self, **kwargs):
        super(ThankYouPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Thank you for participating!'))
        self.add_widget(layout)

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(DemographicPage(name='demographic'))
        self.add_widget(QuestionnairePage(name='questionnaire'))
        self.add_widget(StoryPage(name='storypage'))
        self.add_widget(ThankYouPage(name='thank_you'))


class MyApp(App):
    user_data = {}
    questionnaire_data = {}
    story_data = {}

    def build(self):
        return MyScreenManager()
    

if __name__ == '__main__':
    MyApp().run()