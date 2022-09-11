import argparse
import pickle

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, help='Path to model safe file', required=True)
    parser.add_argument('--length', type=int, help="Length of text", required=True)
    parser.add_argument('--prefix', type=str, help="Started input")

    args = parser.parse_args()

    model_file = open(args.model, 'rb')
    model = pickle.load(model_file)
    prefix = args.prefix if args.prefix is not None else ""
    print(model.generate(args.length, prefix))
