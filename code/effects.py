from pedalboard import (
    Pedalboard,
    Convolution,
    Compressor,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    LadderFilter,
    Phaser,
)

def apply_pedal(audio_array, fs):
    board = Pedalboard([
    Compressor(threshold_db=-50, ratio=25),
    Gain(gain_db=30), # Compensation
    Chorus(),
    LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
    Phaser(),
    # Convolution("./guitar_amp.wav", 1.0),
    Reverb(room_size=0.25),
], sample_rate=fs)

    # Pedalboard objects behave like lists, so you can add plugins:
    board.append(Compressor(threshold_db=-25, ratio=10))
    board.append(Gain(gain_db=10))
    board.append(Limiter())

    effected = board(audio_array)

    return effected