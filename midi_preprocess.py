# This program is for processing midis
# including seperating tracks and normalization
import pretty_midi
import os
import argparse
from tqdm import tqdm

bass_range = range(33, 41)
sax_range = range(65, 69)

def guess_melody(midi_data):
    for instrument in midi_data.instruments:
        if instrument.program in sax_range:
            return True
    return False

def detect_bass_drum(midi_data):
    has_bass = False
    has_drum = False
    for instrument in midi_data.instruments:
        has_bass |= instrument.program in bass_range
        has_drum |= instrument.is_drum
    return has_bass and has_drum

def filter_tracks(instrument):
    return instrument.program in sax_range or instrument.program in bass_range or instrument.is_drum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="Source directory of midis to be processed")
    parser.add_argument("output_dir", type=str, help="Destination directory of processed midis")
    parser.add_argument("-g", "--guess_vocal", action="store_true", help="Also attempt to detect if a midi has melody (Saxphone)")
    parser.add_argument("-t", "--truncate_tracks", action="store_true", help="Whether we should remove other tracks from the midis")
    args = parser.parse_args()

    output_dir = args.output_dir
    input_dir = args.input_dir
    truncate_tracks = args.truncate_tracks
    guess_vocal = args.guess_vocal | truncate_tracks

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for root, _, filenames in os.walk(input_dir):
        for fn in tqdm(filenames):
            if os.path.splitext(fn)[-1] == ".mid":
                try:
                    midi_data = pretty_midi.PrettyMIDI(os.path.join(root, fn))
                except:
                    print("Error loading", fn)
                    continue
                if detect_bass_drum(midi_data):
                    if guess_vocal and not guess_melody(midi_data):
                        continue
                    if truncate_tracks:
                        midi_data.instruments = list(filter(filter_tracks, midi_data.instruments))
                    midi_data.write(os.path.join(output_dir, fn))

if __name__ == '__main__':
    main()