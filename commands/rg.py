import os

def rg_cmd(args):
    if len(args) < 2:
        print("Usage: rg <text> <file_or_folder>")
        return

    search_text = args[0].encode()
    target = args[1]

    def search_file(file_path):
        try:
            with open(file_path, "rb") as f:  # faster than text mode
                for line_num, line in enumerate(f, start=1):
                    if search_text in line:
                        try:
                            decoded = line.decode(errors="ignore").strip()
                        except:
                            decoded = ""
                        print(f"{file_path}:{line_num}: {decoded}")

        except:
            pass

    if os.path.isfile(target):
        search_file(target)

    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                path = os.path.join(root, file)
                search_file(path)

    else:
        print("File or folder not found:", target)
