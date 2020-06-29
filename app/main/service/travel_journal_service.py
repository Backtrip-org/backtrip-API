import os
from random import choice

from app.main.config import root_folder, config_variables
from app.main.model.trip import Trip
from fpdf import FPDF

from app.main.model.user import User
from app.main.service.trip_service import get_user_steps_participation
from app.main.util.exception.TripException import TripMustBeClosedException


class BacktripPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Généré avec Backtrip   -   Page %s' % self.page_no(), 0, 0, 'R')


class TravelJournalService:

    def __init__(self, trip: Trip, user: User):
        self.trip = trip
        self.user = user
        self.document = BacktripPDF()

        if not trip.closed:
            raise TripMustBeClosedException()

    def generate_travel_journal(self):
        self.document.add_font(family='title_font', fname=os.path.join(root_folder, 'resources', 'fonts', 'get_show.ttf'), uni=True, style='')
        self.document.add_page()

        self.__add_title()
        self.__display_steps()

    def __add_title(self):
        self.document.set_font('title_font', size=70)
        self.document.cell(w=0, h=40, txt=self.trip.name, align='C', ln=1)

    def __display_steps(self):
        personal_timeline: list = get_user_steps_participation(self.user, self.trip.id)

        if len(personal_timeline) < 1:
            self.__display_no_step_message()
            return

        for index, step in enumerate(personal_timeline):
            if (index + 1) % 4 == 0:
                self.document.add_page()
            self.__display_step_name(step.name)
            self.__display_step_datetime(step.start_datetime, step.end_datetime)
            self.__display_random_photo(step)
            self.document.cell(w=0, h=5, ln=1)

    def __display_no_step_message(self):
        self.document.set_font('Arial', size=20)
        self.document.cell(w=0, h=20, align='C', txt="Vous n'avez participé à aucune étape !", ln=1)

    def __display_step_name(self, step_name):
        self.document.set_font('Arial', size=20)
        flag_image_url = os.path.join(root_folder, 'resources', 'images', 'flag.png')
        self.document.image(name=flag_image_url, x=10, y=self.document.get_y(), h=9)
        self.document.set_x(20)
        self.document.cell(w=0, h=10, txt=step_name, ln=1)

    def __display_step_datetime(self, step_start_datetime, step_end_datetime):
        self.document.set_font('Arial', size=15)
        flag_image_url = os.path.join(root_folder, 'resources', 'images', 'clock.png')
        self.document.image(name=flag_image_url, x=11, y=self.document.get_y(), h=6)
        self.document.set_x(20)
        text = step_start_datetime.strftime("%d/%m/%Y, %H:%M")
        if step_end_datetime is not None:
            text += ' - {}'.format(step_end_datetime.strftime("%d/%m/%Y, %H:%M"))
        self.document.cell(w=0, h=7, txt=text, ln=1)

    def __display_random_photo(self, step):
        photos = step.get_photos()
        if len(photos) < 1:
            return
        selected_photo = choice(photos)
        photo_url = os.path.join(config_variables.get('files_directory'), '{}.{}'.format(selected_photo.id, selected_photo.extension))
        self.document.cell(w=0, h=3, ln=1)
        self.document.image(name=photo_url, x=20, h=50)

    def get_file_as_bytes_string (self):
        return self.document.output(dest='S')
