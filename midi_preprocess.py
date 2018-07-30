# This program is for processing midis
# including seperating tracks and normalization
import pretty_midi
import os
import argparse
from tqdm import tqdm

def guess_melody(midi_data):
    pass

def detect_bass_drum(midi_data):
    bass_range = range(33, 41)
    has_bass = False
    has_drum = False
    for instrument in midi_data.instruments:
        has_bass |= instrument.program in bass_range
        has_drum |= instrument.is_drum
    return has_bass and has_drum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help="Source directory of midis to be processed")
    parser.add_argument("output_dir", type=str, help="Destination directory of processed midis")
    args = parser.parse_args()

    output_dir = args.output_dir
    input_dir = args.input_dir

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
                    print(fn)
                    midi_data.write(os.path.join(output_dir, fn))

if __name__ == '__main__':
    main()