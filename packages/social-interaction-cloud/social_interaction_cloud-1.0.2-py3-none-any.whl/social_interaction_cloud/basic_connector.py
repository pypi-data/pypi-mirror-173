from enum import Enum
from functools import partial
from threading import Condition, Event, Thread
from time import sleep

from social_interaction_cloud.abstract_connector import AbstractSICConnector


class RobotPosture(Enum):
    STAND = 'Stand'
    STANDINIT = 'StandInit'
    STANDZERO = 'StandZero'
    CROUCH = 'Crouch'
    SIT = 'Sit'  # only for Nao
    SITONCHAIR = 'SitOnChair'  # only for Nao
    SITRELAX = 'SitRelax'  # only for Nao
    LYINGBELLY = 'LyingBelly'  # only for Nao
    LYINGBACK = 'LyingBack'  # only for Nao
    UNKNOWN = 'Unknown'  # this is not a valid posture


class VisionType(Enum):
    FACE = 'onFaceRecognized'
    PEOPLE = 'onPersonDetected'
    EMOTION = 'onEmotionDetected'
    CORONA = 'onCoronaCheckPassed'
    OBJECT = 'onObjectDetected'
    DEPTH = 'onDepthEstimated'
    TRACKING = 'onObjectTracked'

    def as_service(self):
        if self == VisionType.FACE:
            return 'face_recognition'
        elif self == VisionType.PEOPLE:
            return 'people_detection'
        elif self == VisionType.EMOTION:
            return 'emotion_detection'
        elif self == VisionType.CORONA:
            return 'corona_checker'
        elif self == VisionType.OBJECT:
            return 'object_detection'
        elif self == VisionType.DEPTH:
            return 'depth_estimation'
        elif self == VisionType.TRACKING:
            return 'object_tracking'


class NoCallbackException(Exception):
    pass


class Action:
    """
    Encapsulation class for BasicSICConnector method calls.

    The BasicSICConnector method call is executed when the perform() method is called. To create a waiting action,
    a threading.Event() object should be provided as lock.
    """

    def __init__(self, action: callable, *args, lock: Event = None):
        """

        :param action: a callable from the BasicSICConnector
        :param args: optional input arguments for the callable
        :param lock: optional lock to create a waiting Action.
        """
        self.action = action
        self.args = args
        self.lock = lock

    def perform(self) -> Event:
        """
        Calls the action callable.
        :return: the lock
        """
        self.action(*self.args)
        return self.lock


