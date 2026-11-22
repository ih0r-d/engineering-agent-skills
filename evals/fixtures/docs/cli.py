import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    print('{"status": "ok"}' if args.format == "json" else "ok")


if __name__ == "__main__":
    main()
