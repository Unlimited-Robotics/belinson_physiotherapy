# Raya Imports
from raya.tools.fsm import BaseTransitions
from src.FSMs.nurse_aid.helpers import Helpers
from src.app import RayaApplication
from src.FSMs.nurse_aid.constants.navigation_constants import *
from src.FSMs.nurse_aid.constants.ui_hebrew import *
from ...app import RayaApplication
from raya.exceptions import *

# Other Imports
import time
import asyncio


class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers
                

    async def SETUP(self):
        if self.app.dev_mode_flag:
           
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

         # If the robot is localized, navigate to the room
        elif self.app.robot_localized:
            self.helpers.reset_variables()
            self.set_state('NAVIGATING_TO_ROOM')

        # If the robot is not localized and max attempts was reached, abort.
        elif self.app.localizing_attempts > MAX_LOCALIZATION_ATTEMPTS:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_COULDNT_LOCALIZE_{self.app.language}')
            self.helpers.abort(**ERROR_LOCALIZING)
        
        # If the robot is not localized and max attempts wasnt reached,
        # try again
        else:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_RETRYING_TO_LOCALIZE_{self.app.language}')
            self.app_last_state = 'SETUP'
            self.set_state('IDLE')



    async def NAVIGATING_TO_ROOM(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the navigation to the room was successful, approach the patient
        elif self.app.navigation_successful:
            self.helpers.reset_variables(exclude_groups = ['approach'])
            self.set_state('APPROACHING_PERSON')
        
        # If the nav wasn't successful and max attempts was reached, abort
        elif self.app.navigation_attempts > MAX_NAVIGATION_ATTEMPTS:
            fleet_response = await self.helpers.request_help_from_fleet()
            await self.helpers.play_sound_with_leds(
                    f'VOICE_COULDNT_REACH_ROOM_{self.app.language}')
            if fleet_response:
                self.helpers.reset_variables()
            else:
                self.set_state('NAVIGATING_HOME')

        # If nav wasn't successful and max attempts wasnt reached, try again
        else:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_RETRYING_TO_REACH_ROOM_{self.app.language}')
            self.app.last_state = 'NAVIGATING_TO_ROOM'
            self.set_state('IDLE')



    async def APPROACHING_PERSON(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the approach was successful, Gary introduces themselves
        elif self.app.approach_successful:
            # Reset variables
            self.helpers.reset_variables(exclude_groups = ['approach'])
            self.set_state('USER_SETUP')
        
        # If the approach wasn't successful and max attempts was reached, abort
        elif self.app.approach_attempts > MAX_APPROACH_ATTEMPTS:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_COULDNT_REACH_TARGET_{self.app.language}')
            self.set_state('NAVIGATING_HOME')

        # If the approach wasn't successful and max attempts wasnt reached,
        # try again
        else:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_RETRYING_TO_REACH_TARGET_{self.app.language}')
            self.set_state('NAVIGATING_TO_ROOM')

    

    async def APPROACHING_FEET(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the approach was successful, Gary introduces themselves
        elif self.app.feet_approach_successful:
            # Disable models
            try:
                await self.app.cv.disable_model(self.app.feet_detector)
                await self.app.cv.disable_model(self.app.face_detector)
            except Exception as e:
                self.app.log.debug(f"Couldn't disable model - {e}")

            # Reset variables
            self.helpers.reset_variables()
            self.set_state('USER_SETUP')
        
        # If the approach wasn't successful and max attempts was reached, abort
        elif self.app.approach_attempts > MAX_APPROACH_ATTEMPTS:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_COULDNT_REACH_TARGET_{self.app.language}')
            self.set_state('NAVIGATING_HOME')

        # If the approach wasn't successful and max attempts wasnt reached,
        # try again
        else:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_RETRYING_TO_REACH_TARGET_{self.app.language}')
            self.set_state('')



    async def USER_SETUP(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the user verification was successful, begin treatment brief
        elif self.app.user_verification_successful:
            self.helpers.reset_variables()
            self.set_state('SESSIONS')

        elif self.app.user_setup_attempts > MAX_USER_SETUP_ATTEMPTS:
            self.set_state('NAVIGATING_HOME')



    async def BRIEF(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the brief was successful, begin the actual treatment
        elif self.app.brief_successful:
            self.helpers.reset_variables()
            self.set_state('SESSIONS')
        
        # If the brief wasn't successful and max attempts was reached, abort
        elif self.app.brief_attempts > MAX_BRIEF_ATTEMPTS:
            self.set_state('NAVIGATING_HOME')
        
        # If the brief wasn't successful and max attempts wasnt reached,
        # try again
        else:
            self.app_last_state = 'BRIEF'
            self.set_state('IDLE')



    async def SESSIONS(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the sessions were successful, return home
        elif self.app.sessions_successful:
            self.helpers.reset_variables()
            await self.helpers.prehome_motions()
            self.set_state('NAVIGATING_HOME')
        
        # If the sessions weren't successful and max attempts was reached,
        # abort
        elif self.app.sessions_attempts > MAX_SESSIONS_ATTEMPTS:
            self.set_state('NAVIGATING_HOME')
        
        # If the sessions weren't successful and max attempts wasnt reached,
        # try again
        else:
            self.app.last_state = 'SESSIONS'
            self.set_state('IDLE')



    async def NAVIGATING_HOME(self):
        if self.app.dev_mode_flag:
            self.set_state('IDLE')

        if self.app.stop_condition:
            self.set_state('TREATMENT_PAUSE')

        # If the navigation was successful, end the app
        elif self.app.navigation_successful:
            self.helpers.reset_variables()
            end_time = time.time()
            self.app.end_to_end_time = end_time - self.app.end_to_end_timer
            self.app.end_to_end_success = True
            self.set_state('END')
        
        # If the navigation wasn't succesful and max attempts was reached, abort
        elif self.app.navigation_attempts > MAX_NAVIGATION_ATTEMPTS:
            fleet_response = await self.helpers.request_help_from_fleet()
            if fleet_response:
                self.helpers.reset_variables()
            else:
                self.helpers.abort(**ERROR_NAVIGATING)
        
        # If the navigation wasn't successful and max attempts wasnt reached, try again
        else:
            self.app_last_state = 'NAVIGATING_HOME'
            self.set_state('IDLE')



    async def TREATMENT_PAUSE(self):
        # Go home if the conclusion of the pause was to stop the treatment
        if self.app.stop_treatment:
            self.helpers.reset_variables()
            self.set_state('NAVIGATING_HOME')
        
        # Otherwise, rever to the last state, and restore the sessions in case
        # the treatment was stopped during the sessions
        else:
            # Only revert to the last state after an exit choice was made
            self.app.stop_condition = False
            while self.app.exit_choice not in self.helpers.reverse_dict(EXIT_OPTION):
                await self.app.sleep(0.5)
                print(f'app exit choice: {self.app.exit_choice}')
                print(f'reverse dict: {self.helpers.reverse_dict(EXIT_OPTION)}')
            
            await self.helpers.play_sound_with_leds(
                'button_pressed_sound.wav',
                leds = False,
                wait = False
                )
            await self.helpers.turn_on_leds(animation = 'MOTION_10_VER_3',
                            color = 'green',
                            wait = True
                            )

            self.exit_choice_human_format = \
                                            self.helpers.reverse_dict(EXIT_OPTION)
            self.exit_choice_human_format = \
                    self.exit_choice_human_format[self.app.exit_choice]
            self.app.exit_choices.append(self.exit_choice_human_format)
            self.app.button_press_success = True

            if self.app.exit_choice == EXIT_OPTION['Sick'] or \
                self.app.exit_choice == EXIT_OPTION['Other']:
                    await self.helpers.play_sound_with_leds(
                        f'VOICE_EXIT_CHOICE_LEAVE_{self.app.language}')
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
                        self.app.log.warn(f'Got exception - {e} in TREATMENT_PAUSE')
                        
                    self.set_state('NAVIGATING_HOME')
            else:
                await self.helpers.play_sound_with_leds(
                    f'VOICE_EXIT_CHOICE_STAY_{self.app.language}')
        
            self.helpers.reset_variables()
            self.app.session_order_values = list(self.app.sessions_order.values())
            self.app.session_order_keys = list(self.app.sessions_order.keys())
            self.set_state('IDLE')
        
    

    async def IDLE(self):
        if self.app.dev_mode_flag:
            self.app.dev_mode_flag = False
            state_to_go_to = input('Please select a state: ').upper()
            self.app.kthread.dev_mode_flag = False
            self.set_state(str(state_to_go_to))

        else:
            self.set_state(str(self.app.last_state))
    

    async def DEBUG(self):
        self.set_state('USER_SETUP')