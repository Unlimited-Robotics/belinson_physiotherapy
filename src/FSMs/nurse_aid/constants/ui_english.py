from raya.enumerations import UI_ANIMATION_TYPE, UI_THEME_TYPE, UI_TITLE_SIZE
from src.FSMs.nurse_aid.constants.constants import *
import time

# General background
# background_url = 'url(https://i.postimg.cc/3JbLCm8Q/belinson-3-1.png)'
background_url = 'url(/assets/belinson_logo.png)'

# Images for 'aborted by patient' sequence
# stop_treatment_regret_img = 'https://cdn-icons-png.flaticon.com/512/8541/8541369.png'
# stop_treatment_sick_img = 'https://cdn-icons-png.flaticon.com/512/6723/6723264.png'
# stop_treatment_other_img = 'https://cdn-icons-png.flaticon.com/512/3362/3362395.png'

# # Feedback images options for the treatment
# was_good_img = 'https://i.postimg.cc/MGYPrLnc/image-137.png'
# was_ok_img = 'https://i.postimg.cc/HsJNs3hK/image-136.png'
# was_bad_img ='https://i.postimg.cc/hvCqWjhd/Mask-group.png'

# true_img = "https://d1nhio0ox7pgb.cloudfront.net/_img/v_collection_png/512x512/shadow/check.png"
# false_img = "https://us.123rf.com/450wm/vectora/vectora1704/vectora170401047/75817847-red-cross-symbol-icon-as-de"

# Current time
year = time.strftime('%Y')
month = time.strftime('%B')
month_numeric = time.strftime('%m')
month_day = time.strftime('%d')
week_day = time.strftime('%A')
hour = str(int(time.strftime('%I')) + 3)
minute = time.strftime('%M')

# SCREENS
THEME = UI_THEME_TYPE.WHITE

CUSTOM_STYLE = {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                }

