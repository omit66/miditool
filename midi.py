from mido import MidiFile
import argparse
import os


class Midi():

    instrument_mapping = {
        # Piano
        0:	"Acoustic Piano",
        1:	"Bright Piano",
        2:	"Electric Grand Piano",
        3:	"Honky-tonk Piano",
        4:	"Electric Piano 1",
        5:	"Electric Piano 2",
        6:	"Harpsichord",
        7:	"Clavinet",

        # Chromatic Percussion 
        8:	"Celesta",
        9:	"Glockenspiel",
        10:	"Music Box",
        11:	"Vibraphone",
        12:	"Marimba",
        13:	"Xylophone",
        14:	"Tubular Bells",
        15:	"Dulcimer",

        # Organ
        16:	"Drawbar Organ",
        17:	"Percussive Organ",
        18:	"Rock Organ",
        19:	"Church Organ",
        20:	"Reed Organ",
        21:	"Accordion",
        22:	"Harmonica",
        24:	"Acoustic Guitar (nylon)",
        25:	"Acoustic Guitar (steel)",
        26:	"Electric Guitar (jazz)",
        27:	"Electric Guitar (clean)",
        28:	"Electric Guitar (muted)",
        29:	"Overdriven Guitar",
        30:	"Distortion Guitar",
        31:	"Guitar Harmonics",
        32:	"Acoustic Bass",
        33:	"Electric Bass (finger)",
        34:	"Electric Bass (pick)",
        35:	"Fretless Bass",
        36:	"Slap Bass 1",
        37:	"Slap Bass 2",
        38:	"Synth Bass 1",
        39:	"Synth Bass 2",
        40:	"Violin",
        41:	"Viola",
        42:	"Cello",
        43:	"Contrabass",
        44:	"Tremolo Strings",
        45:	"Pizzicato Strings",
        46:	"Orchestral Harp",
        47:	"Timpani",
        48:	"String Ensemble 1",
        49:	"String Ensemble 2",
        50:	"Synth Strings 1",
        51:	"Synth Strings 2",
        52:	"Choir Aahs",
        53:	"Voice Oohs",
        54:	"Synth Choir",
        55:	"Orchestra Hit",
        56:	"Trumpet",
        57:	"Trombone",
        58:	"Tuba",
        59:	"Muted Trumpet",
        60:	"French Horn",
        61:	"Brass Section",
        62:	"Synth Brass 1",
        63:	"Synth Brass 2",
        64:	"Soprano Sax",
        65:	"Alto Sax",
        66:	"Tenor Sax",
        67:	"Baritone Sax",
        68:	"Oboe",
        69:	"English Horn",
        70:	"Bassoon",
        71:	"Clarinet",

        # Pipe
        72:	"Piccolo",
        73:	"Flute",
        74:	"Recorder",
        75:	"Pan Flute",
        76:	"Blown bottle",
        77:	"Shakuhachi",
        78:	"Whistle",
        79:	"Ocarina",

        # Synth Lead 
        80:	"Lead 1 (square)",
        81:	"Lead 2 (sawtooth)",
        82:	"Lead 3 (calliope)",
        83:	"Lead 4 (chiff)",
        84:	"Lead 5 (charang)",
        85:	"Lead 6 (voice)",
        86:	"Lead 7 (fifths)",
        87:	"Lead 8 (bass + lead)",

        # Synth Pad 
        88:	"Pad 1 (new age)",
        89:	"Pad 2 (warm)",
        90:	"Pad 3 (polysynth)",
        91:	"Pad 4 (choir)",
        92:	"Pad 5 (bowed)",
        93:	"Pad 6 (metallic)",
        94:	"Pad 7 (halo)",
        95:	"Pad 8 (sweep)",

        # Synth Effects 
        96:	"FX 1 (rain)",
        97:	"FX 2 (soundtrack)",
        98:	"FX 3 (crystal)",
        99:	"FX 4 (atmosphere)",
        100:	"FX 5 (brightness)",
        101:	"FX 6 (goblins)",
        102:	"FX 7 (echoes)",
        103:	"FX 8 (sci-fi)",

        # Ethnic 
        104:	"Sitar",
        105:	"Banjo",
        106:	"Shamisen",
        107:	"Koto",
        108:	"Kalimba",
        109:	"Bagpipe",
        110:	"Fiddle",
        111:	"Shanai",

        # Percussive
        112:	"Tinkle Bell",
        113:	"Agogo",
        114:	"Steel Drums",
        115:	"Woodblock",
        116:	"Taiko Drum",
        117:	"Melodic Tom",
        118:	"Synth Drum",
        119:	"Reverse Cymbal",

        # Sound effects
        120:	"Guitar Fret Noise",
        121:	"Breath Noise",
        122:	"Seashore",
        123:	"Bird Tweet",
        124:	"Telephone Ring",
        125:	"Helicopter",
        126:	"Applause",
        127:	"Gunshot",
        }

    def __init__(self, filename):
        self.filename = filename
        self.mid = MidiFile(filename)


    def get_track_names(self):
        res = []
        for track in self.mid.tracks:
            res.append(track.name)
        return res

    def get_instrument_codes(self):
        res = []
        for track in self.mid.tracks:
            for msg in track:
                if msg.type == "program_change":
                    res.append(msg.program)
        return res

    def get_instruments(self):
        res = []
        for i in self.get_instrument_codes():
            res.append(self.instrument_mapping.get(i, "No Instrument found ({})".format(i)))
        return res

    def is_piano_only(self):
        # 0 - 7 is the piano section
        res = all(i <= 7 for i in self.get_instrument_codes())
        return res


def main(args):
    if not os.path.exists(args.filename):
        argparse.ArgumentTypeError('The filename does not exist')

    m = Midi(args.filename)
    if args.is_piano:
        print(m.is_piano_only())
    elif args.track_names:
        for (i, track) in enumerate(m.get_track_names()):
            print("Track {}: {}".format(i, track))
    else:
        print(m.get_instruments())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse a midi file.")
    parser.add_argument('filename', type=str,
                        help='name of a midi file')
    g = parser.add_mutually_exclusive_group()
    # subparsers.add_parser('list_instruments')
    g.add_argument('--is_piano', action='store_true')
    g.add_argument('--track_names', action='store_true')

    args = parser.parse_args()
    main(args)


