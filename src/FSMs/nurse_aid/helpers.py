# Raya imports
from src.FSMs.nurse_aid.constants.constants import *
from src.FSMs.nurse_aid.constants.navigation_constants import *
from src.FSMs.nurse_aid.constants.custon_exceptions import *
from src.FSMs.nurse_aid.constants.ui_english import *
from src.FSMs.nurse_aid.constants.ui_hebrew import *
from raya.controllers.navigation_controller import POSITION_UNIT, ANGLE_UNIT
from raya.enumerations import *
from raya.tools.filesystem import *
from raya.tools.image import show_image, draw_on_image
from src.FSMs.nurse_aid.states import STATES

# Other imports
from src.app import RayaApplication
from google.cloud import texttospeech
import time
import eyed3
import asyncio
import pandas as pd
import numpy as np
import math
import tf_transformations
from geometry_msgs.msg import PointStamped, Point, Pose, Quaternion
from collections import deque
import cv2
import random

import asyncio
from concurrent.futures import ThreadPoolExecutor

def check_state_decorator(func):
    '''Decorator to check for stop state prior to executing functions'''

    # Wrapper for regular functions
    def wrapper(self, *args, **kwargs):
        if self.app.stop_condition is True or self.app.dev_mode_flag is True:
            self.app.log.warn(
                        f'Function {func} execution is blocked by decorator')
        else:
            return func(self, *args, **kwargs)
    
    # Wrapper for async functions
    async def async_wrapper(self, *args, **kwargs):
        if self.app.stop_condition is True or self.app.dev_mode_flag is True:
            try:
                await self.app.sound.cancel_all_sounds()
            except Exception as e:
                self.app.log.warn(f'Got exception {e}, skipping it')
            self.app.log.warn(
                        f'Function {func} execution is blocked by decorator')
        else:
            return await func(self, *args, **kwargs)
        
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return wrapper

