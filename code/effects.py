from pedalboard import (
    Pedalboard,
    Distortion,
    Convolution,
    Compressor,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    LadderFilter,
    HighpassFilter,
    LowpassFilter,
    Phaser,
    NoiseGate,
)

# TODO: MAKE a class
# Create finctions to set effects proeprties
# Apply pedal shoud iterate through effects and apply only the ones activated

effect_map = {
    'gain': {
        'instance': Gain,
        'config': {
         'gain_db': 0,   
        },
    },
    'compressor': {
        'instance': Compressor,
        'config': {
            'threshold_db': 0,
            'ratio': 1,
            'attack_ms': 1,
            'release_ms': 100,
        },
    },
    'chorus': {
        'instance': Chorus,
        'config': {
            'rate_hz': 5, 
            'depth': 0.4, 
            'feedback': 0.8
        },
    },
    'ladder': {
        'instance': LadderFilter,
        'config': {
            'mode': LadderFilter.Mode.HPF12, 
            'cutoff_hz': 400
        },
    },
    'hpf': {
        'instance': HighpassFilter,
        'config': {
            'cutoff_frequency_hz': 50,
        },
    },
    'lpf': {
        'instance': LowpassFilter,
        'config': {
            'cutoff_frequency_hz': 2000,
        },
    },
    'gate': {
        'instance': NoiseGate,
        'config': {
            'threshold_db': -100, 
            'ratio': 10, 
            'attack_ms': 1, 
            'release_ms': 100,
        }
    },
    'phaser': {
        'instance': Phaser,
        'config': {
            'rate_hz': 1, 
            'depth': 0.5, 
            'center_frequency_hz': 1300, 
            'feedback': 0, 
            'mix': 0.5,
        },
    },
    'reverb': {
        'instance': Reverb,
        'config': {
            'room_size': 0.5, 
            'damping': 0.5, 
            'wet_level': 0.33, 
            'dry_level': 0.4, 
            'width': 1, 
            'freeze_mode': 0.0,
        }
    },
    'limiter': {
        'instance': Limiter,
        'config': {
            'threshold_db': -10, 
            'release_ms': 100,
        }
    },
    'distortion': {
        'instance': Distortion,
        'config': {
            'drive_db': 25,
        }
    },
    'convolution': {
        'instance': Convolution,
        'config': {
            'file': '' # LLL
        },
    },
    # 'delay': Delay,
}

class Pedal():
    def __init__(self, initial_signal_chain = []):
        self.signal_chain = initial_signal_chain

    def add_effect(self, effect, config={}):
        # default_config = effect_object.config
        # TODO: Initialize with config values
        self.signal_chain.append(effect(**config))

    def remove_effect(self, idx):
        self.signal_chain = self.signal_chain.remove(idx)

    def clear_effects(self):
        self.signal_chain = []

    def process_signal_chain(self, audio_array, fs):
        board = Pedalboard([], sample_rate=fs)

        for effect in self.signal_chain:
            board.append(effect)

        # board = Pedalboard([
        # Compressor(threshold_db=-50, ratio=25), # threshold_db=0, ratio=1, attackMs=1, releaseMS=100
        # Gain(gain_db=30), # Compensation # gain_db=1
        # Chorus(rate_hz=5, depth=0.4, feedback=0.8), # rate_hz = 1, depth=0.25, centreDelayMs=7.0, feedback=0.0, mix=0.5
        # LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=400), # mode, cutoff_hz=200, resonance=0, drive=1
        # Phaser(), # rate_hz=1, depth-0.5, centre_frequency_hz=1300, feedback=0, mix=0.5
        # Distortion(drive_db=50), # drive_db=25)
        # Convolution("./guitar_amp.wav", 1.0),
        # HighpassFilter(), # cutoff_frequency_hz=50
        # LowpassFilter(cutoff_frequency_hz=2000), # cutoff_frequency_hz=50
        # NoiseGate(), #threshold_db=-100, ratio=10, attack_ms=1, release_ms=100
        # Reverb(room_size=0.75), # room_size=0.5, damping=0.5, wet_level=0.33, dry_level=0.4, width=1, freeze_mode=0.0
    # ], sample_rate=fs)

        # Pedalboard objects behave like lists, so you can add plugins:
        # board.append(Limiter()) # threshold_db (-10dB default), release_ms (100ms default)

        return board(audio_array)

