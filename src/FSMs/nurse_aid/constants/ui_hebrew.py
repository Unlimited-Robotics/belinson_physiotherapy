from raya.enumerations import UI_ANIMATION_TYPE, UI_THEME_TYPE, UI_TITLE_SIZE
from src.FSMs.nurse_aid.constants.constants import *
from raya.tools.filesystem import open_file, resolve_path
import time

# General background
background_url = 'url(/assets/belinson_logo.png)'


# Current time
year = time.strftime('%Y')
month = time.strftime('%B')
month_numeric = time.strftime('%m')
month_day = time.strftime('%d')
week_day = time.strftime('%A')
hour = str(int(time.strftime('%I')) + 3)
minute = time.strftime('%M')


hebrew = {'January' : 'ינואר', 'February' : 'פברואר', 'March' : 'מרץ', 'April' : 'אפריל', 'May' : 'מאי',
        'June' : 'יוני', 'July' : 'יולי', 'August' : 'אוגוסט', 'September' : 'ספטמבר', 'October' : 'אוקטובר',
        'November' : 'נובמבר', 'December' : 'דצמבר',
        
        'Sunday' : 'ראשון', 'Monday' : 'שני', 'Tuesday' : 'שלישי', 'Wednesday' : 'רביעי', 'Thursday' : 'חמישי',
        'Friday' : 'שישי', 'Saturday' : 'שבת'}

CUSTOM_STYLE = {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                }