class BasicSICConnector(AbstractSICConnector):
    """
    Basic implementation of AbstractSICConnector. It serves a connector to the Social Interaction Cloud.
    The base mechanism is that a callback function can be registered for each robot action. When the action returns a
    result (e.g. a ActionDone event) the callback is called once and removed. Only for touch and vision events a
    persistent callback can be registered.

    """

    def __init__(self, server_ip: str, dialogflow_language: str = None,
                 dialogflow_key_file: str = None, dialogflow_agent_id: str = None, tts_key_file: str = None,
                 tts_voice: str = None, sentiment: bool = False, stereo_camera: bool = False):
        """
        :param server_ip: IP address of Social Interaction Cloud server
        :param dialogflow_language: the full language key to use in Dialogflow (e.g. en-US)
        :param dialogflow_key_file: path to Google's Dialogflow key file (JSON)
        :param dialogflow_agent_id: ID number of Dialogflow agent to be used (project ID)
        :param tts_language: the full language key to use in TTS (e.g. en-US)
        :param tts_key_file: path to Google's TTS key file (JSON)
        :param tts_voice: ID number of TTS voice to be used
        :param stereo_camera: use of stereo_camera
        """
        self.__action_listeners = {}
        self.__vision_listeners = {}
        self.__event_listeners = {}
        self.__conditions = []
        self.__loaded_actions = []
        self.robot_state = {'posture': RobotPosture.UNKNOWN,
                            'is_awake': False,
                            'battery_charge': 100,
                            'is_charging': False,
                            'hot_devices': []}
        self.stereo_camera = stereo_camera

        super(BasicSICConnector, self).__init__(server_ip=server_ip)

        if sentiment:
            self.enable_service('sentiment_analysis')
        self.sentiment_enabled = sentiment
        
        if dialogflow_language and dialogflow_key_file and dialogflow_agent_id:
            self.enable_service('intent_detection')
            sleep(1)  # give the service some time to load
            self.set_dialogflow_language(dialogflow_language)
            self.set_dialogflow_key(dialogflow_key_file)
            self.set_dialogflow_agent(dialogflow_agent_id)

        if tts_voice:
            self.enable_service('text_to_speech')
            sleep(1)

            if not tts_key_file:
                tts_key_file = dialogflow_key_file

            self.set_tts_key(tts_key_file)
            self.set_tts_voice(tts_voice)

    ###########################
    # Event handlers          #
    ###########################

    def on_event(self, event: str) -> None:
        self.__notify_action_listeners(event)
        self.__notify_event_listeners(event)

    def on_posture_changed(self, posture: str) -> None:
        self.__notify_action_listeners('onPostureChanged', posture)
        self.robot_state['posture'] = RobotPosture[posture.upper()]

    def on_awake_changed(self, is_awake: bool) -> None:
        self.__notify_action_listeners('onAwakeChanged', is_awake)
        self.robot_state['is_awake'] = is_awake

    def on_audio_language(self, language_key: str) -> None:
        self.__notify_action_listeners('onAudioLanguage', language_key)

    def on_audio_intent(self, detection_result: dict) -> None:
        self.__notify_action_listeners('onAudioIntent', detection_result)

    def on_text_transcript(self, transcript: str) -> None:
        self.__notify_action_listeners('onTextTranscript', transcript)

    def on_text_sentiment(self, sentiment: str) -> None:
        self.__notify_action_listeners('onTextSentiment', sentiment)

    def on_new_audio_file(self, audio_file: str) -> None:
        self.__notify_action_listeners('onNewAudioFile', audio_file)

    def on_new_picture_file(self, picture_file: str) -> None:
        self.__notify_action_listeners('onNewPictureFile', picture_file)

    def on_person_detected(self, x: int, y: int) -> None:
        self.__notify_vision_listeners('onPersonDetected', x, y)

    def on_face_recognized(self, identifier: str) -> None:
        self.__notify_vision_listeners('onFaceRecognized', identifier)

    def on_emotion_detected(self, emotion: str) -> None:
        self.__notify_vision_listeners('onEmotionDetected', emotion)

    def on_corona_check_passed(self) -> None:
        self.__notify_vision_listeners('onCoronaCheckPassed')

    def on_object_detected(self, centroid_x: int, centroid_y: int) -> None:
        self.__notify_vision_listeners('onObjectDetected', centroid_x, centroid_y)

    def on_depth_estimated(self, estimation: int, std_dev: int) -> None:
        self.__notify_vision_listeners('onDepthEstimated', estimation, std_dev)

    def on_object_tracked(self, obj_id: int, distance_cm: int, centroid_x: int, centroid_y: int, in_frame_ms: int,
                          speed_cmps: int) -> None:
        self.__notify_vision_listeners('onObjectTracked', obj_id, distance_cm, centroid_x, centroid_y, in_frame_ms,
                                       speed_cmps)

    def on_battery_charge_changed(self, percentage: int) -> None:
        self.__notify_action_listeners('onBatteryChargeChanged', percentage)
        self.robot_state['battery_charge'] = percentage

    def on_charging_changed(self, is_charging: bool) -> None:
        self.__notify_action_listeners('onChargingChanged', is_charging)
        self.robot_state['is_charging'] = is_charging

    def on_hot_device_detected(self, hot_devices: list) -> None:
        self.__notify_action_listeners('onHotDeviceDetected', hot_devices)
        self.robot_state['hot_devices'] = hot_devices

    def on_robot_motion_recording(self, motion: str) -> None:
        self.__notify_action_listeners('onRobotMotionRecording', motion)

    def on_browser_button(self, button: str) -> None:
        self.__notify_action_listeners('onBrowserButton', button)

    ###########################
    # Speech Recognition      #
    ###########################

    def speech_recognition(self, context: str, max_duration: int, callback: callable = None,
                           sentiment_callback: callable = None, sync: bool = True) -> None:
        """
        Initiate a speech recognition attempt using Google's Dialogflow using a context.
        For more information on contexts see: https://cloud.google.com/dialogflow/docs/contexts-overview

        The robot will stream audio for at most max_duraction seconds to Dialogflow to recognize something.
        The result (or a 'fail') is returned via the callback function.

        :param context: Google's Dialogflow context label (str)
        :param max_duration: maximum time to listen in seconds (int)
        :param callback: callback function that will be called when a result (or fail) becomes available
        :param sync: lets main thread wait on this action
        :return:
        """
        inner_callback = callback
        lock = None
        if sync:
            inner_callback, lock = self.__build_sync_callback(inner_callback)

        enhanced_callback, fail_callback, listen_lock = self.__build_speech_recording_callback(inner_callback)
        self.__register_action_listener('onAudioIntent', enhanced_callback)
        self.__register_action_listener('IntentDetectionDone', fail_callback)

        if self.sentiment_enabled and sentiment_callback:
            self.__register_action_listener('onTextSentiment', sentiment_callback)

        Thread(target=self.__recognizing, args=(context, listen_lock, max_duration)).start()

        if lock:
            lock.wait()

    def record_audio(self, duration: int, callback: callable = None, sync: bool = True) -> None:
        """
        Records audio for a number of duration seconds. The location of the audio is returned via the callback function.

        :param duration: number of second of audio that will be recorded.
        :param callback: callback function that will be called when the audio is recorded.
        :param sync: lets main thread wait on this action
        :return:
        """
        inner_callback = callback
        lock = None
        if sync:
            inner_callback, lock = self.__build_sync_callback(inner_callback)

        success_callback, _, listen_lock = self.__build_speech_recording_callback(callback)
        self.__register_action_listener('onNewAudioFile', success_callback)
        Thread(target=self.__recording, args=(listen_lock, duration)).start()

        if lock:
            lock.wait()

    def __recognizing(self, context: str, lock: Event, max_duration: int) -> None:
        self.stop_listening()
        self.set_dialogflow_context(context)
        self.start_listening(max_duration)
        lock.wait()
        self.__unregister_action_listener('onAudioIntent')
        self.__unregister_action_listener('IntentDetectionDone')

    def __recording(self, lock: Event, max_duration: int) -> None:
        self.stop_listening()
        self.set_record_audio(True)
        self.start_listening(max_duration)
        lock.wait()
        self.set_record_audio(False)
        self.__unregister_action_listener('onNewAudioFile')

    @staticmethod
    def __build_speech_recording_callback(embedded_callback: callable = None):
        lock = Event()

        def success_callback(*args):
            lock.set()
            if embedded_callback:
                embedded_callback(*args)

        def fail_callback():
            if not lock.is_set():
                lock.set()
                if embedded_callback:
                    embedded_callback(None)

        return success_callback, fail_callback, lock

    ###########################
    # Vision                  #
    ###########################

    def take_picture(self, callback: callable = None, sync: bool = True, chain: bool = False) -> None:
        """
        Take a picture. Location of the stored picture is returned via callback.

        :param callback:
        :param sync:
        :param chain:
        :return:
        """
        self.__process_action(super(BasicSICConnector, self).take_picture,
                              callback=callback, event='onNewPictureFile', sync=sync, chain=chain)

    def subscribe_vision_listener(self, vision_type: VisionType, callback: callable = None, continuous: bool = False,
                                  sync: bool = True, chain: bool = False) -> None:
        # not continuous stops after one hit, continuous continues
        # synch wait until (first) hit
        # chain wait until any or all (first) hit
        inner_callback = callback
        lock = None

        if not continuous:
            inner_callback = self.__build_vision_stopping_callback(vision_type, inner_callback)

        if sync:
            inner_callback, lock = self.__build_sync_callback(inner_callback)

        if not inner_callback:
            raise NoCallbackException('A vision listener requires a callback')

        if chain:
            self.enable_service(vision_type.as_service())
            sleep(1)  # give the service some time to load
            self.__loaded_actions.append(Action(self.__start_vision_recognition, str(vision_type.value), inner_callback,
                                         continuous, lock=lock))
        else:
            self.enable_service(vision_type.as_service())
            sleep(1)  # give the service some time to load
            self.__start_vision_recognition(str(vision_type.value), inner_callback, continuous)
            if lock:
                lock.wait()

    def unsubscribe_vision_listener(self, vision_type: VisionType):
        self.__stop_vision_recognition(str(vision_type.value))

    def __build_vision_stopping_callback(self, vision_type: VisionType, original_callback: callable = None):
        """
        Builds callback function for a single use vision listener.

        :param vision_type:
        :param original_callback:
        :return:
        """
        def callback(*args):
            if original_callback:
                original_callback(*args)
            self.__stop_vision_recognition(str(vision_type.value))

        return callback

    def __start_vision_recognition(self, event: str, callback: callable = None, continuous: bool = False) -> None:
        had_listeners = len(self.__vision_listeners) > 0
        self.__register_vision_listener(event, callback)
        if not had_listeners and not continuous:
            self.stop_looking()
            self.start_looking(seconds=0, channels=(2 if self.stereo_camera else 1))

    def __stop_vision_recognition(self, event: str) -> None:
        self.__unregister_vision_listener(event)
        if not self.__vision_listeners:
            self.stop_looking()

    ###########################
    # Event Listeners         #
    ###########################

    def subscribe_event_listener(self, event: str, callback: callable, continuous: bool = False,
                                 sync: bool = True, chain: bool = False) -> None:
        """
        Subscribe an event listener. The callback function will be called each time the event becomes available.

        :param event:
        :param callback:
        :return:
        """
        # not continuous stops after one hit, continuous continues
        # synch wait until (first) hit
        # chain wait until any or all (first) hit
        inner_callback = callback
        lock = None

        if not continuous:
            inner_callback = self.__build_event_stopping_callback(event, inner_callback)

        if sync:
            inner_callback, lock = self.__build_sync_callback(inner_callback)

        if not inner_callback:
            raise NoCallbackException('An event listener requires a callback')

        if chain:
            self.__loaded_actions.append(Action(self.__register_event_listener, event, inner_callback, lock=lock))
        else:
            self.__register_event_listener(event, inner_callback)
            if lock:
                lock.wait()

    def unsubscribe_event_listener(self, event: str) -> None:
        """
        Unsubscribe touch listener.

        :param event:
        :return:
        """
        self.__unregister_event_listener(event)

    def __build_event_stopping_callback(self, event, original_callback):
        def callback(*args):
            if original_callback:
                original_callback(*args)
            self.unsubscribe_event_listener(event)

        return callback

    ###########################
    # Robot actions           #
    ###########################

    def say_text_to_speech(self, text: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).say_text_to_speech, text,
                              callback=callback, event='PlayAudioDone', sync=sync, chain=chain)

    def set_language(self, language_key: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_language, language_key,
                              callback=callback, event='LanguageChanged', sync=sync, chain=chain)

    def set_idle(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_idle,
                              callback=callback, event='SetIdle', sync=sync, chain=chain)

    def set_non_idle(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_non_idle,
                              callback=callback, event='SetNonIdle', sync=sync, chain=chain)

    def start_looking(self, seconds: int, channels: int = 1, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).start_looking, seconds, channels,
                              callback=callback, event='WatchingStarted', sync=sync, chain=chain)

    def stop_looking(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).stop_looking,
                              callback=callback, event='WatchingDone', sync=sync, chain=chain)

    def say(self, text: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).say, text,
                              callback=callback, event='TextDone', sync=sync, chain=chain)

    def say_animated(self, text: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).say_animated, text,
                              callback=callback, event='TextDone', sync=sync, chain=chain)

    def stop_talking(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).stop_talking,
                              callback=callback, event='TextDone', sync=sync, chain=chain)

    def do_gesture(self, gesture: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).do_gesture, gesture,
                              callback=callback, event='GestureDone', sync=sync, chain=chain)

    def load_audio(self, audio_file: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).load_audio, audio_file,
                              callback=callback, event='LoadAudioDone', sync=sync, chain=chain)

    def play_audio(self, audio_file: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).play_audio, audio_file,
                              callback=callback, event='PlayAudioDone', sync=sync, chain=chain)

    def play_loaded_audio(self, audio_identifier: int, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).play_loaded_audio, audio_identifier,
                              callback=callback, event='PlayAudioDone', sync=sync, chain=chain)

    def clear_loaded_audio(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).clear_loaded_audio,
                              callback=callback, event='ClearLoadedAudioDone', sync=sync, chain=chain)

    def set_eye_color(self, color: str, callback: callable = None, sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_eye_color, color,
                              callback=callback, event='EyeColourDone', sync=sync, chain=chain)

    def set_ear_color(self, color: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_ear_color, color,
                              callback=callback, event='EarColourDone', sync=sync, chain=chain)

    def set_head_color(self, color: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_head_color, color,
                              callback=callback, event='HeadColourDone', sync=sync, chain=chain)

    def set_led_color(self, leds: list, colors: list, duration: int = 0, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_led_color, leds, colors, duration,
                              callback=callback, event='LedColorDone', sync=sync, chain=chain)
    
    def start_led_animation(self, led_group: str, anim_type: str, colors: list, speed: int,
                            real_blink=False, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).start_led_animation, led_group, anim_type, colors, speed, real_blink,
                              callback=callback, event='LedAnimationDone', sync=sync, chain=chain)

    def stop_led_animation(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).stop_led_animation,
                              callback=None, event='', sync=sync, chain=chain)

    def turn(self, degrees: int, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).turn, degrees,
                              callback=callback, event='TurnDone', sync=sync, chain=chain)

    def wake_up(self, callback: callable = None, sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).wake_up,
                              callback=callback, event='WakeUpDone', sync=sync, chain=chain)

    def rest(self, callback: callable = None, sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).rest,
                              callback=callback, event='RestDone', sync=sync, chain=chain)

    def set_breathing(self, enable: bool, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_breathing, enable,
                              callback=callback, event='Breathing' + ('Enabled' if enable else 'Disabled'), sync=sync, chain=chain)

    def go_to_posture(self, posture: Enum, speed: int = 100, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        """
        The robot will try for 3 times to reach a position.
        go_to_posture's callback returns a bool indicating whether the given posture was successfully reached.
        """
        self.__process_action(super(BasicSICConnector, self).go_to_posture, posture.value, speed,
                              callback=partial(self.__posture_callback,
                                               target_posture=posture,
                                               embedded_callback=callback),
                              event='GoToPostureDone', sync=sync, chain=chain)

    def __posture_callback(self, target_posture: str, embedded_callback: callable) -> None:
        if self.robot_state['posture'] == target_posture:  # if posture was successfully reached
            embedded_callback(True)  # call the listener to signal a success
        else:  # if the posture was not reached
            embedded_callback(False)  # call the listener to signal a failure

    def set_stiffness(self, joints: list, stiffness: int, duration: int = 1000, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).set_stiffness, joints, stiffness, duration,
                              callback=callback, event='SetStiffnessDone', sync=sync, chain=chain)

    def play_motion(self, motion: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).play_motion, motion,
                              callback=callback, event='PlayMotionDone', sync=sync, chain=chain)

    def start_record_motion(self, joint_chains: list, framerate: int = 5, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).start_record_motion, joint_chains, framerate,
                              callback=callback, event='RecordMotionStarted', sync=sync, chain=chain)

    def stop_record_motion(self, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).stop_record_motion,
                              callback=callback, event='onRobotMotionRecording', sync=sync, chain=chain)

    def browser_show(self, html: str, callback: callable = None,  sync: bool = True, chain: bool = False) -> None:
        self.__process_action(super(BasicSICConnector, self).browser_show, html,
                              callback=None, event='', sync=sync, chain=chain)

    ###########################
    # Listeners Management  #
    ###########################
    def __register_action_listener(self, event: str, callback: callable) -> None:
        self.__action_listeners[event] = callback

    def __unregister_action_listener(self, event: str) -> None:
        del self.__action_listeners[event]

    def __register_vision_listener(self, event: str, callback: callable) -> None:
        self.__vision_listeners[event] = callback

    def __unregister_vision_listener(self, event: str) -> None:
        del self.__vision_listeners[event]

    def __register_event_listener(self, event: str, callback: callable):
        self.__event_listeners[event] = callback

    def __unregister_event_listener(self, event: str) -> None:
        del self.__event_listeners[event]

    def __register_condition(self, condition: Condition) -> None:
        """
        Subscribe a threading.Condition object that will be notified each time a registered callback is called.

        :param condition: Condition object that will be notified
        :return:
        """
        self.__conditions.append(condition)

    def __unregister_condition(self, condition: Condition) -> None:
        """
        Unsubscribe the threading.Condition object.

        :param condition: Condition object to unsubscribe
        :return:
        """
        if condition in self.__conditions:
            self.__conditions.remove(condition)

    def __notify_action_listeners(self, event: str, *args) -> None:
        if event in self.__action_listeners:
            listener = self.__action_listeners[event]
            listener(*args)
            self.__notify_conditions()

    def __notify_vision_listeners(self, event: str, *args) -> None:
        if event in self.__vision_listeners:
            listener = self.__vision_listeners[event]
            listener(*args)
            self.__notify_conditions()

    def __notify_event_listeners(self, event: str, *args) -> None:
        if event in self.__event_listeners:
            listener = self.__event_listeners[event]
            listener(*args)
            self.__notify_conditions()

    def __notify_conditions(self) -> None:
        for condition in self.__conditions:
            with condition:
                condition.notify()

    @staticmethod
    def __build_sync_callback(additional_callback: callable = None):
        """
        Builds a callback function that calls set() on an threading.Event() lock when trigger.
        This is the main mechanism behind a waiting Action.

        :param additional_callback: callback function to be embedded in the waiting callback
        :return: Callable callback, Event() lock
        """
        lock = Event()

        def callback(*args):
            if additional_callback:
                additional_callback(*args)
            lock.set()

        return callback, lock

    def __process_action(self, action: callable, *args, callback: callable, event: str, sync: bool, chain: bool):
        inner_callback = callback
        lock = None

        if sync:
            inner_callback, lock = self.__build_sync_callback(callback)

        if inner_callback:
            self.__register_action_listener(event, inner_callback)

        if chain:
            self.__loaded_actions.append(Action(action, *args, lock=lock))
        else:
            action(*args)
            if lock:
                lock.wait()

    def run_loaded_actions(self, wait_for_any=False):
        locks = []
        for action in self.__loaded_actions:
            lock = action.perform()
            if lock:
                locks.append(lock)

        if locks:
            condition = Condition()
            self.__register_condition(condition)
            with condition:
                if wait_for_any:
                    condition.wait_for(lambda: any([_lock.is_set() for _lock in locks]))
                else:
                    condition.wait_for(lambda: all([_lock.is_set() for _lock in locks]))
            self.__unregister_condition(condition)

        self.__loaded_actions = []

    ###########################
    # Management              #
    ###########################

    def start(self) -> None:
        self.__clear_listeners()
        super(BasicSICConnector, self).start()

    def stop(self) -> None:
        self.__clear_listeners()
        super(BasicSICConnector, self).stop()

    def __clear_listeners(self) -> None:
        self.__action_listeners = {}
        self.__conditions = []
        self.__vision_listeners = {}
        self.__event_listeners = {}
