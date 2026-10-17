import sys
import threading
import queue
import time
import pyttsx3

# SAPI SpeechVoiceSpeakFlags
SVSF_ASYNC = 1
SVSF_PURGE_BEFORE_SPEAK = 2


class TTSEngine:
	"""Threaded TTS engine that only speaks the latest message; urgent ones cut off the current sentence."""

	def __init__(self, rate: int = 180, volume: float = 1.0, voice_index: int | None = None):
		self._settings = (rate, volume, voice_index)
		self._queue: "queue.Queue[tuple[str, bool]]" = queue.Queue()
		self._thread = threading.Thread(target=self._worker, daemon=True)
		self._voice = None
		self._ready = threading.Event()
		self._running = True
		self._thread.start()
		self._ready.wait(timeout=5.0)

	def _init_engine(self) -> None:
		# The engine must be created on the thread that runs it: SAPI5 hangs in runAndWait otherwise
		rate, volume, voice_index = self._settings
		self._engine = pyttsx3.init()
		self._engine.setProperty("rate", rate)
		self._engine.setProperty("volume", volume)
		if voice_index is not None:
			voices = self._engine.getProperty("voices")
			if 0 <= voice_index < len(voices):
				self._engine.setProperty("voice", voices[voice_index].id)
		if sys.platform == "win32":
			# pyttsx3 can't reliably cut off a sentence, but its underlying SAPI voice can
			self._voice = self._engine.proxy._driver._tts

	def _worker(self) -> None:
		try:
			self._init_engine()
		finally:
			self._ready.set()
		while self._running:
			try:
				text, interrupt = self._queue.get(timeout=0.1)
			except queue.Empty:
				continue
			if not text:
				continue
			try:
				if self._voice is None:
					self._engine.say(text)
					self._engine.runAndWait()
					continue
				# Let the current sentence finish, unless this one is urgent or a newer one arrives
				while not interrupt and self._running and self._queue.empty() and not self._voice.WaitUntilDone(50):
					pass
				if not interrupt and not self._queue.empty():
					continue
				self._voice.Speak(text, SVSF_ASYNC | SVSF_PURGE_BEFORE_SPEAK)
			except Exception:
				# Avoid crashing on TTS errors; wait briefly
				time.sleep(0.1)
		if self._voice is not None:
			try:
				self._voice.Speak("", SVSF_ASYNC | SVSF_PURGE_BEFORE_SPEAK)
			except Exception:
				pass

	def speak(self, text: str, interrupt: bool = False) -> None:
		if not text:
			return
		# Drop anything not yet spoken: only the latest scene matters
		while True:
			try:
				self._queue.get_nowait()
			except queue.Empty:
				break
		self._queue.put((text, interrupt))

	def stop(self) -> None:
		self._running = False
		# Unblock the queue
		self._queue.put(("", False))
		try:
			self._thread.join(timeout=1.0)
		except Exception:
			pass
