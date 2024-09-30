from raya.tools.fsm import BaseActions
from raya.controllers.navigation_controller import POSITION_UNIT, ANGLE_UNIT
from src.FSMs.nurse_aid.constants.navigation_constants import *
from src.FSMs.nurse_aid.constants.ui_hebrew import *
from ...app import RayaApplication


from src.FSMs.nurse_aid.helpers import Helpers
from src.FSMs.nurse_aid.tests import *
import os
import matplotlib.pyplot as plt

from raya.exceptions import *

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        self.app = app
        self.helpers = helpers


    async def enter_SETUP(self):
        # Declare the state
        self.app.last_state = 'SETUP'

        # Set the treatment stop option (decorator) inside the helpers class
        self.helpers.decorate_methods()

        # Create listeners
        await self.helpers.create_listeners()

        # Get the session time
        await self.helpers.acquire_session_time()

        # Reset the user feedbacks
        self.helpers.reset_user_feedbacks()

        # Download voices
        await self.helpers.download_all_voices()

        # Localize and update to normal footprint
        try:
            self.app.log.info('Localizing...')
            self.app.robot_localized = \
                                await self.app.nav.set_map(self.app.map_name)
            await self.app.nav.update_robot_footprint(GARY_FOOTPRINT)

        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('LOCALIZING',
                                             e,
                                             self.app.localizing_attempts,
                                             MAX_LOCALIZATION_ATTEMPTS)
            self.app.localizing_attempts += 1
            await self.helpers.look_around()



    async def enter_NAVIGATING_TO_ROOM(self):
        # Declare the state
        self.app.last_state = 'NAVIGATING_TO_ROOM'

        # Cancel navigation if you're already navigating
        if self.app.nav.is_navigating():
                await self.app.nav.cancel_navigation()

        # Navigate to the room
        try:
            await self.helpers.navigate(self.app.x_initial,
                                        self.app.y_initial,
                                        self.app.angle_initial,
                                        UI_NAVIGATING_TO_INITIAL_POSITION,
                                        pos_unit = POSITION_UNIT.PIXELS,
                                        ang_unit = ANGLE_UNIT.DEGREES)
            
            # Inform the patient about Gary's arrival
            await self.app.ui.display_animation(**UI_ARRIVING)
            await self.helpers.play_sound_with_leds(
                    f'VOICE_ARRIVING_{self.app.language}')
            
            # Update the fleet and the app flag
            await self.helpers.update_fleet('הרובוט הגיע לחדר המטופל\ת')
            self.app.navigation_successful = True

        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('NAVIGATING_TO_ROOM',
                                             e,
                                             self.app.navigation_attempts,
                                             MAX_NAVIGATION_ATTEMPTS)
            
            self.app.navigation_attempts += 1
            await self.helpers.look_around()



    async def enter_APPROACHING_PERSON(self):
        # Declare the state
        self.app.last_state = 'APPROACHING_PERSON'

        try:
            # Execute approach to face sequence
            # self.app.approach_successful = \
            #                         await self.helpers.approach_sequence()

            try:
                await self.app.skill_belinson_approach.execute_main(
                    execute_args={
                        'face_angle' : self.app.angle_initial
                    },
                    callback_feedback=self.helpers.cb_belinson_approach_feedback
                )
                self.app.approach_successful = \
                      self.app.belinson_approach_feedback['skill_success']
                
            except Exception as e:
                self.app.log.error(f'Error executing skill: {e}')

            # If the approach wasn't successful, update the counter
            if not self.app.approach_successful:
                self.app.approach_attempts += 1
             

        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('APPROACHING_PERSON',
                                             e,
                                             self.app.approach_attempts,
                                             MAX_APPROACH_ATTEMPTS)


    async def enter_APPROACHING_FEET(self):
        # Declare the state
        self.app.last_state = 'APPROACHING_FEET'
        
        try:
            # Execute approach to feet sequence
            self.app.feet_approach_successful = \
                                await self.helpers.stinky_feet_sequence()

            # If the approach wasn't successful, update the counter
            if not self.app.feet_approach_successful:
                self.app.approach_attempts += 1

        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('APPROACHING_FEET',
                                               e,
                                               self.app.approach_attempts,
                                               MAX_APPROACH_ATTEMPTS)



    async def enter_USER_SETUP(self):
        # Declare the state
        self.app.last_state = 'USER_SETUP'

        try:
            # Begin user setup (touchscreen preferences and verification)
            await self.helpers.user_setup_sequence()
            await self.helpers.update_fleet(
                                f'המטופל\ת {self.app.patient_name} זוהו בהצלחה')

        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('USER_SETUP',
                                               e,
                                               self.app.user_setup_attempts,
                                               MAX_USER_SETUP_ATTEMPTS)

    

    async def enter_BRIEF(self):
        # Declare the state
        self.app.last_state = 'BRIEF'

        try:
            # Begin session brief
            await self.helpers.brief_patient()
            self.app.brief_successful = True
        
        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('BRIEF',
                                               e,
                                               self.app.brief_attempts,
                                               MAX_BRIEF_ATTEMPTS)


    async def enter_SESSIONS(self):
        # Declare the state
        self.app.last_state = 'SESSIONS'
        
        try:
            # Pre video interactions
            await self.helpers.play_sound_with_leds(
                    f'VOICE_PREVIDEO_1_{self.app.language}')
            
            await self.helpers.play_sound_with_leds(
                    f'VOICE_PREVIDEO_2_{self.app.language}')
            
            # Start treatment
            await self.helpers.wait_for_button(screen = UI_BEGIN,
                                                    button_type = 'start'
                                                    )

            # Move backwards
            try:
                await self.helpers.play_sound_with_leds(
                    f'VOICE_MOVING_BACKWARDS_{self.app.language}')
               
                await self.app.motion.move_linear(distance = 0.2,
                                                x_velocity = -0.1,
                                                wait = True
                                                )
            except Exception as e:
                print(e)

            # Start opening videos one by one
            video_params = UI_OPEN_VIDEO
            video_params['async_callback'] = self.helpers.async_cb_video_links
            for i in range(len(self.app.videos_dict)):
                if self.app.videos_dict[f'video{i+1}']['link'] != 'no_value':

                    # Specific video instructions - shoulder fracture
                    if VIDEO_DICT[self.app.videos_dict[f'video{i+1}']['link']] \
                        == 'shoulder_fracture':
                        await self.app.ui.display_screen(**UI_SHOULDER_FRACTURE)
                        await self.helpers.play_sound_with_leds(
                            f'VOICE_SHOULDER_FRACTURE_{self.app.language}')
                    
                    video_params['url'] = \
                                    self.app.videos_dict[f'video{i+1}']['link']
                    
                    for j in range(self.app.videos_dict[f'video{i+1}']['reps']):
                        self.app.video_feedback = None 

                        # Open video, wait until finished
                        await self.app.ui.open_video(**video_params)
                        while not self.app.video_feedback:
                            await self.app.sleep(0.5)
                        
                        # Video finished interactions
                        await self.app.ui.display_screen(**UI_CONGRATS)

                if i < len(self.app.videos_dict)-1:
                    await self.helpers.play_sound_with_leds(
                        f'VOICE_NEXT_VIDEO_{self.app.language}')
                   

            # End of treatment
            await self.helpers.play_sound_with_leds(
                    f'VOICE_END_TREATMENT_{self.app.language}')

            # Move forwards
            try:
                await self.helpers.play_sound_with_leds(
                    f'VOICE_MOVING_FORWARDS_{self.app.language}')
                
                await self.app.motion.move_linear(distance = 0.15,
                                                x_velocity = 0.075,
                                                wait = True
                                                )
            except Exception as e:
                print(e)

            # Get user feedback
            await self.helpers.get_user_feedback()
            await self.app.ui.display_screen(**UI_NAVIGATING_TO_HOME)
            await self.helpers.play_sound_with_leds(
                    f'VOICE_AFTER_FEEDBACK_{self.app.language}')
            self.app.sessions_successful = True

        except Exception as e:
            self.app.sessions_successful = False
            self.app.current_error = e
            await self.helpers.error_messanger('SESSIONS',
                                               e,
                                               self.app.brief_attempts,
                                               MAX_BRIEF_ATTEMPTS)


            

    async def enter_NAVIGATING_HOME(self):
        # Declare the state
        self.app.last_state = 'NAVIGATING_HOME'

        # Disable models
        await self.app.cv.disable_all_models()

        try:
            await self.helpers.return_home()
            self.app.navigation_successful = True
            
        except Exception as e:
            self.app.current_error = e
            await self.helpers.error_messanger('NAVIGATING_HOME',
                                               e,
                                               self.app.navigation_attempts,
                                               MAX_NAVIGATION_ATTEMPTS)
            await self.helpers.look_around()



    async def enter_TREATMENT_PAUSE(self):
        # Set stop condition to false to use helpers funsctions
        self.app.stop_condition = False

        # Treatment aborted by staff
        if self.app.stop_fleet:
            await self.app.ui.display_screen(**UI_TREATMENT_STOPPED_SCREEN)
            await self.helpers.play_sound_with_leds(
                    f'VOICE_ABORTED_BY_STAFF_{self.app.language}',
                    wait = False)
            self.app.stop_treatment = True

        else:
            await self.helpers.play_sound_with_leds(
                    f'VOICE_ABORT_REASON_{self.app.language}')
    
            await self.helpers.turn_on_leds(group = 'chest',
                                            color = 'red',
                                            animation = 'MOTION_2',
                                            wait = False)
            start_time = time.time()
            self.app.press2reaction_time = round(abs(start_time - self.app.press2reaction_time), 2)
            self.app.press2reaction_times.append(self.app.press2reaction_time)

            treatment_stop_feedback = \
                await self.app.ui.display_choice_selector(
                    **UI_STOP_TREATMENT,
                    wait = False,
                    async_callback = self.helpers.async_stop_treatment_feedback
                    )

            # Set the stop condition back to True after unblocking the methods
            # For the treatment pause setup
            self.app.stop_condition = True
           
            # Analytics
            end_time = time.time()
            self.app.user_stop_states.append(self.app.last_state)
            self.app.stop_condition_timers.append(end_time - start_time)
    


    async def enter_IDLE(self):
        self.app.log.debug(f'Returning to state {self.app.last_state}')
        if self.app.nav.is_navigating():
            await self.app.nav.cancel_navigation()
        if self.app.motion.is_moving():
            await self.app.motion.cancel_motion()



    async def enter_DEBUG(self):
        self.app.log.debug(f'IN DEBUG MODE')
        self.app.last_state = 'DEBUG'

        self.helpers.decorate_methods()
        await self.helpers.create_listeners()
        await self.helpers.download_all_voices()
        await self.helpers.get_buffers_dict(dynamic = True)   
        self.helpers.temp_get_audio()
        
        await self.app.sleep(3)
        self.app.log.debug(f'DONE!')




        