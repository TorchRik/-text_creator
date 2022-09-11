import argparse
from model import Model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, help='Path to model safe file', required=True)
    parser.add_argument('--input-dir', type=str, help='Train data dir if None model will train by stdin')
    args = parser.parse_args()

    path_to_model = args.model if args.model else 'trained_model'

    text = ""
    if args.input_dir is None:
        s = input()
        while s:
            text += s
            s = input()

    model = Model(args.model, args.input_dir, text)
    model.fit()
    model.save_me()
