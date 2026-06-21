def cat_cmd(args):
    if not args:
        print("Usage: cat <file>")
        return

    filename = args[0]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(file.read())

    except FileNotFoundError:
        print(f"File not found: {filename}")

    except Exception as e:
        print(f"Error: {e}")