class Helpers:

    def __init__(self, app: RayaApplication):
        self.app = app



    @classmethod
    def decorate_methods(cls):
        '''Set the check_state_decorator for every attribute in the class
           except callbacks, listeners, and private methods
        '''
        for name, method in cls.__dict__.items():
            if callable(method) and not name.startswith("__") \
                and not "cb" in name and not "listener" in name:
                setattr(cls, name, check_state_decorator(method))
                


    def reset_variables(self, exclude_groups = []):
        '''Reset flags and variables'''

        if 'navigation' not in exclude_groups:
            self.app.robot_localized = False
            self.app.navigation_successful = False
            self.app.navigation_attempts = 0
        
        if 'approach' not in exclude_groups:
            self.app.approach_successful = False
            self.app.approach_attempts = 0
            self.app.feet_detected = False
        
        self.app.stop_condition = False
        self.app.stop_fleet = False
        self.app.brief_attempts = 0
        self.app.brief_successful = False
        self.app.sessions_attempts = 0
        self.app.sessions_successful = False
        self.app.bad_id = False
        self.app.exit_choice = None
        self.app.ui_button_feedback = None
        self.app.ui_button_feedback_id = None


    async def acquire_session_time(self):
        '''Get the session time to speak it later'''
        if int(self.app.treatment_time) != 0:
            if self.app.language == 'HEBREW':
                self.app.cognishine_sentence = \
                                f'{self.app.treatment_time} דקות של תרגול קוגנטיבי'
            elif self.app.language == 'ENGLISH':
                self.app.cognishine_sentence = \
                    f'{self.app.treatment_time} minutes of cognitive exercises'
        else:
            self.app.cognishine_sentence = ''



    async def get_current_time(self,
                               speech: bool = False,
                               download: bool = False
                               ):
        """
        INPUTS:
            speech - whether to speak the current time, or not

        OUTPUTS:
            t - the current time in the form of  M/D/WD/H/M
            seciton_of_day - the section of the day
        """

        month = time.strftime('%B')
        month_day = time.strftime('%d')
        week_day = time.strftime('%A')
        hour = str(int(time.strftime('%I')) + 3)
        minute = time.strftime('%M')
        t = [month, month_day, week_day, hour, minute]

        # Incase the hour is 12, so the robot won't say '0 hour'
        hour = int(hour)%12 if int(hour)%12 != 0 else 12

        # Section of day
        hour_24_clock = (int(time.strftime('%H')) + 2) % 24
        section_of_day = ""
        if 5 <= int(hour_24_clock) <= 11:
            if self.app.language == 'HEBREW':
                section_of_day = f'בוקר טוב {self.app.patient_name}'
            if self.app.language == 'ENGLISH':
                section_of_day = f'Good morning {self.app.patient_name}'

        elif 12 <= int(hour_24_clock) <= 16:
            if self.app.language == 'HEBREW':
                section_of_day = f'צהריים טובים {self.app.patient_name}'
            if self.app.language == 'ENGLISH':
                section_of_day = f'Good afternoon {self.app.patient_name}'

        elif 17 <= int(hour_24_clock) <= 20:
            if self.app.language == 'HEBREW':
                section_of_day = f'ערב טוב {self.app.patient_name}'
            if self.app.language == 'ENGLISH':
                section_of_day = f'Good evening {self.app.patient_name}'

        else:
            if self.app.language == 'HEBREW':
                section_of_day = f'לילה טוב {self.app.patient_name}'
            if self.app.language == 'ENGLISH':
                section_of_day = f'Good night {self.app.patient_name}'

        text, language, name = None, None, None
      
        # Transcribe text
        if self.app.language == 'HEBREW':
            language, name = 'he-IL', 'he-IL-Wavenet-D'
            if 10 <= int(minute) < 20:
                text = f'{section_of_day}. היום הוא יום {HEBREW_TENSES[t[2]]},\
                ה-{t[1]} ב{HEBREW_TENSES[t[0]]}, והשעה היא {hour} ו-{t[4]} דקות'
            elif int(minute) < 10:
                text = f'{section_of_day}. היום הוא יום {HEBREW_TENSES[t[2]]},\
                ה-{t[1]} ב{HEBREW_TENSES[t[0]]}, והשעה היא {hour} ו-{t[4][-1]} דקות'

            else:
                text = f'.{section_of_day}, היום יום {HEBREW_TENSES[t[2]]},\
                      ה-{t[1]} ב{HEBREW_TENSES[t[0]]}, והשעה היא {hour} {t[4]}'

        if self.app.language == 'ENGLISH':
            language, name = 'en-GB', 'en-GB-Wavenet-D'
            text = f'{section_of_day}. Today is {t[2]}, \
                                                and the time is {hour} {t[4]}'

        if speech:
            await self.text_to_speech(text = text,
                                      language = language,
                                      name = name,
                                      leds = True
                                      )
        if download:
            await self.download_voice(
                    text = text,
                    language='he-IL',
                    name='he-IL-Wavenet-D',
                    file_name=f'VOICE_BACKUP_CURRENT_TIME_{self.app.language}',
                    dynamic=True
                    )

        return t



    async def text_to_speech(self,
                             text: str,
                             language: str ='en-GB',
                             name: str ='en-GB-Neural2-B',
                             audio_type: str ='mp3',
                             leds: bool = True
                             ):
        """
        INPUTS:
                text - A text for the robot to speak
                language - language to speak
                name - voice from the API's list of voices
                audio_type - audio file type (mp3, wav, etc..)
                leds - whether to turn on leds or not

        OUTPUTS:
                This function doesn't return any outputs, it speaks 'text'
        """

        # Synthesize the input text, choose voice configuration
        synthesized_input = texttospeech.SynthesisInput(text = text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=name,
            ssml_gender=texttospeech.SsmlVoiceGender.MALE)
        audio_config = texttospeech.AudioConfig(
                                audio_encoding=texttospeech.AudioEncoding.MP3,
                                speaking_rate = 0.9
                                )
        
        # Get the response from the API
        response = self.app.text_to_speech_client.synthesize_speech(
                                                    input=synthesized_input,
                                                    voice=voice,
                                                    audio_config=audio_config
                                                    )

        # Write the audio response to a file
        with open_file(f'{AUDIO_PATH}/gary_response.{audio_type}', 'wb') \
                                                             as gary_response:
            gary_response.write(response.audio_content)

        gary_response_path = f'{AUDIO_PATH}/gary_response.{audio_type}'
        self.app.audio_duration = \
                    eyed3.load(resolve_path(gary_response_path)).info.time_secs

        # Turn on leds
        if leds is True:
            try:
                await self.turn_on_leds(rep_time=int(self.app.audio_duration))

            except Exception as e:
                self.app.log.warn(
                    f'Got exception {e} in text_to_speech method, skipping leds')

        # Play the audio file
        try:
            await self.app.sound.play_sound(
                                path=f'{AUDIO_PATH}/gary_response.{audio_type}',
                                callback_finish = self.cb_finish_sound
                                )
        except Exception as e:
            self.app.log.warning(f'Skipped playing sound, got error {e}')



    async def turn_on_leds(self,
                           rep_time: int = 3,
                           group: str = 'head',
                           animation: str = 'MOTION_4',
                           color: str = 'BLUE',
                           wait: bool = True
                           ):
        """
        INPUTS:
                rep_time - repetition time in seconds
                group - leds group to turn on (head, skirt, etc..)
                animation - type of animation to play
                color - animation color
                wait - whether to wait for the command to finish or not

        OUTPUTS:
                This function doesn't return any outputs, it turns on the leds
        """
        
        try:
            await self.app.leds.animation(
                group = group,
                color = color,
                animation = animation,
                speed = 7,
                repetitions = int(0.3 * rep_time) + 1,
                wait = wait)

        except Exception as e:
            self.app.log.warn(f'Skipped leds, got exception {e}')



    async def navigate(self,
                       x: float,
                       y: float,
                       angle: float,
                       screen: dict,
                       pos_unit: POSITION_UNIT = POSITION_UNIT.METERS,
                       ang_unit: ANGLE_UNIT = ANGLE_UNIT.RADIANS):
        """
         Wrapper for navigation with a UI screen
        INPUTS:
                x - x coordinate in the map to navigate to
                y - y coordinate in the map to navigate to
                angle - angle in the map to navigate to
                screen - UI screen to show whilst navigating
                pos_unit - measurement unit for the coordinates
                ang_unit - measurement unit for the angle

        OUTPUTS:
                This function doesn't return any outputs, it navigates
        """
        await self.app.ui.display_screen(**screen)
        await self.app.nav.navigate_to_position(
                                    x = x,
                                    y = y,
                                    angle = angle,
                                    pos_unit = pos_unit,
                                    ang_unit = ang_unit,
                                    wait = True,
                                    callback_feedback = self.cb_nav_feedback,
                                    callback_finish = self.cb_nav_finish
                                    )



    async def download_voice(self,
                       text: str,
                       file_name: str,
                       language: str = 'en-GB',
                       name: str = 'en-GB-Neural2-B',
                       audio_type: str = 'mp3',
                       dynamic: bool = False
                       ):
        """
        Download a custom voice to the robot
        INPUTS:
                text - A text for the robot to download
                file_name - name to save the audio file
                language - language of the audio
                name - name of the voice from the API's voice list
                audio_type - audio file type (mp3, wav, etc..)
                dynamic - whether to always download the voice, or download it
                          only if it doesn't exist

        OUTPUTS:
                This function doesn't return any outputs, it saves a file
        """

        # Get relevant path
        path = f'{AUDIO_PATH}/{file_name}.{audio_type}'

        # If the voice isn't downloaded already, or dynamic flag is up,
        #  download it
        if not check_file_exists(path) or dynamic is True:
            self.app.dynamic_recordings_list.append(path.strip(f'/{AUDIO_PATH}'))
            self.app.log.info(f'Downloading audio: \'{path}\'')
            synthesized_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=name,
                ssml_gender=texttospeech.SsmlVoiceGender.MALE)

            audio_config = texttospeech.AudioConfig(
                                audio_encoding=texttospeech.AudioEncoding.MP3,
                                speaking_rate = 0.9
                                )
            
            response = self.app.text_to_speech_client.synthesize_speech(
                                                    input=synthesized_input,
                                                    voice=voice,
                                                    audio_config=audio_config
                                                    )
            with open_file(path, 'wb') as gary_response:
                gary_response.write(response.audio_content)



    async def download_all_voices(self):
        '''Download all of the application voices'''
        create_dat_folder(AUDIO_PATH)
        for voice in self.app.audio_dict:
            await self.download_voice(**self.app.audio_dict[voice])



    def reverse_dict(self, original_dict: dict):
        '''Reverse keys and values for dictionary'''
        reversed_dict = {value: key for key, value in original_dict.items()}
        return reversed_dict
    


    def strip_prefix_suffix_from_keys(self, orig_dict: dict, prefix: str):
        '''Strip a chosen prefix from keys of a dictionary'''
        prefix_len = len(prefix)
        new_dict = {}
        for key, value in orig_dict.items():
            if key.startswith(prefix):
                key = key[prefix_len:]
            if key.endswith(prefix):
                key = key[:-prefix_len]
            new_dict[key] = value
        return new_dict
    


    def combine_dicts(self, dict_ids: dict, dict_timestamps: dict):
        '''
        Combine two dictionaries with the same keys to a new dictionary where
        each value is a dict containing the values of the original dict
        '''
        combined_dict = {}
        for name in dict_ids:
            combined_dict[name] = {
                'buffer_id': dict_ids[name],
                'timestamp': dict_timestamps[name]
            }

        return combined_dict

    

    async def play_predefined_sound_v2(self,
                                       recording_name: str,
                                       leds: bool = True,
                                       wait: bool = True
                                       ):
        """"
        Play predefined sound with the sound controller patch
        INPUTS:
                recording_name - name of the audio file to play
                leds - whether to turn on the leds whilst playing the audio
                wait - whether to wait for the audio to finish or not

        OUTPUTS:
                This function doesn't return any outputs, it plays a recording
        """

        buffer_id = recording_name['buffer_id']
        rec_time = recording_name['timestamp']

        leds_data = {'group' : 'head',
                        'color' : 'blue',
                        'animation' : 'MOTION_4',
                        'speed' : 7,
                        'repetitions' : int(0.3*rec_time)+1,
                        'wait' : False
                        }
        try:
            await self.app.sound.cancel_all_sounds()
            await self.app.leds.turn_off_group(group = 'head')
        
        except Exception as e:
            self.app.log.debug(
                f"Couldn't cancel sounds and leds \
                            in play_predefined_sound_v2, got exception - {e}" )

        try:
            self.app.sound._playing_buffers_ids.update(BUFFER_IDS)
            await self.app.sound._play_buffer(
                                buff_id = buffer_id,
                                leds = leds,
                                leds_data = leds_data,
                                wait = wait
                                )

        except Exception as e:
            self.app.log.debug(f"Couldn't play sound {recording_name} \
                               got exception - {e}")



    async def get_buffers_dict(self,
                                leds: bool = False,
                                wait: bool = True,
                                save: bool = False,
                                buffer_id: str = None,
                                dynamic: bool = True
                                ):
        '''
        Get the dictionary containing the buffer ids with their corresponding
        recording name. The function plays each sound and assigns it to a buffer
        INPUTS:
            leds - whether to play leds (the param is required in the sound
                    controller patch, its auto set to False in this wrapper)
            wait - whether to wait when playing the sound
            save - whether to save the sound
            buffer_id - buffer to assign (the param is required in the sound
                        controller patch, its auto set to None in order to
                        generate a buffer id)
            dynamic - whether to assign a buffer to a recording or not if it
                      already exists

        OUTPUTS:
            This function has no outputs. It sets a buffer dictionary attribute
        '''

        # Get the list of recordings to process, depending on whether all
        # voices should be downloaded, or just dynamic ones
        path = f'{AUDIO_PATH}'
        i = 1
        self.rec_times = {}
        recordings_list = os.listdir(resolve_path(path)) if not dynamic else \
                                            self.app.dynamic_recordings_list
        
        # Play the recording, assign a buffer ID to it
        for recording in recordings_list:
            print(
                f'playing recording: {recording} | [{i}/{len(recordings_list)}]')
            try:
                if self.app.sound.is_playing():
                    await self.app.sound.cancel_all_sounds()

                start_time = time.time()
                await self.app.sound.play_sound(
                                path=f'{AUDIO_PATH}/{recording}',
                                callback_finish = self.cb_finish_sound,
                                wait = wait,
                                save = save,
                                leds = leds,
                                leds_data = {},
                                volume = 0,
                                buffer_id = buffer_id
                                )
                end_time = time.time()
                self.rec_times[recording] = abs(end_time-start_time)
                print(f'time: {abs(end_time-start_time)}'),
                print('-'*75)

            except Exception as e:
                self.app.log.debug(f'got exception - {e} in get_buffers_dict')
            i += 1
        
        # Print the results
        self.current_buffer_dict = self.app.sound._get_audio_dict()
        print('-'*100)
        print('BUFFER DICT:')
        print(self.current_buffer_dict)
        print(f'RECORDING TIMES:')
        print(self.rec_times)
        


    async def play_predefined_sound(self,
                                    recording_name: str,
                                    audio_type: str = 'mp3',
                                    leds: str = True,
                                    wait: str = True,
                                    save : str= False,
                                    buffer_id: str = None
                                    ):
        
        """"
        Play predefined sound 
        INPUTS:
                recording_name - name of the audio file to play
                audio_type - audio file type (mp3, wav, etc..)
                leds - whether to turn on the leds whilst playing the audio
                wait - whether to wait for the audio to finish or not
                save - whether to save the buffer or not
                buffer_id - whether to play a specific buffer id or not

        OUTPUTS:
                This function doesn't return any outputs, it plays a recording
        """

        # Get the path to the recording
        path = f'{AUDIO_PATH}/{recording_name}.{audio_type}'

        if audio_type == 'mp3':  # TODO: Add something more robust than eyed3 package
            self.app.audio_duration = eyed3.load(resolve_path(path)).info.time_secs
        
        # Turn on leds
        if leds:
            leds_data = {'group' : 'head',
                        'color' : 'blue',
                        'animation' : 'MOTION_4',
                        'speed' : 7,
                        'repetitions' : int(0.3*self.app.audio_duration)+1,
                        'wait' : False
                        }
        else:
            leds_data = {}

        # Play the recording
        try:
            if self.app.sound.is_playing():
                await self.app.sound.cancel_all_sounds()
                await self.app.leds.turn_off_group(group = 'head')

            await self.app.sound.play_sound(
                            path=f'{AUDIO_PATH}/{recording_name}.{audio_type}',
                            callback_finish = self.cb_finish_sound,
                            wait = wait,
                            save = save,
                            leds = leds,
                            leds_data = leds_data,
                            buffer_id = buffer_id
                            )

        except Exception as e:
            self.app.log.debug(f'got exception - {e} in play_predefined_sound')



    async def wait_for_button(self,
                            screen: dict,
                            rep_time: int = 10,
                            button_type: str = 'start'
                            ):
        '''
        Wait for the user to press a button
        INPUTS:
            screen - the screen to display
            rep_time - the time after which the instructions are repeated if
                        the button is not pressed
            button_type - the type of button, either 'start' to start actions
                        or 'abort' to cancel the treatment

        OUTPUTS:
            The function has no outputs, it simply waits for the user to press
            a button before performing the next action
        '''

        # Reset feedbacks
        self.reset_user_feedbacks()

        # Display start button, start a timer for repeating the instructions
        if button_type == 'start':
            counter = 0
            await self.app.ui.display_action_screen(**screen,
                                                    callback=self.cb_ui_feedback
                                                    )
        
        # Repeat the instructions every rep_time until button is pressed
        while self.app.ui_button_feedback != 'button pressed':
            if self.app.stop_condition is True or self.app.dev_mode_flag is True:
                break

            if counter % rep_time == 0:

                if button_type == 'start':
                    await self.play_predefined_sound_v2(
                        self.combined_dict[
                            f'VOICE_PRESS_BUTTON_{self.app.language}'])

                if button_type == 'abort':
                    await self.play_predefined_sound_v2(
                        self.combined_dict[
                            f'VOICE_ABORT_REASON_{self.app.language}'])

            await self.app.sleep(1.0)
            counter += 1

        # Activate leds when button is pressed, reset the button feedback
        await self.play_predefined_sound_v2(
            self.combined_dict[f'button_pressed_sound.wav'],
            leds = False,
            wait = False
            )
        await self.turn_on_leds(animation = 'MOTION_10_VER_3',
                            color = 'green',
                            wait = True
                            )
        


    def reset_user_feedbacks(self):
        '''Reset any UI feedback given by the user'''
        self.app.ui_button_feedback = None
        self.app.ui_button_feedback_id = None
        self.app.video_feedback = None
        self.app.games_feedback = {'action' : None,
                                   'completed_cards' : 0,
                                   'amount_of_cards' : 0,
                                   'failed_attempts' : 0,
                                   'successful_guess' : 0,
                                   'stage' : 1,
                                   'last_try_success' : False
                                   }
        self.app.approach_successful = False



    async def send_fleet_status(self, msg: str, status: FLEET_UPDATE_STATUS):
        '''Send a message to the fleet'''
        await self.app.fleet.update_app_status(
            task_id=self.app.task_id,
            status=status,
            message=msg
        )



    async def create_listeners(self):
        '''Create fleet and chest button listeners for treatment cancellation'''
        self.app.fleet.set_msgs_from_fleet_callback(
                                callback = self.cb_fleet_messages,
                                callback_async = self.async_cb_fleet_messages)
        
        self.app.sensors.create_threshold_listener(listener_name = CHEST_SENSOR,
                                            callback_async = self.async_cb_chest_button,
                                            sensors_paths = CHEST_SENSOR_PATH,
                                            higher_bound = 10,
                                            lower_bound = 1e-10)


    async def look_around(self):
        '''Try to move backwards or turn backwards in case the robot is stuck'''
        try:
            # await self.app.motion.move_linear(distance = -0.1,
            #                               x_velocity = 0.05,
            #                               wait = True)
            await self.move_linear_wrapper(distance = -0.1,
                                           x_velocity = 0.05,
                                           wait = True)        
        except Exception as e:
            try:
                # await self.app.motion.rotate(angle = 180,
                #                          angular_speed = ROTATE_SPEED,
                #                          wait = True)
                await self.rotate_wrapper(angle = 180,
                                          angular_speed = ROTATE_SPEED,
                                          wait = True)
            except Exception as e:
                self.app.log.debug(
                            f'Got exception - {e} while trying to look around')



    def abort(self, message):
        raise NurseAidFSMAborted(message)

    

    async def update_fleet(self,
                           info_message,
                           status_type = FLEET_UPDATE_STATUS.INFO):
        '''Update the fleet'''
        self.app.log.warn(info_message.upper())
        await self.app.fleet.update_app_status(
                            task_id=self.app.task_id, 
                            status = status_type, 
                            message=info_message)
        
    

    def inverse_angle(self,
                      angle: int
                      ):
        '''Get the inverse of an angle'''
        inverse = (angle + 180) % 360
        if inverse < 0:
            inverse += 360
        return inverse


    def get_projected_point(self,
                            detection_pose: Pose,
                            distance: float
                            ):
        '''
        Get x y coordinates to navigate to in order to be "distance" away
        from the detection
        INPUTS
            detection_pose - pose of the detection in quanternion
            distance - desired distance between the robot and the detection
        
        OUTPUTS
            projected_point - an x, y coordinate
        '''
        det_x = detection_pose.position.x
        det_y = detection_pose.position.y
        quaternion = (
            detection_pose.orientation.x,
            detection_pose.orientation.y,
            detection_pose.orientation.z,
            detection_pose.orientation.w
        )
        euler = tf_transformations.euler_from_quaternion(quaternion)
        tag_orientation = euler[2]  

        point_x = det_x + distance * math.cos(tag_orientation)
        point_y = det_y + distance * math.sin(tag_orientation)

        projected_point = PointStamped()
        projected_point.point = Point(x = point_x, y = point_y, z = 0.0)

        return projected_point         


    async def approach_sequence(self):
        '''
        Navigate towards a patient at a predefined distance
        The function returns a bool indicating whether the approach was
        successful
        '''

        # Reset the detections and wait 3 seconds to obtain new ones
        # Create face detection listener
        self.app.face_detector.set_img_detections_callback(
                    callback = self.callback_all_faces,
                    as_dict = True,
                    call_without_detections = True,
                    cameras_controller = self.app.cameras
                )
        self.app.face_detections = {}
        await self.app.sleep(3.0)

        # Check if path is available
        if self.app.face_detections: 
            current_detection = self.app.face_detections[0]
            face_position = current_detection['center_point_map']

            goal_predict = Pose()
            goal_predict.position = Point(x = face_position[0],
                                        y = face_position[1],
                                        z = face_position[2])
            target_angle = self.inverse_angle(self.app.angle_initial)
            quat = tf_transformations.quaternion_from_euler(        
                                                    0.0,
                                                    0.0,
                                                    np.deg2rad(target_angle)
                                                    )
            goal_predict.orientation = Quaternion(x=quat[0], y=quat[1],
                                                    z=quat[2], w=quat[3]
                                                    )

            projected_point = self.get_projected_point(
                        detection_pose = goal_predict,
                        distance = APPROACH_EXECUTE_ARGS['distance_to_goal']
                        ).point
            
            self.app.path_available = await self.check_path_available(
                                                        projected_point.x,
                                                        projected_point.y,
                                                        self.app.angle_initial
                                                        )
            
            print(f'path available: {self.app.path_available}')


        # Compute the desired coordinates to navigate to
        if self.app.path_available and not self.app.nav.is_navigating():
            self.app.path_available = False

            # Inform patient of arrival
            await self.app.ui.display_animation(**UI_APPROACHING)
            await self.play_predefined_sound_v2(
                self.combined_dict[f'VOICE_APPROACHING_{self.app.language}'])

            # Navigate towards the patient
            try:
                await self.app.nav.navigate_to_position(
                                    x = projected_point.x,
                                    y = projected_point.y,
                                    angle = self.app.angle_initial,
                                    pos_unit = POSITION_UNIT.METERS,
                                    ang_unit = ANGLE_UNIT.DEGREES,
                                    wait = True,
                                    callback_feedback = self.cb_nav_feedback,
                                    callback_finish = self.cb_nav_finish
                                    )
                return True

            except Exception as e:
                self.app.log.debug(f'got exception - {e} in approach_sequence')

            return False


    async def check_path_available(self,
                                   x,
                                   y,
                                   angle,
                                   pos_unit = POSITION_UNIT.METERS,
                                   ang_unit = ANGLE_UNIT.DEGREES
                                   ):
        try:
            await self.app.nav.navigate_to_position( 
                x = float(x), 
                y = float(y), 
                angle = float(angle), 
                pos_unit = pos_unit, 
                ang_unit = ang_unit,
                callback_feedback = self.cb_nav_feedback,
                callback_finish = self.cb_nav_finish,
                options={"behavior_tree": "compute_path"},
                wait=True,
            )
            self.app.log.debug(f'path {x, y, angle} available!')
            return True
        except Exception as e:
            self.app.log.debug(f'path {x, y, angle} not available!')
            return False
          

    async def stinky_feet_sequence(self):
        '''
        Approach to feet sequence
        The function returns a bool indicating whether the approach was
        successful
        '''
         # Reset feet detection flag, create a queue
        self.app.feet_detected = False
        feet_detected_at_least_once = False
        self.feet_queue = deque(maxlen=5)

        # Create listener
        self.app.feet_detector.set_img_detections_callback(
                callback = self.cb_stinky_feet,
                as_dict = True,
                call_without_detections = True,
                cameras_controller = self.app.cameras
            )
        
        # Inform the patient, give the model a few seconds to detect
        await self.play_predefined_sound_v2(
            self.combined_dict[
                f'VOICE_PLEASE_TUCK_LEGS_1_{self.app.language}'])
        await self.app.sleep(3.0)
        
        # Scan backwards, left and right, if you cant find a detection
        if not self.app.feet_detected:
            await self.play_predefined_sound_v2(
                self.combined_dict[
                    f'VOICE_RETRYING_TO_REACH_TARGET_{self.app.language}'])
            await self.scan_for_detection()

        # Move forwards as long as you detect feet
        while self.app.feet_detected:
            feet_detected_at_least_once = True
            try:
                # await self.app.motion.set_velocity(
                #     x_velocity = 0.03,
                #     y_velocity = 0.0,
                #     angular_velocity = 0.0,
                #     duration = 0.75,
                #     enable_obstacles = False,
                #     wait = False
                # )
                await self.set_velocity_wrapper(
                    x_velocity = 0.03,
                    y_velocity = 0.0,
                    angular_velocity = 0.0,
                    duration = 0.75,
                    enable_obstacles = False,
                    wait = False
                )

                # Stop moving if you're too close
                if self.app.distance_to_feet < FEET_DIST_BEFORE_STOP or  \
                    self.is_bbox_at_bottom(image = self.current_image,
                                            thresh_percentage = 0.1,
                                            bbox_ymin = self.app.bbox_ymin
                                            ) or self.app.stop_condition or self.app.dev_mode_flag:
                    break
            except Exception as e:
                self.app.log.warn(f'linear movement failed, error: {e}')
            
        # When the feet are no longer detected, compute the final distance
        # to move forwards
        if self.app.distance_to_feet > 0 and \
                feet_detected_at_least_once and not self.app.stop_condition:  
            try:
                unweighted_distance = np.mean(self.feet_queue)
                weighted_distance = self.check_final_queue(self.feet_queue)

                if type(weighted_distance) is not int:
                    weighted_distance = unweighted_distance

                self.app.log.warn(f'Moving final distance - {weighted_distance}')
                # await self.app.motion.move_linear(
                #     distance = weighted_distance,
                #     x_velocity = 0.03,
                #     wait = True,
                #     callback_feedback_async = self.cb_motion,
                #     enable_obstacles = False
                # )
                await self.move_linear_wrapper(distance = weighted_distance,
                                                x_velocity = 0.03,
                                                wait = True,
                                                callback_feedback_async = self.cb_motion,
                                                enable_obstacles = False) 
            except Exception as e:
                self.app.log.warn(f"Couldn't move final distance - \
                                    {self.app.distance_to_feet} because of \
                                    error - {e}")

            return True        
        return False



    def check_final_queue(self,
                          queue: deque
                          ):
        '''
        Compute weighted average using a gaussian filter
        '''

        # Get mean and std, initiate params
        queue_mean = np.mean(queue)
        queue_std = np.std(queue)

        weights = np.exp(-0.5 * ((queue - queue_mean) / (queue_std)) ** 2)
        normalized_weights = weights / weights.sum()
        weighted_average = np.sum(queue * normalized_weights)
        
        return weighted_average



    def is_bbox_at_bottom(self,
                          image: np.array,
                          thresh_percentage: int,
                          bbox_ymin: int
                          ):
        '''
        Check if a bounding box is at the bottom of the image
        INPUTS
            image - an image array
            threshold_percentage - the percentage of the image to consider
                                    a detection to be at the bottom
            bbox_ymin - the lowest point of the detection

        OUTPUTS
            The function returns a bool indicating whether a detection is at
            the bottom of the image or not
        '''
        height = image.shape[0]
        if height - bbox_ymin < thresh_percentage * height:
            return True
        return False



    async def get_user_feedback(self):
        '''Ask the patient for feedback on the treatment'''

        # Reset feedbacks and timer
        self.reset_user_feedbacks()
        counter = 0

        # Display the feedback options
        await self.app.ui.display_choice_selector(**UI_FEEDBACK_END_TREATMENT,
                                                  callback=self.cb_ui_feedback,
                                                  wait = False)
        
        # Repeat the question every 20 sec, for 90 sec max 
        start_time = time.time()
        while self.app.ui_button_feedback != 'button pressed' and \
                                                counter < INSTRUCTIONS_TIMEOUT:

            self.app.log.debug(
                        f'ui button feedback: {self.app.ui_button_feedback}')

            if self.app.stop_condition is True or self.app.dev_mode_flag is True:
                break

            if counter%20 == 0:
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_FEEDBACK_{self.app.language}'],
                        wait = False
                        )

            counter += 1
            await self.app.sleep(1)
        
        end_time = time.time()
        self.app.treatment_time = end_time - start_time
        await self.play_predefined_sound_v2(
            self.combined_dict[f'button_pressed_sound.wav'],
            leds = False,
            wait = False
            )
        await self.turn_on_leds(animation = 'MOTION_10_VER_3',
                            color = 'green',
                            wait = True
                            )
        # Update fleet
        try:
            user_choice = self.app.ui_button_feedback_id['selected_option']['id']
            USER_FEEDBACK = {5 : 'גבוהה', 6 : 'בינונית', 7 : 'נמוכה'}

            if USER_FEEDBACK[user_choice] == 'גבוהה':
                await self.play_predefined_sound(
                                    f'VOICE_FEEDBACK_GOOD_{self.app.language}')
            elif USER_FEEDBACK[user_choice] == 'בינונית':
                await self.play_predefined_sound(
                                    f'VOICE_FEEDBACK_OKAY_{self.app.language}')
            elif USER_FEEDBACK[user_choice] == 'נמוכה':
                await self.play_predefined_sound(
                                    f'VOICE_FEEDBACK_BAD_{self.app.language}')


            await self.update_fleet(f"המטופל נתן פידבק {USER_FEEDBACK[user_choice]}")

        except Exception as e:
            self.app.log.warn(f'Got exception {e} in user_feedback, skipping it')



    async def user_setup_sequence(self):
        '''
        UI screens and voices to explain the patient that they are about to
        start a treatment, verify their IDs and clicking tool preferences
        '''

        # Create all of the tasks
        running_tasks = [self.app.ui.display_animation(**UI_INTRODUCTION),
                         self.play_predefined_sound_v2(self.combined_dict[
                             f'VOICE_INTRODUCTION_{self.app.language}']),
                         self.select_finger_or_wand(),
                         self.verify_id(),
                         self.app.ui.display_animation(**UI_GUIDELINES),
                         self.play_predefined_sound_v2(
                             self.combined_dict[
                                 f'VOICE_GUIDELINES_{self.app.language}']),
                         self.app.ui.display_animation(**UI_DANIEL_IS_A_MEME),
                         self.play_predefined_sound_v2(
                             self.combined_dict[
                                 f'VOICE_DANIEL_IS_A_MEME_{self.app.language}']),
                         self.app.ui.display_screen(**UI_STOP_CONDITION),
                         self.turn_on_leds(group = 'chest',
                                        rep_time = 6,
                                        color = 'red',
                                        animation = 'MOTION_2',
                                        wait = True
                                        ),
                         self.play_predefined_sound_v2(
                             self.combined_dict[
                                 f'VOICE_STOP_CONDITION_{self.app.language}']),
                         self.app.ui.display_animation(**UI_BEFORE_ACTIVITIES),
                         self.play_predefined_sound_v2(
                             self.combined_dict[
                                 f'VOICE_BEFORE_ACTIVITIES_{self.app.language}'])
                         ]
        
        # Run tasks, stop incase of stop flag
        for task in running_tasks:
            if self.app.stop_condition or self.app.bad_id or self.app.dev_mode_flag:
                return
            else:
                await task


    async def select_finger_or_wand(self):
        '''Get the clicking tool preference of the user'''

        # Reset previous feedbacks, display the choice selector
        self.reset_user_feedbacks()
        await self.play_predefined_sound_v2(
            self.combined_dict[
                f'VOICE_EXPLAIN_FINGER_OR_WAND_{self.app.language}'])
        await self.app.ui.display_choice_selector(
                                                **UI_SELECT_WAND_OR_FINGER,
                                                callback = self.cb_ui_feedback,
                                                wait = False
                                                )
        await self.play_predefined_sound_v2(
            self.combined_dict[
                f'VOICE_FINGER_OR_WAND_CHOICE_{self.app.language}'],
                wait = False
                )

        # Repeat the instructions every rep_time until button is pressed
        start_time = time.time()
        counter = 1

        while self.app.ui_button_feedback == None:
            if self.app.stop_condition is True or self.app.dev_mode_flag is True:
                break

            if counter%INSTRUCTIONS_REP_TIME  == 0:
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_FINGER_OR_WAND_CHOICE_{self.app.language}'],
                        wait = False
                        )
                                                 
            await self.app.sleep(1)   
            counter += 1

        end_time = time.time()
        self.app.touch_item_time = end_time - start_time
        self.app.log.info(f"{self.app.ui_button_feedback}")
        
        try:
            await self.play_predefined_sound_v2(
                self.combined_dict[f'button_pressed_sound.wav'],
                leds = False,
                wait = False
                )
            await self.turn_on_leds(animation = 'MOTION_10_VER_3',
                                color = 'green',
                                wait = True
                                )
            
            # Set the clicking tool preferences based on the user's choice
            if self.app.ui_button_feedback_id['selected_option']['id'] == \
                                                         TOUCH_ITEM['Wand']:
                self.app.touch_item = 'Wand'
                await self.app.ui.display_animation(**UI_TAKE_STICK)
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_TAKE_STICK_{self.app.language}'])
                await self.app.sleep(3)
                
            elif self.app.ui_button_feedback['selected_option']['id'] == \
                                                         TOUCH_ITEM['Hand']:
                self.app.touch_item = 'Hand'
                
        except Exception as e:
            self.app.log.warn(f'Got exception {e} in select_finger_or_wand function, skipping it')



    async def verify_id(self):
        '''Verify the ID of the patient'''

        # Reset feedbacks and timer
        self.reset_user_feedbacks()
        counter = 1

        # Choose the screen based on the language
        verification_screen = UI_USER_VERIFY_1
        if self.app.language == 'HEBREW':
            verification_screen['title'] = \
                            f'לפני שנתחיל, האם השם הוא {self.app.patient_name}?'
        elif self.app.language == 'ENGLISH':
            verification_screen['title'] = \
                     f'Before we begin, is your name {self.app.patient_name}?'

        # Ask the user to verify their ID
        await self.app.ui.display_screen(**verification_screen)
        await self.app.sleep(0.5)

        await self.play_predefined_sound_v2(
            self.combined_dict[
                f'VOICE_VERIFY_PATIENT_{self.app.language}'],
                wait = False
                )
        await self.app.sleep(1.0)
        await self.app.ui.display_choice_selector(
                                                **UI_USER_VERIFY_2,
                                                callback = self.cb_ui_feedback,
                                                wait = False
                                                )

        # Repeat the verification until a timeout is reached or the button was
        # pressed
        while self.app.ui_button_feedback != 'button pressed' and \
                                                counter < INSTRUCTIONS_TIMEOUT:

            if self.app.stop_condition is True or self.app.dev_mode_flag is True:
                break
                
            if counter%INSTRUCTIONS_REP_TIME == 0:
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_VERIFY_PATIENT_{self.app.language}'])
                

            counter += 1
            await self.app.sleep(1)
        
        # The button was pressed or timeout occured
        await self.play_predefined_sound_v2(
            self.combined_dict[f'button_pressed_sound.wav'],
            leds = False,
            wait = False
            )
        await self.turn_on_leds(animation = 'MOTION_10_VER_3',
                            color = 'green',
                            wait = True
                            )

        # Leave the room if either no feedback is given or if its the wrong
        # patient, otherwise continue
        if self.app.ui_button_feedback is None or \
            self.app.ui_button_feedback_id['selected_option']['id'] == \
                                                        USER_VERIFY['False']:
            await self.play_predefined_sound_v2(
                self.combined_dict[
                    f'VOICE_ABORTED_BY_PATIENT_{self.app.language}'])
            self.app.bad_id = True
            return
        
        self.app.user_verification_successful = True



    async def brief_patient(self):  
        '''
        UI screens and voices to give the patient a brief of the treatment
        '''      
        ui_session_screen = UI_SESSION_SCREEN

        if self.app.language == 'HEBREW':
            ui_session_screen['title'] = \
                    f'אורך התרגול היום יהיה כ-{int(self.app.treatment_time)} דקות'
            ui_session_screen['subtitle'] = \
                                f'כולל {", ".join(self.app.session_order_keys)}'

        if self.app.language == 'ENGLISH':
            ui_session_screen['title'] = \
                f"Today's session will be {int(self.app.treatment_time)} minutes"
            ui_session_screen['title'] = \
                f"Including {', '.join(self.app.session_order_keys)}"

        # Create tasks
        running_tasks = [
            self.app.ui.display_animation(**UI_GOOD_DAY),
            self.get_current_time(speech = True),
            self.app.ui.display_animation(**UI_BELINSON),
            self.play_predefined_sound_v2(
                self.combined_dict[f'VOICE_BELINSON_{self.app.language}']),
            self.app.ui.display_screen(**UI_ACTIVITIES),
            self.play_predefined_sound_v2(
                self.combined_dict[f'VOICE_ACTIVITIES_{self.app.language}']),
            self.app.ui.display_screen(**UI_SESSION_SCREEN),
            self.play_predefined_sound_v2(
                self.combined_dict[f'VOICE_EXPLAIN_SESSION_{self.app.language}'])
            ]
        
        # Run tasks, stop incase of stop flag
        for task in running_tasks:
            if self.app.stop_condition is True or self.app.dev_mode_flag is True:
                return
            else:
                await task
    


    def temp_get_audio(self):
        '''
        Temporary way to get the dictionary with the buffer ID and recording
        time, until we apply the changes to the sound controller that the
        patch currently covers
        '''
        self.static_buffer_dict = self.reverse_dict(BUFFER_IDS)
        self.static_buffer_dict = self.strip_prefix_suffix_from_keys(
                                        orig_dict = self.static_buffer_dict,
                                        prefix = 'dat:tts_audio/'
                                        )
        self.static_buffer_dict = self.strip_prefix_suffix_from_keys(
                                        orig_dict = self.static_buffer_dict,
                                        prefix = '.mp3'
                                        )
        self.rec_times_dict = self.strip_prefix_suffix_from_keys(
                                                        orig_dict = REC_TIMES,
                                                        prefix = '.mp3'
                                                        )


        self.dynamic_buffers_dict = self.reverse_dict(self.current_buffer_dict)
        self.dynamic_buffers_dict = self.strip_prefix_suffix_from_keys(
                                        orig_dict = self.dynamic_buffers_dict,
                                        prefix = 'dat:tts_audio/'
                                        )
        self.dynamic_buffers_dict = self.strip_prefix_suffix_from_keys(
                                        orig_dict = self.dynamic_buffers_dict,
                                        prefix = '.mp3'
                                        )
        

        for item in self.app.dynamic_recordings_list:
            self.static_buffer_dict[item.strip('.mp3')] = \
                                self.dynamic_buffers_dict[item.strip('.mp3')]
            self.rec_times_dict[item.strip('.mp3')] = self.rec_times[item]

        self.combined_dict = self.combine_dicts(self.static_buffer_dict, self.rec_times_dict)

        # print(f'combined dict: {self.combined_dict}')
        # print('-'*100)



    async def session_num(self, num):
        '''Perform a session based on the given order from the app args'''
        if num == 1:
            await self.cognitive_session()
        if num == 2:
            await self.video_session()
        if num == 3:
            await self.upper_limb_session()



    def choose_random_success_voice(self):
        '''
        Choose a random voice to play to the patient when they chose a correct
        answer in one of the games
        '''
        rand_num = np.random.uniform()
        if 0 <= rand_num <= 0.33:
            voice = f'VOICE_CARD_MATCH_2_{self.app.language}'
        elif 0.33 < rand_num <= 0.66:
            voice = f'VOICE_CARD_MATCH_3_{self.app.language}'
        else:
            voice = f'VOICE_CARD_MATCH_4_{self.app.language}'

        return voice
    


    def choose_random_fail_voice(self):
        '''
        Choose a random voice to play to the patient when they chose an
        incorrect answer in one of the games
        '''
        rand_num = np.random.uniform()
        if 0 <= rand_num <= 0.5:
            voice = f'VOICE_CARD_MISMATCH_1_{self.app.language}'
        elif 0.5 < rand_num <= 1.0:
            voice = f'VOICE_CARD_MISMATCH_2_{self.app.language}'

        return voice



    async def cognitive_session(self):
        await self.update_fleet("התחלת פעילות משחקים")

        # By default, the touch option is by hand, unless the user chose with a
        # wand
        with_wand=False
        if self.app.touch_item == 'Wand':
            with_wand=True
        
        # Give guidelines and instructions
        await self.exercise_instructions()
        await self.wait_for_button(screen = UI_BEGIN, button_type = 'start')
        
        # Open the games one by one
        await self.difference_game()
        await self.memory_game()
        await self.trivia_game()
        # await self.simon_game()

        # Give the user instructions after the games 
        await self.exercise_instructions(return_wand = with_wand)
        await self.app.sleep(1)
        await self.app.ui.display_screen(**UI_CONGRATS)


    async def video_session(self):
        await self.update_fleet("התחלת ציפייה בסרטוני הדרכה")
        await self.create_session(link = self.app.video_link, video = True)
        

    async def upper_limb_session(self):
        await self.update_fleet('התחיל תרגול גפה עליונה')
        await self.exercise_instructions(full_instructions = True)
        await self.play_predefined_sound(f'VOICE_MOVING_BACKWARDS_{self.app.language}')
        await self.app.motion.set_velocity(x_velocity = -0.03,
                                           y_velocity = 0.0,
                                           angular_velocity = 0.0,
                                           duration = 5.0,
                                           ang_unit = ANGLE_UNIT.RADIANS,
                                           wait = True
                                           )
        await self.create_session(link = self.app.exercise_link, video = True)
        await self.play_predefined_sound(f'VOICE_MOVING_FORWARDS_{self.app.language}')
        await self.app.motion.set_velocity(x_velocity = 0.03,
                                           y_velocity = 0.0,
                                           angular_velocity = 0.0,
                                           duration = 5.0,
                                           ang_unit = ANGLE_UNIT.RADIANS,
                                           wait = True
                                           )
        

    async def exercise_instructions(self, return_wand = False, full_instructions = False):

        # Ask patient to return the wand in the end of a screen exercise
        if return_wand is True:
            await self.app.ui.display_animation(UI_RETURN_STICK)
            await self.play_predefined_sound(f'VOICE_RETURN_STICK_{self.app.language}')
            await self.app.sleep(0.5)

        # Give full instructions when not doing a screen exercise
        elif full_instructions is True:
            running_tasks = [
                self.app.ui.display_animation(UI_SESSION_EMPHASES),
                self.play_predefined_sound(f'VOICE_SESSION_EMPHASES_{self.app.language}'),
                self.app.ui.display_animation(UI_SIT_STRAIGHT),
                self.play_predefined_sound(f'VOICE_SIT_STRAIGHT_{self.app.language}'),
                self.app.ui.display_animation(UI_LEGS_ON_FLOOR),
                self.play_predefined_sound(f'VOICE_LEGS_ON_FLOOR_{self.app.language}'),
                self.app.ui.display_animation(UI_STRAIGHT_HEAD),
                self.play_predefined_sound(f'VOICE_STRAIGHT_HEAD_{self.app.language}'),
                self.app.ui.display_animation(UI_NO_TIME_FOR_CAUTION),
                self.play_predefined_sound(f'VOICE_NO_TIME_FOR_CAUTION_{self.app.language}')
                ]

            # Run tasks, stop incase of stop flag
            for task in running_tasks:
                if self.app.stop_condition is True:
                    return
                else:
                    await task


    async def difference_game(self):
        '''Open a difference game session'''

        # Reset feedback
        self.reset_user_feedbacks()

        # Open game
        await self.app.ui.open_game(
            game = 'FindDifference',
            back_button_text = '',
            title = 'אנא לחצו כדי להתחיל',
            button_text = 'התחל',
            pageTitle = 'מצא את ההבדלים',
            theme = UI_THEME_TYPE.WHITE,
            difficulty = self.app.difference_game_difficulty,
            wait = False,
            feedback_callback_async = self.async_cb_feedback_games,
            finish_callback_async = self.async_cb_finish_games,
            custom_style = CUSTOM_STYLE,
            photo_title = '',
            loaderTime = '15',
            loaderText = '!בהצלחה',
            chosen_language = self.app.language[:2].lower(),
            end_game_text = 'End Game',
            show_start_modal = False,
            start_button_timeout = 0.0
        )

        # Explain the game
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_DIFFERENCE_GAME_{self.app.language}'])
            

        # Play the game
        last_stage = self.app.games_feedback['stage']
        last_feedback = self.app.games_feedback.copy()
        i = 0
        while self.app.games_feedback['action'] != 'game-completed':
            # Continue to next stage
            if self.app.games_feedback['stage'] != last_stage and \
                                    last_feedback != self.app.games_feedback:
                last_stage = self.app.games_feedback['stage']
                last_feedback = self.app.games_feedback.copy()
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_CONTINUE_STAGE_{self.app.language}'])

            # Correct guess feedback
            elif self.app.games_feedback['last_try_success'] and  \
                                    last_feedback != self.app.games_feedback:
                last_feedback = self.app.games_feedback.copy()

                if self.app.games_feedback['successful_guess'] == 1:
                    await self.play_predefined_sound_v2(
                        self.combined_dict[
                            f'VOICE_CARD_MATCH_1_{self.app.language}'])
                else:
                    voice = self.choose_random_success_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice])

            # Incorrect guess feedback
            elif not self.app.games_feedback['last_try_success'] and \
                                    last_feedback != self.app.games_feedback:
                last_feedback = self.app.games_feedback.copy()

                if i%2 == 0:
                    voice = self.choose_random_fail_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice])
                i += 1
               

            if self.app.ui_button_feedback == 'button_pressed' or \
                                            self.app.stop_condition is True:
                break
            
            await self.app.sleep(1.0)

        # Congratulate the patient upon game completion
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_GAME_COMPLETED_{self.app.language}'])


    async def memory_game(self):
        '''Open a memory game session'''

        # Reset feedback
        self.reset_user_feedbacks()
        await self.app.ui.open_game(
                        game = 'MemoryGame',
                        difficulty = self.app.memory_game_difficulty,
                        back_button_text = '',
                        title = 'משחק הזכרון',
                        button_text = 'התחל',
                        loaderText = '!בהצלחה',
                        loaderTime = '5',
                        theme = UI_THEME_TYPE.WHITE,
                        show_start_modal = True,
                        start_button_timeout = 7.0,
                        chosen_language = self.app.language[:2].lower(),
                        end_game_text = 'End Game',
                        wait = False,
                        feedback_callback_async = self.async_cb_feedback_games,
                        finish_callback_async = self.async_cb_finish_games,
                        custom_style = CUSTOM_STYLE_GAMES
                        )
        
        # Explain the game
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_MEMORY_GAME_{self.app.language}'])
       
        # Give the patient feedback until the game is complete
        last_feedback = self.app.games_feedback.copy()
        i = 0
        while self.app.games_feedback['action'] != 'game-completed':
            # Correct card match feedback
            if self.app.games_feedback['last_try_success'] and \
                                     self.app.games_feedback != last_feedback:
                last_feedback = self.app.games_feedback.copy()
                if self.app.games_feedback['completed_cards'] == 2:
                    await self.play_predefined_sound_v2(
                        self.combined_dict[
                            f'VOICE_CARD_MATCH_1_{self.app.language}'])
                elif self.app.games_feedback['completed_cards'] == \
                                 self.app.games_feedback['amount_of_cards']-2:
                    await self.play_predefined_sound_v2(
                        self.combined_dict[
                            f'VOICE_CARD_MATCH_LAST_{self.app.language}'])
                else:
                    voice = self.choose_random_success_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice])
        

            # Incorrect card match feedback
            elif not self.app.games_feedback['last_try_success'] and \
                self.app.games_feedback['failed_attempts'] != \
                                            last_feedback['failed_attempts']:
                last_feedback = self.app.games_feedback.copy()        
                if i%2 == 0:
                    voice = self.choose_random_fail_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice])
                else:
                    await self.play_predefined_sound_v2(
                                    self.combined_dict['wrong_answer_sound'])
                i += 1
        

            # Break if stop condition
            if self.app.ui_button_feedback == 'button_pressed' or self.app.stop_condition is True:
                break

            await self.app.sleep(1.0)

        # Congratulate the patient upon game completion
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_GAME_COMPLETED_{self.app.language}'])
    


    async def trivia_game(self):
        '''Open a trivia game session'''

         # Reset feedback
        self.reset_user_feedbacks()

        loader_time = '21'
        await self.app.ui.open_game(
                        game = 'MemoryTriviaGame',
                        difficulty = self.app.trivia_game_difficulty,
                        back_button_text = '',
                        button_text = 'התחל',
                        title = 'משחק זכרון תמונות',
                        photo_title = 'התבוננו וזכרו את פרטי התמונה',
                        loaderText = '!בהצלחה',
                        chosen_language = self.app.language[:2].lower(),
                        end_game_text = 'End Game',
                        loaderTime = loader_time,
                        show_start_modal = True,
                        start_button_timeout = 7.0,
                        theme = UI_THEME_TYPE.WHITE,
                        wait = False,
                        feedback_callback_async = self.async_cb_feedback_games,
                        finish_callback_async = self.async_cb_finish_games,
                        custom_style = CUSTOM_STYLE_GAMES)
            
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_TRIVIA_GAME_{self.app.language}'])

        # Repeat the instructions every 10 seconds until the game started
        num_instructions_reps = 0
        last_feedback = self.app.games_feedback
        start_time, current_time = time.time(), time.time()
        while self.app.games_feedback['action'] != 'game-started' and \
                                                    num_instructions_reps < 3:
            await self.app.sleep(1.0)
            current_time = time.time()
            if abs(current_time - start_time) >= 30:
                num_instructions_reps += 1
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_TRIVIA_GAME_{self.app.language}'])
                start_time = time.time()

        # Wait the countdown, speak the question
        loader_start_time, loader_current_time = time.time(), time.time()
        try:
            await self.app.leds.turn_off_group('head')
            await self.app.leds.animation(group = 'head',
                                color = 'blue',
                                animation = 'TIMER_COUNT_DOWN',
                                speed = 10,
                                repetitions = int(0.5*int(loader_time)),
                                wait = False
                                )
        except Exception as e:
            self.app.log.debug(f'Couldnt count down leds, got exception - {e}')

        while abs(loader_current_time - loader_start_time) <= int(loader_time)-1:
            loader_current_time = time.time()
            await self.app.sleep(0.1)

        last_feedback = self.app.games_feedback.copy()
        await self.play_predefined_sound_v2(self.combined_dict[f'VOICE_TRIVIA_Q1_{self.app.trivia_game_difficulty.upper()}_{self.app.language}'])
        await self.play_predefined_sound_v2(self.combined_dict[f'VOICE_TRIVIA_A1_{self.app.trivia_game_difficulty.upper()}_{self.app.language}'], wait = False)

        # Measure the patient response time between instructions and start
        self.app.memory_game_response_time = current_time - start_time

        # Give the patient feedback until the game is complete
        i, j = 1, 2
        while self.app.games_feedback['action'] != 'game-completed':
            # Correct card match feedback
            if self.app.games_feedback['last_try_success'] and \
                                    self.app.games_feedback != last_feedback:

                last_feedback = self.app.games_feedback.copy()       
                voice = self.choose_random_success_voice()
                await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice],
                                                    wait = True)

                loader_start_time, loader_current_time = time.time(), time.time()
                try:
                    await self.app.leds.turn_off_group('head')
                    await self.app.leds.animation(group = 'head',
                                        color = 'blue',
                                        animation = 'TIMER_COUNT_DOWN',
                                        speed = 10,
                                        repetitions = int(0.5*int(loader_time)),
                                        wait = False
                                        )
                except Exception as e:
                    self.app.log.debug(f'Couldnt count down leds, got exception - {e}')

                while abs(loader_current_time - loader_start_time) \
                                                         <= int(loader_time)-1:
                    loader_current_time = time.time()
                    await self.app.sleep(0.1)

                if j <= 3:
                    await self.play_predefined_sound_v2(self.combined_dict[f'VOICE_TRIVIA_Q{j}_{self.app.trivia_game_difficulty.upper()}_{self.app.language}'])
                    await self.play_predefined_sound_v2(self.combined_dict[f'VOICE_TRIVIA_A{j}_{self.app.trivia_game_difficulty.upper()}_{self.app.language}'], wait = False)
                j += 1

            # Incorrect card match feedback
            elif not self.app.games_feedback['last_try_success'] and \
                                    self.app.games_feedback != last_feedback:
                last_feedback = self.app.games_feedback.copy()            
               
                if i%2 == 0:
                    voice = self.choose_random_fail_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice],
                                                    wait = False)
                i += 1
            
            # Break if stop condition
            if self.app.ui_button_feedback == 'button_pressed' or \
                                            self.app.stop_condition is True:
                break

            await self.app.sleep(1.0)

        # Congratulate the patient upon game completion
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_GAME_COMPLETED_{self.app.language}'])

        # Analytics
        end_time = time.time()
        self.app.trivia_game_time = end_time - start_time


    
    async def simon_game(self):
        '''Open a simon says game session'''

         # Reset feedback
        self.reset_user_feedbacks()        
        await self.app.ui.open_game(
                        game = 'SimonGame',
                        difficulty = self.app.simon_game_difficulty,
                        back_button_text = '',
                        button_text = 'התחל',
                        title = 'המלך אמר',
                        show_start_modal = True,
                        start_button_timeout = 7.0,
                        theme = UI_THEME_TYPE.WHITE,
                        chosen_language = self.app.language[:2].lower(),
                        end_game_text = 'End Game',
                        wait = False,
                        feedback_callback_async = self.async_cb_feedback_games,
                        finish_callback_async = self.async_cb_finish_games,
                        custom_style = CUSTOM_STYLE_GAMES
                        )
        
        # Explain the game
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_SIMON_GAME_{self.app.language}'])

        # Repeat the instructions every 10 seconds until the game started
        num_instructions_reps = 0
        last_feedback = self.app.games_feedback
        start_time, current_time = time.time(), time.time()
        while self.app.games_feedback['action'] == None and  \
                                                    num_instructions_reps < 3:
            await self.app.sleep(1.0)
            current_time = time.time()
            if abs(current_time - start_time) >= 30:
                num_instructions_reps += 1
                await self.play_predefined_sound_v2(
                    self.combined_dict[f'VOICE_SIMON_GAME_{self.app.language}'])
                start_time = time.time()
        last_feedback = self.app.games_feedback

        
        # Give the patient feedback until the game is complete
        last_stage = self.app.games_feedback['stage']
        last_feedback = self.app.games_feedback.copy()
        i, j = 0, 2
        while self.app.games_feedback['action'] != 'game-completed':
            # Incorrect card match feedback
            if not self.app.games_feedback['last_try_success'] and \
                                    self.app.games_feedback != last_feedback:
                last_feedback = self.app.games_feedback.copy()                    
                if i%2 == 0:
                    voice = self.choose_random_fail_voice()
                    await self.play_predefined_sound_v2(
                                                    self.combined_dict[voice])
                i += 1

            # Break if stop condition
            if self.app.ui_button_feedback == 'button_pressed' or \
                                            self.app.stop_condition is True:
                break

            await self.app.sleep(1.0)

        # Congratulate the patient upon game completion
        await self.play_predefined_sound_v2(
            self.combined_dict[f'VOICE_GAME_COMPLETED_{self.app.language}'])



    async def scan_for_detection(self):
        '''Move backwards and scan left \ right to search for detections'''
        # running_tasks = [
        #     self.app.motion.move_linear(distance = -0.2,
        #                                 x_velocity = 0.05,
        #                                 wait = True
        #                                 ),
        #     self.app.motion.rotate(angle = 20.0,
        #                            angular_speed = 5.0,
        #                            wait = True
        #                            ),
        #     self.app.motion.rotate(angle = -40.0,
        #                            angular_speed = 5.0,
        #                            wait = True
        #                            )
        # ]
        running_tasks = [
            self.move_linear_wrapper(distance = -0.2,
                                           x_velocity = 0.05,
                                           wait = True
                                           ),
            self.rotate_wrapper(angle = 20.0,
                                angular_speed = 5.0,
                                wait = True
                                ),
            self.rotate_wrapper(angle = -40.0,
                                angular_speed = 5.0,
                                wait = True
                                )
        ]

        # Run tasks unless stop condition is met
        for task in running_tasks:
            if self.app.feet_detected:
                break
            else:
                try:
                    await task
                except Exception as e:
                    self.app.log.debug(
                                f'got exception - {e} in scan_for_detection')
        
        # Orient the robot's angle to be towards the patient after the scan
        await self.app.nav.go_to_angle(self.app.angle_initial, 0.05, wait = True)



    async def return_home(self):
        '''Navigate to a predefined home position'''
        await self.navigate(x = NAV_POINT_HOME['x'],
                            y = NAV_POINT_HOME['y'],
                            angle = NAV_POINT_HOME['angle'],
                            screen = UI_NAVIGATING_TO_HOME,
                            pos_unit = NAV_POINT_HOME['pos_unit'],
                            ang_unit = NAV_POINT_HOME['ang_unit']
                            )



    async def request_help_from_fleet(self):
        '''
        Request help from the fleet
        The function returns a bool indicating the fleet user's response
        '''
        self.app.fleet_request_counter += 1
        try:
            response = await self.app.fleet.request_action(title = 'גרי צריך עזרה',
                                                message = 'נתקעתי. בבקשה בואו לעזור לי',
                                                task_id = self.app.task_id,
                                                timeout = 90.0)
            if response == 'Okay, coming':
                ans = await self.app.ui.display_modal(**UI_REQUEST_FLEET_HELP)
                if ans['action'] == 'confirmed':
                    return True
                
        except Exception as e:
            return False
        
    

    def calculate_distance_to_image_center(self,
                                           detection: dict,
                                           image: np.array,
                                           only_y: bool = False
                                           ):
        
        '''
        Calculate the distance of a detection from the image center
        INPUTS
            detection - a dictionary with the detection's info
            image - the image on which the detection was obtained
            only_y - whether the distance should be calculated only on the y
                    axis or not
        
        OUTPUTS
            distance - the distance of the detection from the image's center
        '''
        # Calculate the center of the image
        image_center_x, image_center_y = image.shape[0]/2, image.shape[1]/2

        # Calculate the center of the face
        face_center_x = detection['object_center_px'][0]
        face_center_y = detection['object_center_px'][1]

        # Calculate the distance to the image center
        if only_y:
            distance = abs(face_center_y - image_center_y)
            return distance
        
        distance = math.sqrt((face_center_x - image_center_x)**2 + \
                                        (face_center_y - image_center_y)**2)
        
        return distance
    
    
    async def prehome_motions(self):
        try:
            await self.app.motion.move_linear(
                                    distance = 0.25,
                                    x_velocity = -0.1,
                                    wait = True)
            await self.app.motion.rotate(angle = 180.0,
                                        angular_speed = 20.0,
                                        wait = True,
                                        enable_obstacles = False)
        except Exception as e:
                self.app.log.warn(f'Failed at prehome motions - {e}')
    
    #------------------------------- Callbacks -------------------------------#

    async def cb_belinson_approach_feedback(self, feedback):
        self.app.belinson_approach_feedback = feedback
        self.app.log.debug(feedback)
        if feedback['status_msg'] == 1:
            await self.app.ui.display_animation(**UI_APPROACHING)
            await self.play_predefined_sound_v2(
                self.combined_dict[f'VOICE_APPROACHING_{self.app.language}'])
            
        if feedback['status_msg'] == 2:
            await self.play_predefined_sound_v2(
            self.combined_dict[
                f'VOICE_PLEASE_TUCK_LEGS_1_{self.app.language}'])

    
    def callback_all_faces(self, detections, image):
        if detections:
            self.app.face_detections = sorted(detections,
                key = lambda x: (self.calculate_distance_to_image_center(
                                    x, image,
                                    only_y = True),
                                    -x['confidence'])
                )
            self.app.face_detections = [self.app.face_detections[0]]
       


    async def async_cb_sound(self, arg1, arg2, arg3):
        self.app.can_play_sound = False

    async def async_cb_finish_sound(self, status, status_msg):
        self.app.can_play_sound = True
    


    def cb_finish_sound(self, status, status_msg):
        pass

    def cb_stinky_feet(self, predictions, image):
        '''Callback used to obtain predictions'''
        self.current_image = image                        
        if predictions:

            # Sort predictions based on - 
            # 1. distance from image center
            # 2. distance from the robot
            # 3. prediction confidence
            sorted_detections = sorted(
                                predictions,
                                key = lambda x: \
                                    (self.calculate_distance_to_image_center(
                                                    x, image, only_y = True),
                                        x['distance'],
                                        -x['confidence']
                                        )
                                    )

            # Filter the predictions based on threshold and size
            filtered_predictions = [item for item in sorted_detections if \
                    item['confidence'] >= FEET_DETECTION_THRESHOLD \
                            and 0.01 < (item['height'] * item['width']) \
                                                        < FEET_SIZE_THRESHOLD]
            

            # Take the first 2 items from the filtered predictions. They are
            # assumed to be the feet of the patient
            if len(filtered_predictions) > 0:
                if len(filtered_predictions) > 2:
                    filtered_predictions = filtered_predictions[:2]
                self.app.distance_to_feet = \
                    filtered_predictions[0]['center_point'][0] - DISTANCE_CONST
                self.app.bbox_ymin = filtered_predictions[0]['y_min']
                self.feet_queue.append(self.app.distance_to_feet)
                self.app.feet_detected = True
            else:
                self.app.feet_detected = False
            
    
    async def cb_motion(self, msg1 ,msg2, msg3, msg4):
        # Stop movement in case of stop condition
        if self.app.stop_condition:
            await self.app.motion.cancel_motion()


    def cb_fleet_messages(self, message_dict):
        '''Create an async callback for fleet messages'''
        try:
            self.app.create_task(name = 'fleet messages',
                             afunc = self.async_cb_fleet_messages,
                             message_dict = message_dict)
        except Exception as e:
            print(f'Error in cb_fleet_messages {e}')


    async def async_cb_fleet_messages(self, message_dict):
        '''Obtain messages sent from the fleet'''
        self.fleet_messages = message_dict.values()

        # Stop the app from the fleet
        if FLEET_STOP_COMMAND in self.fleet_messages:
            self.app.stop_condition_counter += 1
            self.app.stop_condition = True
            self.app.stop_fleet = True
    

    def cb_chest_button(self):
        '''Create an async callback for chest button press'''
        try:
            self.app.create_task(name = 'ui select feedback',
                                 afunc = self.async_cb_chest_button,
                                error = '',
                                error_msg = ''
                                )
        except Exception as e:
            self.app.log.info(f'Error in cb_chest_button {e}')


    async def async_cb_chest_button(self):
        '''Initiate app stop condition if the chest button is pressed'''

        # Set stop condition flag
        self.app.stop_condition = True
        self.app.stop_condition_counter += 1
        self.app.press2reaction_time = time.time()

        # Stop playing sounds and turn off leds
        try:
            await self.app.sound.cancel_all_sounds()
            await self.app.leds.turn_off_group(group = 'head')
            await self.app.nav.cancel_navigation()

        except Exception as e:
            self.app.log.warn(f'Got exception {e}, skipping it')




    def cb_nav_feedback(self, error, error_msg, distance_to_goal, speed):
        '''Create an async navigation callback'''
        try:
            self.app.create_task(name='nav feedback',
                                afunc=self.async_cb_nav_feedback,
                                error=error,
                                error_msg=error_msg,
                                distance_to_goal=distance_to_goal,
                                speed=speed
                                )
        except Exception as e:
            self.app.log.warn(f'Got error in cb_nav_feedback - {e}')
        

    async def async_cb_nav_feedback(self,
                                    error,
                                    error_msg,
                                    distance_to_goal,
                                    speed
                                    ):
        '''Navigation callback'''

        # Download dynamic voices while navigating to the patient (only on
        # first navigation)
        if self.app.one_time_action_flag:
            self.app.one_time_action_flag = False
            await self.get_buffers_dict(dynamic = True)   
            self.temp_get_audio()
            
        # Print the current actions
        if self.app.nav_feedback != error_msg:
            self.app.log.info(f'Action: {error_msg} | ID: {error}')

        # Actions for obstacle management
        if error == OBSTACLE_DICT['Waiting obstacle to move']:
            self.app.obstacle_counter += 1
            if self.app.obstacle_counter%3 == 0:
                await self.play_predefined_sound_v2(
                    self.combined_dict[
                        f'VOICE_PLEASE_MOVE_{self.app.language}'])

        # Set the current feedback to the error message
        self.nav_feedback = error_msg



    def cb_nav_finish(self, error, error_msg):
        '''Create an async callback for navigation finish'''
        try:
            self.app.create_task(name='nav finish',afunc=self.async_cb_nav_finish,
                        error=error,
                        error_msg=error_msg,
                        )
        except Exception as e:
            print(f'Error in cb_nav_finish {e}')



    async def async_cb_nav_finish(self, error, error_msg):
        '''Async callback for navigation finish'''
        pass



    def cb_video_links(self, error):
        '''Create an async callback for video using links'''
        self.app.create_task(name = 'ui video link',
                             afunc = self.async_cb_video_links,
                             error = error
                             )


    # Async feedback for web links
    async def async_cb_video_links(self, error):
        '''Async callback for videos using links'''
        self.app.video_feedback = error['action']
        print(f'video feedback: {self.app.video_feedback}')


    async def async_cb_feedback_games(self, error):
        '''Async callback for games'''
        
        # Pretty display
        if self.app.games_feedback != error:
            self.app.log.info(f'Action: {error}')

        # Update feedback
        for key in error:
            self.app.games_feedback[key] = error[key]
        
        # Log
        self.app.log.debug(f'GAMES FEEDBACK: {self.app.games_feedback}')




    async def async_cb_finish_games(self, error):
        '''Async callback for games finish'''
        for key in error:
            self.app.games_feedback[key] = error[key]
        self.app.log.debug(f'GAMES FINISH: {error}')



    async def error_messanger(self, state, exception, counter, max_counter):
        '''Display an error to the developer when a state is failing'''
        await self.app.sleep(1.0)
        self.app.log.debug(f'Exception - {exception}')
        self.app.log.debug(f'Failed in state {state}. due to the exception above. \
                       Attempt {counter}/{max_counter}')
    

     
    def cb_ui_feedback(self, error, error_msg = 'button pressed'):
        '''Create an async UI callback'''
        try:
            self.app.create_task(name = 'ui feedback',
                                afunc = self.async_cb_ui_feedback,
                                error = error,
                                error_msg = error_msg
                                )
        except Exception as e:
                pass



    async def async_cb_ui_feedback(self, error, error_msg):
        '''Async UI selectors callback'''
        if self.app.ui_button_feedback != error_msg:
            self.app.log.info(f'Action: {error_msg} | ID: {error}')

        if self.app.sound.is_playing():
            try:
                await self.app.sound.cancel_all_sounds()
            except Exception as e:
                self.app.log.warn(f'Got exception {e}, skipping it')

        self.app.ui_button_feedback = error_msg
        self.app.ui_button_feedback_id = error

       

    async def async_stop_treatment_feedback(self, error):
        if self.app.sound.is_playing():
            try:
                await self.app.sound.cancel_all_sounds()
            except Exception as e:
                self.app.log.warn(f'Got exception {e}, skipping it')

        self.app.exit_choice = error['selected_option']['id']
    


    async def move_linear_wrapper(self,
                                  distance,
                                  x_velocity,
                                  callback_feedback_async = None,
                                  enable_obstacles = True,
                                  y_velocity = 0.0,
                                  wait = False,
                                  ):
        await self.app.motion.move_linear(distance = distance,
                                          x_velocity = x_velocity,
                                          y_velocity = y_velocity,
                                          wait = wait,
                                          callback_feedback_async = callback_feedback_async,
                                          enable_obstacles = enable_obstacles)
        

    async def rotate_wrapper(self,
                            angle,
                            angular_speed,
                            enable_obstacles = True,
                            wait = False
                            ):
        await self.app.motion.rotate(angle = angle,
                                     angular_speed = angular_speed,
                                     enable_obstacles = enable_obstacles,
                                     wait = wait)
        
    
    async def set_velocity_wrapper(self,
                                   x_velocity,
                                   duration,
                                   enable_obstacles,
                                   y_velocity = 0.0,
                                   angular_velocity = 0.0,
                                   wait = False
                                   ):
        await self.app.motion.set_velocity(
                    x_velocity = x_velocity,
                    y_velocity = y_velocity,
                    angular_velocity = angular_velocity,
                    duration = duration,
                    enable_obstacles = enable_obstacles,
                    wait = wait
                )
    