CUSTOM_STYLE_GAMES = {'title' : {'font-size' : '75px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                }


UI_NAVIGATING_TO_HOME = {
        'title':'On my way home 🏠', 
        'subtitle':"I've finished the treatment",
        'theme' : THEME,
        'show_loader' : True,
        'back_button_text' : '',
        'custom_style' : {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'}}
    }

UI_SCREEN_END = {
        'title':'Thanks!', 
        'subtitle':'Don\'t forget to subscribe and like 😉',
        'show_loader':False,
        'show_back_button': False,
        'theme' : THEME
    }

UI_NAVIGATING_TO_INITIAL_POSITION = {
        'title':"On my way to start a treatment",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : '',
        'show_loader' : True,
        'back_button_text' : '',
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }

UI_GOOD_DAY = {
        'title' : week_day,
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : f'{month_day}/{month_numeric}/{year}',
        'format' : UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://content.presentermedia.com/content/clipart/00003000/3878/magnify_desk_calendar_month_view_300_nwm.jpg',
        'content' : '/assets/UI_GOOD_DAY_2.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }


UI_DANIEL_IS_A_MEME = {
        'title' : "Take a break if you feel any pain",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format' : UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://media.giphy.com/media/nIYphcRREmvd7GHkHM/giphy.gif',
        'content' : '/assets/UI_DANIEL_IS_A_MEME_2.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }
    
UI_SESSION = {
        'title' : "Today's treatment length is 30 minutes",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : 'Including cognitive treatment and videos',
        'show_loader' : False,
        'back_button_text' : '',
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }


UI_BEGIN = {
    'title' : '',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : '',
    'button_text' : 'Begin',
    'back_button_text' : '',
    'button_size' : 'LARGE',
    'wait' : False,
    'theme' : THEME,
    'custom_style' : {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'button' :   {'font-size' : '200px',
                                        'width' : '80%',
                                        'height' : '60%'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                        }
    }

UI_STOP = {
    'title' : '',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : '',
    'button_text' : 'Stop',
    'back_button_text' : '',
    'button_size' : 'LARGE',
    'wait' : False,
    'theme' : THEME,
    'custom_style' : {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'button' :   {'font-size' : '200px',
                                        'width' : '80%',
                                        'height' : '60%'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                        }
    }


UI_CONTINUE_VIDEOS = {
    'title' : "Click the button to begin",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'Educational video',
    'button_text' : 'Start treatment',
    'back_button_text' : '',
    'wait' : False,
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_CONTINUE_EXERCISE = {
    'title' : "Click the button to begin",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : "Cognitive exercise",
    'button_text' : "Start treatment",
    'back_button_text' : '',
    'wait' : False,
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_END_OF_SESSION = {
    'title' : "The treatment is completed",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : "Good day",
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_OPEN_VIDEO = {
    'title' : '',
    'url' : 'https://www.youtube.com/watch?v=Kt-tLuszKBA',
    'theme' : THEME,
    'back_button_text' : '',
    'width' : '85%',
    'height' : '75%'
    }


UI_CONGRATS = {
    'title' : "Congratulations!",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : "The current part is completed",
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_SIT_STRAIGHT = {
    'title' : "Sit straight",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://businessmirror.com.ph/wp-content/uploads/2019/06/hf02-062719.jpg',
    'content' : '/assets/UI_SIT_STRAIGHT.jpg',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_LEGS_ON_FLOOR = {
    'title' : "Feet on the floor",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media.giphy.com/media/H897EyN4b6WseXBBCq/giphy.gif',
    'content' : '/assets/UI_LEGS_ON_FLOOR.gif',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_STRAIGHT_HEAD = {
    'title' : "Straight head, in line with your spine",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://blog.kakaocdn.net/dn/OA1Rg/btqGd1TrMh6/ushfpBvqnRU4rCk92HKIXk/img.png',
    'content' : '/assets/UI_STRAIGHT_HEAD.png',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_NO_TIME_FOR_CAUTION = {
    'title' : "Perform the exercises slowly and carefully",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://www.seekpng.com/png/detail/779-7794349_stop-bot-cartoon-stop-sign-with-transparent-background.png',
    'content' : '/assets/UI_NO_TIME_FOR_CAUTION.jpeg',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_SESSION_EMPHASES = {
    'title' : "Emphases for the treatment",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://www.rotary-ribi.org/upimages/PageMainPics/EARS.jpg',
    'content' : '/assets/UI_SIT_STRAIGHT.jpg',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_TAKE_STICK = {
    'title' : "Please take the wand to your right",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media0.giphy.com/media/MZXmFVrbMA1qSDNGOt/giphy.gif?cid=ecf05e47k0o5qi0r21x53t5kgtvfjsab7qx8q88pikd9lbb1&rid=giphy.gif&ct=s',
    'content' : '/assets/UI_TAKE_STICK.gif',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_RETURN_STICK = {
    'title' : "Please return the wand",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media0.giphy.com/media/MZXmFVrbMA1qSDNGOt/giphy.gif?cid=ecf05e47k0o5qi0r21x53t5kgtvfjsab7qx8q88pikd9lbb1&rid=giphy.gif&ct=s',
    'content' : '/assets/UI_TAKE_STICK.gif',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_GUIDELINES = {
    'title' : "Safety instructions",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    'content' : '/assets/UI_GUIDELINES.jpg',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_STOP_CONDITION = {
    'title' : "Emergency Button",
    'title_size' : UI_TITLE_SIZE.MEDIUM,
    # 'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    'show_loader' : False,
    # 'content' : '/assets/UI_STOP_CONDITION.gif',
    'theme' : THEME,
    'custom_style' : {'title' : {'font-size' : '130px'},
                        'subtitle' : {'font-size' : '60px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '333px',
                                    'height' : '500px'}
                        }
                                        
    }


UI_ARRIVING = {
        'title' : "I'll be right there",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'subtitle' : "Please sit straight",
        'back_button_text' : '',
        # 'content' : 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=360/uploads/users/1112/posts/25730/final_image/animate-run-progress-04.gif',
        'content' : '/assets/UI_ARRIVING.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }

UI_INTRODUCTION = {
        'title' : "Hello! I'm Billie the robot",
        'title_size' : UI_TITLE_SIZE.MEDIUM,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        #'content' : 'https://images.pond5.com/robot-and-sign-hello-seamless-footage-075074609_prevstill.jpeg',
        'content' : '/assets/gary_the_robot.png',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : {'title' : {'font-size' : '130px'},
                        'subtitle' : {'font-size' : '60px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '400px',
                                    'height' : '700px'}
                        }
    }

UI_BEFORE_ACTIVITIES = {
    'title' : 'Before we begin',
    'title_size' : UI_TITLE_SIZE.MEDIUM,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    'content' : '/assets/UI_BEFORE_ACTIVITIES.jpg',
    'show_loader' : False,
    'theme' : THEME,
    'custom_style' : {'title' : {'font-size' : '130px'},
                        'subtitle' : {'font-size' : '60px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '900px',
                                    'height' : '1000px'}
                        }
}

UI_BELINSON = {
        'title' : '',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://www.israelhayom.co.il/wp-content/uploads/2022/07/07/07/OM5_9542-600x400.jpg',
        'content' : '/assets/UI_BELINSON.jpg',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '800px',
                                    'height' : '600px'}
                        }
    }


UI_GERIATRIC = {
        'title' : "Geriatric department",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://media.giphy.com/media/zOU33C79GYLcyg6dWI/giphy.gif',
        'content' : '/assets/UI_GERIATRIC.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }


UI_ACTIVITIES = {
        'title' : "Today we'll do several activities",
        #'subtitle' : 'המרפאה לריפוי בעיסוק',
        'title_size' : UI_TITLE_SIZE.MEDIUM,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://media.giphy.com/media/JTbtvgjLN4w9jXmsS4/giphy.gif',
        'content' : '/assets/UI_ACTIVITIES.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : {'title' : {'font-size' : '130px'},
                        'subtitle' : {'font-size' : '60px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},

                        'image' : {'width' : '300px',
                                    'height' : '500px'}
                        
                        }
    }

UI_SCREEN = {
    'title' : "Click the button to use me",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'button_text' : "Click here",
    'back_button_text' : '',
    'wait' : False,
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_APPROACHING = {
        'title' : "I'm moving slowly and carefully",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQUzamS1hiJugJpXan0pKd1UAi3E-vmFnhQQ&usqp=CAU',
        'content' : '/assets/UI_APPROACHING.png',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }


UI_PICK_WAND_OR_FINGER = {
    'title' : "How would you prefer to interact with the screen?",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : "Please click your choice - finger or wand",
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : {'title' : {'font-size' : '70'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                        }
    }


UI_SELECT_WAND_OR_FINGER = {
                'title': "How would you prefer to interact with the screen?",
                'show_back_button':False,
                'data':[{
                'id': TOUCH_ITEM['Wand'],
                'name': 'Wand',
                'imgSrc' : '/assets/UI_STICK.png'
                # 'imgSrc':"https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Fi.postimg.cc%2FZY1GGrH7%2Fimage-134.png"
                    
            }, {
                'id': TOUCH_ITEM['Hand'],
                'name': 'Finger',
                'imgSrc' : '/assets/UI_HAND.jpeg'
                # 'imgSrc':"https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F158222770%2Fphoto%2Ftouch-controlled-white-virtual-screen.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3DDqO5KDPGUoddvcQdSGIQdIMLhFuD-cjyy-oFl4K6cvM%3D"
            }]
        ,
                'theme' : THEME,
                'title_size' : UI_TITLE_SIZE.LARGE,
                'custom_style' : {'title' : {'font-size' : '80px'},
                        'subtitle' : {'font-size' : '50px'},
                            "selector": {"background-color": "white",
                                        "border-width": "4px",
                                        "border-color": "#0686D8"
                                    },
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}}
                
            
}


UI_SESSION_SCREEN = {
        #'title' : f"אורך התרגול היום יהיה כ-{int(self.treatment_time)} דקות",
        #'subtitle' : 'כולל תרגול קוגנטיבי, צפייה בסרטונים, ותרגילי גפה',
        'show_loader' : False,
        'back_button_text' : '',
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
        }   


UI_TREATMENT_STOPPED_SCREEN = {
    'title' : "The treatment was stopped by the staff",
    'subtitle' : "Good day",
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_STOP_TREATMENT = {
                'title':"Why do you wish to stop the treatment?",
                'show_back_button':False,
                'data':[{
                'id': EXIT_OPTION['Other'],
                'name': 'Other',
                'imgSrc' : '/assets/UI_OTHER.png'
                # 'imgSrc': stop_treatment_other_img,
                },
                
                {'id': EXIT_OPTION['Sick'],
                'name': "Feel sick",
                'imgSrc' : '/assets/UI_SICK.png'
                # 'imgSrc': stop_treatment_sick_img
                },
                
                {'id': EXIT_OPTION['Regret'],
                'name': "Continue Treatment",
                'imgSrc' : '/assets/UI_REGRET.png'
                # 'imgSrc': stop_treatment_regret_img
                }
                ],

                'theme' : THEME,
                'title_size' : UI_TITLE_SIZE.LARGE,
                'custom_style' : {'title' : {'font-size' : '80px'},
                        'subtitle' : {'font-size' : '50px'},
                            "selector": {"background-color": "white",
                                        "border-width": "4px",
                                        "border-color": "#0686D8"
                                    },
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                            }
}


UI_CHEST_BUTTON_INTRODUCTION = {
        'title' : "To stop the treatment at any point",
        'title_size' : UI_TITLE_SIZE.MEDIUM,
        'format': UI_ANIMATION_TYPE.URL,
        'subtitle' : '',
        'back_button_text' : '',
        # 'content' : "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWZoczVxZGI4ZzFvbnJpZ3Q1emhoNm1qd2UyOXhwZDBqbG9sMno1ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1z/9PekRRQ0WlrRVwynAk/200w.gif",
        'content' : '/assets/UI_STOP_CONDITION.gif',
        'show_loader' : False,
        'theme' : THEME,
        'custom_style' : CUSTOM_STYLE
    }          


UI_CHEST_BUTTON_STOP_TRIGGER ={
    'title' : "The treatment is completed!",
    'subtitle' : "Good day",
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }

UI_FEEDBACK_END_TREATMENT={
                'title':"How was the treatment?",
                'show_back_button':False,
                'data':[{
                'id': 5,
                'name':  "Good",
                'imgSrc' : '/assets/was_good.png'
                # 'imgSrc': was_good_img
                    
            }, {
                'id': 6,
                'name': "Okay",
                'imgSrc' : '/assets/was_okay.png'
                # 'imgSrc': was_ok_img
                },
                {
                'id': 7,
                'name': "Bad",
                'imgSrc' : '/assets/was_bad.png'
                # 'imgSrc': was_bad_img
            }]
        ,
                'theme' : THEME,
                'title_size' : UI_TITLE_SIZE.LARGE,
                'custom_style' : {'title' : {'font-size' : '80px'},
                        'subtitle' : {'font-size' : '50px'},
                            "selector": {"background-color": "white",
                                        "border-width": "4px",
                                        "border-color": "#0686D8"
                                    },
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}}
                        
    }

UI_USER_VERIFY_2 ={
                'title':'',
                'show_back_button':False,
                'data':[{
                'id': USER_VERIFY['True'],
                'name': 'Yes',
                'imgSrc' : '/assets/UI_TRUE.png'
                # 'imgSrc': true_img
                    
            }, 
                {
                'id': USER_VERIFY['False'],
                'name': 'No',
                'imgSrc' : '/assets/UI_FALSE.jpeg'
                # 'imgSrc': false_img
            }]
        ,
                'theme' : THEME,
                'title_size' : UI_TITLE_SIZE.LARGE,
                'custom_style' : {'title' : {'font-size' : '100px'},
                        'subtitle' : {'font-size' : '70px'},
                            "selector": {"background-color": "white",
                                        "border-width": "4px",
                                        "border-color": "#0686D8"
                                    },
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}}
                
            
        }

#  User verification screen step 1
UI_USER_VERIFY_1 = {
    #'title' : 'שלום, האם השם הוא משה?',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : THEME,
    'custom_style' : CUSTOM_STYLE
    }


UI_REQUEST_FLEET_HELP = {
    'title' : 'Waiting for the operator to clear the way',
    'submit_text' : 'Continue',
    'cancel_text' : 'Go Home',
    'wait' : True
}

SCREENS_ENGLISH = {'UI_NAVIGATING_TO_HOME' : UI_NAVIGATING_TO_HOME,
                    'UI_SCREEN_END' : UI_SCREEN_END,
                    'UI_NAVIGATING_TO_INITIAL_POSITION' : UI_NAVIGATING_TO_INITIAL_POSITION,
                    'UI_GOOD_DAY' : UI_GOOD_DAY,
                    'UI_DANIEL_IS_A_MEME' : UI_DANIEL_IS_A_MEME,
                    'UI_SESSION' : UI_SESSION,
                    'UI_BEGIN' : UI_BEGIN,
                    'UI_STOP' : UI_STOP,
                    'UI_CONTINUE_VIDEOS' : UI_CONTINUE_VIDEOS,
                    'UI_CONTINUE_EXERCISE' : UI_CONTINUE_EXERCISE,
                    'UI_END_OF_SESSION' : UI_END_OF_SESSION,
                    'UI_OPEN_VIDEO' : UI_OPEN_VIDEO,
                    'UI_CONGRATS' : UI_CONGRATS,
                    'UI_SIT_STRAIGHT' : UI_SIT_STRAIGHT,
                    'UI_LEGS_ON_FLOOR' : UI_LEGS_ON_FLOOR,
                    'UI_STRAIGHT_HEAD' : UI_STRAIGHT_HEAD,
                    'UI_NO_TIME_FOR_CAUTION' : UI_NO_TIME_FOR_CAUTION,
                    'UI_SESSION_EMPHASES' : UI_SESSION_EMPHASES,
                    'UI_TAKE_STICK' : UI_TAKE_STICK,
                    'UI_RETURN_STICK' : UI_RETURN_STICK,
                    'UI_GUIDELINES' : UI_GUIDELINES,
                    'UI_STOP_CONDITION' : UI_STOP_CONDITION,
                    'UI_ARRIVING' : UI_ARRIVING,
                    'UI_INTRODUCTION' : UI_INTRODUCTION,
                    'UI_BELINSON' : UI_BELINSON,
                    'UI_GERIATRIC' : UI_GERIATRIC,
                    'UI_ACTIVITIES' : UI_ACTIVITIES,
                    'UI_SCREEN' : UI_SCREEN,
                    'UI_APPROACHING' : UI_APPROACHING,
                    'UI_PICK_WAND_OR_FINGER' : UI_PICK_WAND_OR_FINGER,
                    'UI_SELECT_WAND_OR_FINGER' : UI_SELECT_WAND_OR_FINGER,
                    'UI_SESSION_SCREEN' : UI_SESSION_SCREEN,
                    'UI_TREATMENT_STOPPED_SCREEN' : UI_TREATMENT_STOPPED_SCREEN,
                    'UI_STOP_TREATMENT' : UI_STOP_TREATMENT,
                    'UI_CHEST_BUTTON_INTRODUCTION' : UI_CHEST_BUTTON_INTRODUCTION,
                    'UI_CHEST_BUTTON_STOP_TRIGGER' : UI_CHEST_BUTTON_STOP_TRIGGER,
                    'UI_FEEDBACK_END_TREATMENT' : UI_FEEDBACK_END_TREATMENT,
                    'UI_USER_VERIFY_2' : UI_USER_VERIFY_2,
                    'UI_USER_VERIFY_1' : UI_USER_VERIFY_1,
                    'UI_REQUEST_FLEET_HELP' : UI_REQUEST_FLEET_HELP
                }