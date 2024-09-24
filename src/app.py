# Raya Imports
from raya.application_base import RayaApplicationBase
from raya.controllers import *
from raya.enumerations import *
from src.FSMs.nurse_aid.constants.constants import *
from src.FSMs.nurse_aid.states import STATES
from raya.tools.fsm import FSM
from raya.tools.filesystem import *
from raya.tools.image import show_image, draw_on_image
from raya.skills import RayaSkillHandler
from skills.skill_belinson_approach.skill_belinson_approach import SkillBelinsonApproach

# Get audio options for every language
from src.FSMs.nurse_aid.constants.audio_english import AUDIO_ENGLISH
from src.FSMs.nurse_aid.constants.audio_hebrew import AUDIO_HEBREW
AUDIO_language_dict = {'ENGLISH' : AUDIO_ENGLISH,
                    'HEBREW' : AUDIO_HEBREW}

# Get UI options for every language
from src.FSMs.nurse_aid.constants.ui_english import SCREENS_ENGLISH
from src.FSMs.nurse_aid.constants.ui_hebrew import SCREENS_HEBREW
UI_language_dict = {'ENGLISH' : SCREENS_ENGLISH,
                    'HEBREW' : SCREENS_HEBREW}


# Other imports
import argparse
import os
from pytube import YouTube
import numpy as np
import time
import math
import pandas as pd

import threading
import sys
import tty
import termios
import ast

# Import VR libraries and create a text to speech client
from google.cloud import texttospeech
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_service_key_4.json'


class KeyboardThread(threading.Thread):
    '''Class to get a keyboard input'''
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.dev_mode_flag = False
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            if not self.dev_mode_flag:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                self.input_cbk(key)