CUSTOM_STYLE_GAMES = {'title' : {'font-size' : '75px'},
                      'image' : {'height' : '80%',
                                 'width' : '80%',
                                 'maxHeight' : '525'},
                        'questions_size' : '60',
                      'pageTitle' : {'font-size' : '60px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                }


# SCREENS

UI_NAVIGATING_TO_HOME = {
        'title':'🏠 בדרכי הביתה', 
        'subtitle':'סיימתי את התרגול',
        'theme' : UI_THEME_TYPE.WHITE,
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
        'theme' : UI_THEME_TYPE.WHITE
    }


UI_NAVIGATING_TO_INITIAL_POSITION = {
        'title':'בדרכי להתחיל תרגול',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : '',
        'show_loader' : True,
        'back_button_text' : '',
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_GOOD_DAY = {
        'title' : f'יום {hebrew[week_day]}',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : f'חודש {hebrew[month]} והשנה היא {year}',
        'format' : UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://content.presentermedia.com/content/clipart/00003000/3878/magnify_desk_calendar_month_view_300_nwm.jpg',
        'content' : '/assets/UI_GOOD_DAY_2.gif',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_DANIEL_IS_A_MEME = {
        'title' : 'אם יש כאב, רצוי לעשות הפסקה',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format' : UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://media.giphy.com/media/nIYphcRREmvd7GHkHM/giphy.gif',
        'content' : '/assets/UI_DANIEL_IS_A_MEME_2.gif',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_SESSION = {
        'title' : "אורך התרגול היום יהיה כ-30 דקות",
        'title_size' : UI_TITLE_SIZE.LARGE,
        'subtitle' : 'כולל תרגול קוגנטיבי וצפייה בסרטונים',
        'show_loader' : False,
        'back_button_text' : '',
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_BEGIN = {
    'title' : '',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : '',
    'button_text' : 'התחל',
    'back_button_text' : '',
    'button_size' : 'LARGE',
    'wait' : False,
    'theme' : UI_THEME_TYPE.WHITE,
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
    'button_text' : 'עצור',
    'back_button_text' : '',
    'button_size' : 'LARGE',
    'wait' : False,
    'theme' : UI_THEME_TYPE.WHITE,
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
    'title' : 'לחץ על הכפתור כדי להתחיל',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'סרטון למידה',
    'button_text' : 'התחל תרגול',
    'back_button_text' : '',
    'wait' : False,
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_CONTINUE_EXERCISE = {
    'title' : 'לחץ על הכפתור כדי להתחיל',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'תרגול קוגנטיבי',
    'button_text' : 'התחל תרגול',
    'back_button_text' : '',
    'wait' : False,
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_END_OF_SESSION = {
    'title' : "התרגול הסתיים בהצלחה",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'המשך יום נעים',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_OPEN_VIDEO = {
    'title' : '',
    'url' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'back_button_text' : '',
    'width' : '85%',
    'height' : '75%',
    'close_after_finished' : True,
    'wait' : False,
    'custom_style' : CUSTOM_STYLE
    }


UI_CONGRATS = {
    'title' : "!כל הכבוד",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'החלק הנוכחי הסתיים בהצלחה',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_SIT_STRAIGHT = {
    'title' : 'יש לשמור על ישיבה זקופה',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://businessmirror.com.ph/wp-content/uploads/2019/06/hf02-062719.jpg',
    'content' : '/assets/UI_SIT_STRAIGHT.jpg',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_LEGS_ON_FLOOR = {
    'title' : 'כפות הרגליים מונחות על הרצפה',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media.giphy.com/media/H897EyN4b6WseXBBCq/giphy.gif',
    'content' : '/assets/UI_LEGS_ON_FLOOR.gif',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_STRAIGHT_HEAD = {
    'title' : 'ראש ישר, בהמשך לעמוד השדרה',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://blog.kakaocdn.net/dn/OA1Rg/btqGd1TrMh6/ushfpBvqnRU4rCk92HKIXk/img.png',
    'content' : '/assets/UI_STRAIGHT_HEAD.png',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_NO_TIME_FOR_CAUTION = {
    'title' : 'יש לבצע את התרגילים באיטיות ובזהירות',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://www.seekpng.com/png/detail/779-7794349_stop-bot-cartoon-stop-sign-with-transparent-background.png',
    'content' : '/assets/UI_NO_TIME_FOR_CAUTION.jpeg',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_SESSION_EMPHASES = {
    'title' : 'דגשים לתרגול',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://www.rotary-ribi.org/upimages/PageMainPics/EARS.jpg',
    'content' : '/assets/UI_SIT_STRAIGHT.jpg',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_TAKE_STICK = {
    'title' : 'אנא קח את המקל מימינך',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media0.giphy.com/media/MZXmFVrbMA1qSDNGOt/giphy.gif?cid=ecf05e47k0o5qi0r21x53t5kgtvfjsab7qx8q88pikd9lbb1&rid=giphy.gif&ct=s',
    'content' : '/assets/UI_TAKE_STICK.gif',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
}


UI_RETURN_STICK = {
    'title' : 'נא החזר את מקל האחיזה',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://media0.giphy.com/media/MZXmFVrbMA1qSDNGOt/giphy.gif?cid=ecf05e47k0o5qi0r21x53t5kgtvfjsab7qx8q88pikd9lbb1&rid=giphy.gif&ct=s',
    'content' : '/assets/UI_TAKE_STICK.gif',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_GUIDELINES = {
    'title' : 'הוראות בטיחות',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    # 'content' : 'https://www.rotary-ribi.org/upimages/PageMainPics/EARS.jpg',
    'content' : '/assets/UI_GUIDELINES.jpg',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }



UI_STOP_CONDITION = {
    'title' : '!כפתור חירום',
    'title_size' : UI_TITLE_SIZE.MEDIUM,
    # 'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    'show_loader' : False,
    # 'content' : '/assets/UI_STOP_CONDITION.gif',
    'theme' : UI_THEME_TYPE.WHITE,
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
        'title' : 'אני כבר מגיע',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'subtitle' : 'אנא לשבת זקוף',
        'back_button_text' : '',
        # 'content' : 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=360/uploads/users/1112/posts/25730/final_image/animate-run-progress-04.gif',
        'content' : '/assets/UI_ARRIVING.gif',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_INTRODUCTION = {
        'title' : 'שלום! אני בילי הרובוט',
        'title_size' : UI_TITLE_SIZE.MEDIUM,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://i.postimg.cc/DwSCXBNx/f415e2-7d7e99622ef14504b66e6d560b34c34ef000.webp',
        'content' : '/assets/gary_the_robot.png',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
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
    'title' : 'התחלת פעילות',
    'title_size' : UI_TITLE_SIZE.MEDIUM,
    'format' : UI_ANIMATION_TYPE.URL,
    'back_button_text' : '',
    'content' : '/assets/UI_BEFORE_ACTIVITIES.jpg',
    'show_loader' : False,
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : {'title' : {'font-size' : '130px'},
                        'subtitle' : {'font-size' : '60px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '900px',
                                    'height' : '700px'}
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
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : {'title' : {'font-size' : '150px'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'},
                        'image' : {'width' : '1000px',
                                    'height' : '800px'}
                        }
    }


UI_GERIATRIC = {
        'title' : 'אנחנו נמצאים במחלקה הגריאטרית',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://media.giphy.com/media/zOU33C79GYLcyg6dWI/giphy.gif',
        'content' : '/assets/UI_GERIATRIC.gif',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


# UI_ACTIVITIES = {
#         'title' : 'נעשה היום ביחד פעילויות',
#         #'subtitle' : 'המרפאה לריפוי בעיסוק',
#         'title_size' : UI_TITLE_SIZE.MEDIUM,
#         'format': UI_ANIMATION_TYPE.URL,
#         'back_button_text' : '',
#         # 'content' : 'https://media.giphy.com/media/JTbtvgjLN4w9jXmsS4/giphy.gif',
#         # 'content' : '/assets/UI_ACTIVITIES.gif',
#         'content' : '',
#         'show_loader' : False,
#         'theme' : UI_THEME_TYPE.WHITE,
#         'custom_style' : {'title' : {'font-size' : '130px'},
#                         'subtitle' : {'font-size' : '60px'},
#                         'background' : {'background' : background_url,
#                                         'backgroundRepeat' : 'no-repeat',
#                                         'backgroundSize' : 'cover'},

#                         'image' : {'width' : '300px',
#                                     'height' : '500px'}
                        
#                         }
#     }

UI_ACTIVITIES = {
        'title' : 'נעשה ביחד מספר פעילויות',
        'show_loader' : False,
        'back_button_text' : '',
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
        }  


UI_SCREEN = {
    'title' : 'לחץ על הכפתור במסך כדי להשתמש בי',
    'title_size' : UI_TITLE_SIZE.LARGE,
    'button_text' : 'לחץ כאן',
    'back_button_text' : '',
    'wait' : False,
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


UI_APPROACHING= {
        'title' : 'אני מתקדם באיטיות ובזהירות',
        'title_size' : UI_TITLE_SIZE.LARGE,
        'format': UI_ANIMATION_TYPE.URL,
        'back_button_text' : '',
        # 'content' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQUzamS1hiJugJpXan0pKd1UAi3E-vmFnhQQ&usqp=CAU',
        'content' : '/assets/UI_APPROACHING.png',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }


UI_PICK_WAND_OR_FINGER = {
    'title' : "כיצד תבצע את הבחירות על המסך? ",
    'title_size' : UI_TITLE_SIZE.LARGE,
    'subtitle' : 'אנא לחץ על בחירתך, בעזרת מקל אחיזה או אצבע',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : {'title' : {'font-size' : '70'},
                        'subtitle' : {'font-size' : '70px'},
                        'background' : {'background' : background_url,
                                        'backgroundRepeat' : 'no-repeat',
                                        'backgroundSize' : 'cover'}
                        }
    }


UI_SELECT_WAND_OR_FINGER = {
                'title':'?כיצד תבצע את הבחירות על המסך',
                'show_back_button':False,
                'data':[{
                'id': TOUCH_ITEM['Wand'],
                'name': 'מקל',
                'imgSrc' : '/assets/UI_STICK.png'
                # 'imgSrc':"https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Fi.postimg.cc%2FZY1GGrH7%2Fimage-134.png"
                    
            }, {
                'id': TOUCH_ITEM['Hand'],
                'name': 'אצבע',
                'imgSrc' : '/assets/UI_HAND.jpeg'
                # 'imgSrc':"https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F158222770%2Fphoto%2Ftouch-controlled-white-virtual-screen.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3DDqO5KDPGUoddvcQdSGIQdIMLhFuD-cjyy-oFl4K6cvM%3D"
            }]
        ,
                'theme' : UI_THEME_TYPE.WHITE,
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
        # 'title' : f"אורך התרגול היום יהיה כ-{int(self.treatment_time)} דקות",
        #'subtitle' : 'כולל תרגול קוגנטיבי, צפייה בסרטונים, ותרגילי גפה',
        'show_loader' : False,
        'back_button_text' : '',
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
        }   


UI_TREATMENT_STOPPED_SCREEN = {
    'title' : 'התרגול הופסק על ידי הצוות',
    'subtitle' : 'המשך יום נעים',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


# Stop the treatment (by user)
UI_STOP_TREATMENT = {
                'title':'?מדוע תרצה/י להפסיק את התרגול',
                'show_back_button':False,
                'data':[{
                'id': EXIT_OPTION['Other'],
                'name': 'אחר',
                'imgSrc' : '/assets/UI_OTHER.png'
                # 'imgSrc': stop_treatment_other_img
                },
                
                {'id': EXIT_OPTION['Sick'],
                'name': 'לא מרגיש טוב',
                'imgSrc' : '/assets/UI_SICK.png'
                # 'imgSrc': stop_treatment_sick_img
                },
                
                {'id': EXIT_OPTION['Regret'],
                'name': 'התחרטתי- לחזור ',
                'imgSrc' : '/assets/UI_REGRET.png'
                # 'imgSrc': stop_treatment_regret_img
                }
                ],

                'theme' : UI_THEME_TYPE.WHITE,
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
        'title' : 'להפסקת התרגול בכל שלב',
        'title_size' : UI_TITLE_SIZE.MEDIUM,
        'format': UI_ANIMATION_TYPE.URL,
        'subtitle' : '',
        'back_button_text' : '',
        # 'content' : "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWZoczVxZGI4ZzFvbnJpZ3Q1emhoNm1qd2UyOXhwZDBqbG9sMno1ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1z/9PekRRQ0WlrRVwynAk/200w.gif",
        'content' : '/assets/UI_STOP_CONDITION.gif',
        'show_loader' : False,
        'theme' : UI_THEME_TYPE.WHITE,
        'custom_style' : CUSTOM_STYLE
    }               
    


# Chest button trigger to stop the app
UI_CHEST_BUTTON_STOP_TRIGGER ={
    'title' : "!התרגול הסתיים",
    'subtitle' : 'המשך יום נעים',
    'show_loader' : False,
    'back_button_text' : '',
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }


# Feedback screen
UI_FEEDBACK_END_TREATMENT={
                'title':'?איך היה התרגול',
                'show_back_button':False,
                'data':[{
                'id': 5,
                'name': 'נהנתי מאוד',
                'imgSrc' : '/assets/was_good.png'
                # 'imgSrc': was_good_img
                    
            }, {
                'id': 6,
                'name': 'היה בסדר',
                'imgSrc' : '/assets/was_okay.png'
                },
                {
                'id': 7,
                'name': 'לא נהנתי  ',
                'imgSrc' : '/assets/was_bad.png'
            }]
        ,
                'theme' : UI_THEME_TYPE.WHITE,
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


# User verification screen step 2
UI_USER_VERIFY_2 ={
                'title':'',
                'show_back_button':False,
                'data':[{
                'id': USER_VERIFY['True'],
                'name': 'כן',
                'imgSrc' : '/assets/UI_TRUE.png'
                # 'imgSrc': true_img
                    
            }, 
                {
                'id': USER_VERIFY['False'],
                'name': 'לא',
                'imgSrc' : '/assets/UI_FALSE.jpeg'
                # 'imgSrc': false_img
            }]
        ,
                'theme' : UI_THEME_TYPE.WHITE,
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
    'theme' : UI_THEME_TYPE.WHITE,
    'custom_style' : CUSTOM_STYLE
    }

UI_REQUEST_FLEET_HELP = {
    'title' : 'מחכה לאופרטור שיפנה לי את הדרך',
    'submit_text' : 'המשך במשימה',
    'cancel_text' : 'חזור הביתה',
    'wait' : True
}

SCREENS_HEBREW = {'UI_NAVIGATING_TO_HOME' : UI_NAVIGATING_TO_HOME,
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