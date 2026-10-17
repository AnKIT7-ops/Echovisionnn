"""Self-check for announcement timing. Run: python src/test_scene_change.py"""
from scene_change import SceneChangeAnnouncer, summarize_scene, urgent_hazard

FAR = "chair far away on the left"
CLOSE = "person close ahead"
VERY_CLOSE = "person very close ahead"

assert urgent_hazard(f"{VERY_CLOSE}; {FAR}") == VERY_CLOSE
assert urgent_hazard("person medium distance ahead; chair close on the left") is None

# Center phrase comes first
dets = [("chair", 0.9, (0, 0, 50, 50)), ("person", 0.9, (300, 0, 340, 300))]
assert summarize_scene(dets, 640, 480).startswith("person")

a = SceneChangeAnnouncer(cooldown_seconds=3.0, refresh_seconds=15.0, urgent_gap_seconds=1.0)
assert a.should_announce(FAR, 0.0)
assert not a.should_announce("cup far away on the left", 1.0)  # normal change waits out cooldown
assert a.should_announce(CLOSE, 1.0)  # new hazard skips cooldown
assert not a.should_announce(VERY_CLOSE, 1.5)  # within urgent gap
assert a.should_announce(VERY_CLOSE, 2.0)  # getting closer is a new hazard
assert not a.should_announce("person medium distance ahead", 2.5)  # flicker away: cooldown
assert not a.should_announce(VERY_CLOSE, 3.5)  # flicker back to the same hazard: no repeat
assert a.should_announce(VERY_CLOSE, 17.0)  # refresh still fires
print("ok")