class RayaApplication(RayaApplicationBase):
       
    async def setup(self):
        # Timer
        self.app_start_time = time.time()

        # self.log.debug(f'Setting keyboard listener...')
        # self.kthread = KeyboardThread(self.my_callback)
        # self.key = 0

        # Enable controllers
        await self.enable_controllers()

        # Get input args
        self.get_args()

        # Set initial variables
        await self.setup_variables()

        # Debug flag
        if not self.debug:
            
            # Localize
            # self.log.info('Localizing...')
            # await self.nav.set_map(
            #                 map_name= self.map_name,
            #                 wait_localization = True,
            #                 wait = True
            #                 )

            # Init detection models
            self.log.info('Enabling face detection model...')
            self.face_detector = await self.cv.enable_model(
                    name = APPROACH_PREDICTOR,
                    source = APPROACH_CAMERA,
                    model_params = {'scale': 0.3,
                                    'depth' : True
                                    }
                )
            self.log.info('Model enabled!')

            # Enable feet detector
            self.log.info('Enabling feet detection model...')
            self.feet_detector = await self.cv.enable_model(
                    name = FEET_PREDICTOR,
                    source = FEET_CAMERA,
                    model_params = {'depth': True}
                )
            self.log.info('Model enabled!')

            self.log.warn('Registering skills')
            self.skill_belinson_approach = self.register_skill(SkillBelinsonApproach)
            await self.skill_belinson_approach.execute_setup(
                setup_args={
                    'map_name' : self.map_name
                }
            )

        self.log.info('Setting up Nurse Aid FSM...')
        self.fsm = FSM(app=self,name='nurse_aid',log_transitions=True)

        # Setup complete
        self.log.info('Setup Complete')



    async def loop(self):
        # Loop
        self.log.info(f'FSM nurse_aid_fsm starting...')
        await self.fsm.run_and_await()
        self.finish_app()



    async def finish(self):
        # Finishing instructions
        await self.test_specific_component('chest_button')
        await self.fleet.finish_task(task_id = str(self.task_id),
                                     result = FLEET_FINISH_STATUS.SUCCESS)
        self.log.warn(f'FSM nurse_aid_fsm finished')


    def my_callback(self, inp):
            #evaluate the keyboard input
            self.key = inp
            print('You Entered:', inp)
            if self.key == 'd':
                try:
                    self.create_task(name = 'stop_all_movement',
                                    afunc = self.stop_all_movement)
                except Exception as e:
                    print(f'Error in stop_all_movement -  {e}')

                self.dev_mode_flag = True
                self.kthread.dev_mode_flag = True
        
            if self.key == 'q':
                self.finish_app()
    

    async def stop_all_movement(self):
        try:
            await self.sound.cancel_all_sounds()
            await self.nav.cancel_navigation()
            await self.leds.turn_off_all()
            await self.motion.cancel_motion()
            
        except Exception as e:
            print(f'Error in stop_all_movement - {e}')

    async def enable_controllers(self):
        # Enable controllers
        self.ui: UIController = await self.enable_controller('ui')
        self.log.info('UI controller - Enabled')
        self.leds: LedsController = await self.enable_controller('leds')
        self.log.info('Leds controller - Enabled')
        self.nav: NavigationController = await self.enable_controller('navigation')
        self.log.info('Navigation controller - Enabled') 
        self.motion: MotionController = await self.enable_controller('motion')
        self.log.info('Motion controller - Enabled')
        self.cameras: CamerasController = await self.enable_controller('cameras')
        self.log.info('Cameras controller - Enabled')
        self.sound: SoundController = await self.enable_controller('sound')
        self.log.info('Sound controller - Enabled')
        self.cv: CVController = await self.enable_controller('cv')
        self.log.info('CV controller - Enabled')
        self.sensors: SensorsController = await self.enable_controller('sensors')
        self.log.info('Sensors controller - Enabled')
        self.fleet: FleetController = await self.enable_controller('fleet')
        self.log.info('Fleet controller - Enabled')
        self.analytics: AnalyticsController = await self.enable_controller('analytics')
        self.log.info(f'Analytics controller - Enabled')
        self.lidar = await self.enable_controller('lidar')
        self.log.info('Lidar controller - Enabled')

        # Enable cameras
        await self.cameras.enable_camera(APPROACH_CAMERA)
        await self.cameras.enable_camera(FEET_CAMERA)



    async def setup_variables(self):
        create_dat_folder(DATA_PATH)
        create_dat_folder(AUDIO_PATH)

        # App flags and counters
        self.robot_localized = False
        self.navigation_successful = False
        self.localizing_attempts = 0
        self.current_error = None
        self.last_state = None
        self.stop_condition = False
        self.approach_successful = False
        self.approach_attempts = 0
        self.brief_attempts = 0
        self.user_setup_attempts = 0
        self.brief_successful = False
        self.sessions_attempts = 0
        self.sessions_successful = False
        self.stop_treatment = False
        self.feet_detected = False
        self.bbox_ymin = 0
        self.distance_to_feet = -1
        self.bad_id = False
        self.face_detections = {}      
        self.dynamic_recordings_list = []
        self.one_time_action_flag = True
        self.feet_approach_successful = False
        self.navigation_attempts = 1
        self.nav_feedback = None
        self.stop_fleet = False
        self.ui_button_feedback = None
        self.ui_button_feedback_id = None
        self.video_feedback = None
        self.games_feedback = None
        self.can_play_sound = True
        self.dev_mode_state = None
        self.dev_mode_flag = False
        self.path_available = False
        self.belinson_approach_feedback = {'skill_success' : None,
                                           'status_msg' : None}
        self.text_to_speech_client = texttospeech.TextToSpeechClient()

        # Analytics for Daniel
        self.obstacle_counter = 1
        self.fleet_request_counter = 0
        self.touch_item_time = 0
        self.touch_item = None
        self.treatment_feedback_time = None
        self.user_feedback = None
        self.user_verification_successful = False
        self.stop_condition_counter = 0
        self.stop_condition_timers = []
        self.exit_choice = None
        self.exit_choice_human_format = {}
        self.user_stop_states = []
        self.memory_game_response_time = 0     
        self.memory_game_time = 0
        self.difference_game_response_time = 0
        self.difference_game_time = 0
        self.trivia_game_time = 0
        self.end_to_end_time, self.end_to_end_timer = 0, time.time()
        self.end_to_end_success = False

        # Chest button component test variables
        self.button_press_success = False
        self.exit_choices = []
        self.press2reaction_time = None
        self.press2reaction_times = []

    async def test_specific_component(self, component_name):
        '''
        Test a specific component in the application and get a spreadsheet
        containing the results from each run
        '''

        # Get date and time
        month = time.strftime('%B')
        month_day = time.strftime('%d')
        hour = str(int(time.strftime('%I')) + 3)
        minute = time.strftime('%M')
        path = f'{DATA_PATH}/{component_name}.csv'

        # Choose data based on the component you want to test
        if component_name == 'chest_button':
            if int(self.stop_condition_counter) == 0:
                self.log.debug(f'Chest button was not pressed. Not saving run...')
                return
            
            data = {'Number of presses' : int(self.stop_condition_counter),
                'State of Button Press' : self.last_state,
                'Button Press Success' : self.button_press_success,
                'Exit Choices' : self.exit_choices,
                'Press to Reaction Times [s]' : self.press2reaction_times,
                'Date & Time' : f'{month_day}/{month} | {hour}:{minute}',
                'Fail Reason' : ''
                }

        # Add fail reason
        if not self.button_press_success:
            data['Fail Reason'] = input('Please enter fail reason:')

        # Create the log if it doesn't exist, otherwise update it
        if check_file_exists(path):
            existing_df = pd.read_csv(resolve_path(path))
        else:
            existing_df = pd.DataFrame(columns = data.keys())

        df = pd.DataFrame.from_dict(data, orient = 'index').T
        combined_df = pd.concat([existing_df, df], ignore_index = True)
        csv_string = combined_df.to_csv(index = False)
        with open_file(path, 'w') as f:
            f.write(csv_string)
        self.log.info(f'Saved component test: {component_name} to path: {path}')


    async def save_run(self):
        month = time.strftime('%B')
        month_day = time.strftime('%d')
        week_day = time.strftime('%A')
        hour = str(int(time.strftime('%I')) + 2)
        minute = time.strftime('%M')
        current_time = [month, month_day, week_day, hour, minute]

        timestamp = ''
        for elem in current_time:
            timestamp = f'{timestamp}_{elem}'

        path = f'{DATA_PATH}/data{timestamp}.csv'
        data = {'Obstacles' : str(self.obstacle_counter - 1),
                'Fleet Requests' : str(self.fleet_request_counter),
                'Touch Item' : str(self.touch_item),
                'Touch Item Time [s]' : str(self.touch_item_time),
                'Treatment Feedback' : str(self.user_feedback),
                'Treatment Feedback Time [s]' : str(self.treatment_feedback_time),
                'User verified' : str(self.user_verification_successful),
                'Exit Choice' : str(self.exit_choice),
                'State in Exit Choice' : str(self.user_stop_states),
                'Memory Game Time [s]' : str(self.memory_game_time),
                'Memory Game Response Time [s]' : str(self.memory_game_response_time),
                'Chest Button Pressed' : int(self.stop_condition_counter),
                'Total App Time [s]' : str(self.end_to_end_time),
                'E2E Success' : str(self.end_to_end_success),
                }
        
        df = pd.DataFrame.from_dict(data, orient = 'index').T
        csv_string = df.to_csv(index = False)
        with open_file(path, 'w') as f:
            f.write(csv_string)


    # update_audio dictionary to include the patient's name
    def update_audio_dict(self, audio_dict, prefix1, prefix2):
        for item in audio_dict:
            if prefix1 in audio_dict[item]['text']:
                audio_dict[item]['text'] = \
                    audio_dict[item]['text'].replace(prefix1, prefix2)
                                                


    # Parse arguments with argparse
    def get_args(self):
        parser = argparse.ArgumentParser()

        # Initial navigation position (X, Y, angle)
        parser.add_argument('-x' , '--target_x',
                            type = float, default = 149.0, required = False,
                            help ='X coordinate to initial navigation')
        
        parser.add_argument('-y', '--target_y',
                            type = float, default = 298.0, required = False,
                            help = 'Y coordinate to initial navigation')
        
        parser.add_argument('-a', '--target_angle',
                            type = float, default = 43.18, required = False,
                            help = 'Angle to initial navigation')

        # Target goal (new fleet arg)
        parser.add_argument('-tg', '--target_goal', default = None,
                            type = str, required = False, help = 'target goal')

        # Map name
        parser.add_argument('-m', '--map_name',
                            type = str, default = 'Belinson__default',
                            required = False,
                            help = 'Map name')

        # Task ID
        parser.add_argument('-tid', '--task_id',
                            type = str, default = 1,
                            required = False, help = 'Task ID')
        
        # Patient name
        parser.add_argument('-usr', '--patient_name',
                            type = str, default = None,
                            required = False, help = 'name of the patient')
        

        # Language to speak
        parser.add_argument('-l', '--language',
                            type = str, default = 'hebrew',
                            required = False, help = 'language')
        
        # Video arguments (link and number of repetitions)
        parser.add_argument('-v1', '--watch_vid1',
                            type = str, default = 'no_value',
                            required = False, help = 'first video link')
        
        parser.add_argument('-r1', '--watch_vid1_repeat',
                            type = int, default = 1,
                            required = False, help = 'first video repetitions')
        
        parser.add_argument('-v2', '--watch_vid2',
                            type = str, default = 'no_value',
                            required = False, help = 'second video link')
        
        parser.add_argument('-r2', '--watch_vid2_repeat',
                            type = int, default = 1,
                            required = False, help = 'second video repetitions')
        
        parser.add_argument('-v3', '--watch_vid3',
                            type = str, default = 'no_value',
                            required = False, help = 'third video link')
        
        parser.add_argument('-r3', '--watch_vid3_repeat',
                            type = int, default = 1,
                            required = False, help = 'third video repetitions')
        
        parser.add_argument('-v4', '--watch_vid4',
                            type = str, default = 'no_value',
                            required = False, help = 'fourth video link')
        
        parser.add_argument('-r4', '--watch_vid4_repeat',
                            type = int, default = 1,
                            required = False, help = 'fourth video repetitions')
        
        parser.add_argument('-v5', '--watch_vid5',
                            type = str, default = 'no_value',
                            required = False, help = 'fifth video link')
        
        parser.add_argument('-r5', '--watch_vid5_repeat',
                            type = int, default = 1,
                            required = False, help = 'fifth video repetitions')

        # Debug flag
        parser.add_argument('-db', '--debug_flag',
                            type = bool, default = False,
                            required = False, help = 'debug flag')
        
        
        # Parse the arguments
        args = parser.parse_args()
        self.x_initial = args.target_x
        self.y_initial = args.target_y
        self.angle_initial = args.target_angle
        self.map_name = args.map_name
        self.task_id = args.task_id
        self.patient_name = args.patient_name
        self.v1 = args.watch_vid1
        self.r1 = args.watch_vid1_repeat
        self.v2 = args.watch_vid2
        self.r2 = args.watch_vid2_repeat
        self.v3 = args.watch_vid3
        self.r3 = args.watch_vid3_repeat
        self.v4 = args.watch_vid4
        self.r4 = args.watch_vid4_repeat
        self.v5 = args.watch_vid5
        self.r5 = args.watch_vid5_repeat
        self.debug = args.debug_flag
        self.language = args.language.upper()

        # Conver target goal to dict
        if args.target_goal:
            target_goal = ast.literal_eval(args.target_goal)
            self.x_initial = float(target_goal['x'])
            self.y_initial = float(target_goal['y'])
            self.angle_initial = float(target_goal['angle'])
            self.map_name = target_goal['map_name']

            self.log.debug(f'target goal: {target_goal}')

        # Update the audio constants file with the patient name
        self.audio_dict = AUDIO_language_dict[self.language]
        self.update_audio_dict(audio_dict = self.audio_dict,
                               prefix1 = 'dummy_patient_name',
                               prefix2 = self.patient_name
                               )

        # Take the relevant screens according to the chosen language
        globals().update(UI_language_dict[self.language])
    
        # Create a videos dictionary
        self.videos_dict = {'video1' : {'link' : self.v1,
                                        'reps' : int(self.r1)
                                        },
                            'video2' : {'link' : self.v2,
                                        'reps' : int(self.r2)
                                        },
                            'video3' : {'link' : self.v3,
                                        'reps' : int(self.r3)
                                        },
                            'video4' : {'link' : self.v4,
                                        'reps' : int(self.r4)
                                        },
                            'video5' : {'link' : self.v5,
                                        'reps' : int(self.r5)
                                        },
                            }