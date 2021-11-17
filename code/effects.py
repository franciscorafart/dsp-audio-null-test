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
            'centre_frequency_hz': 1300,
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
        self.signal_chain.append(effect(**config))

    def remove_effect(self, idx):
        self.signal_chain = self.signal_chain.remove(idx)

    def clear_effects(self):
        self.signal_chain = []

    def process_signal_chain(self, audio_array, fs):
        board = Pedalboard([], sample_rate=fs)

        for effect in self.signal_chain:
            board.append(effect)

        return board(audio_array)

    def get_mode(self, mode):
        #  LPF12, HPF12, ""BPF12, LPF24, HPF24, or BPF24
        if mode == 'Mode.LPF12':
            return LadderFilter.Mode.LPF12
        if mode == 'Mode.HPF12':
            return LadderFilter.Mode.HPF12
        if mode == 'Mode.BPF12':
            return LadderFilter.Mode.BPF12
        if mode == 'Mode.LPF24':
            return LadderFilter.Mode.LPF24
        if mode == 'Mode.HPF24':
            return LadderFilter.Mode.HPF24
        if mode == 'Mode.BPF24':
            return LadderFilter.Mode.BPF24

        return None

