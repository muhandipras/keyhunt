import os
import re
import argparse
from tqdm import tqdm

def load_keywords(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to load keywords from {file_path}: {e}")
        return []

def scan_file(file_path, keyword_files, keywords_to_search, output_scan, base_dir):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            file_with_keyword = False

            for line_num, line in enumerate(lines, start=1):
                for keyword in keywords_to_search:
                    if re.search(rf"\b{keyword}\b", line):
                        relative_path = os.path.relpath(file_path, base_dir)
                        output_scan.write(f"[!] Found '{keyword}' on line {line_num} in file /{os.path.basename(base_dir)}/{relative_path}\n")
                        file_with_keyword = True

            for line_num, line in enumerate(lines, start=1):
                if re.search(r"base64_decode\(['\"]?[A-Za-z0-9+/=]+['\"]?\)", line):
                    relative_path = os.path.relpath(file_path, base_dir)
                    output_scan.write(f"[!] Pattern base64_decode found on line {line_num} in file /{os.path.basename(base_dir)}/{relative_path}\n")
                    file_with_keyword = True

            if file_with_keyword:
                keyword_files.append(file_path)
    except Exception as e:
        print(f"[!] Failed to scan file {file_path}: {e}")

def scan_directory(directory, valid_extensions, keywords_to_search, output_scan):
    keyword_files = []
    all_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    with tqdm(total=len(all_files), desc="Scanning Files", unit="file") as pbar:
        for file_path in all_files:
            scan_file(file_path, keyword_files, keywords_to_search, output_scan, directory)
            pbar.update(1)

    return keyword_files

def remove_files_from_list(file_list):
    for file_path in file_list:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[+] Successfully deleted file: {file_path}")
            else:
                print(f"[!] File not found: {file_path}")
        except Exception as e:
            print(f"[!] Failed to delete file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan files for specified keywords.", usage="python %(prog)s <directory> -w <wordlist> -ext <extensions> [-rm <file_list>]")
    parser.add_argument("directory", help="Directory to scan", nargs="?", default=None)
    parser.add_argument("-w", "--wordlist", help="Path to the keyword list file", required=True, type=str)
    parser.add_argument("-ext", "--extensions", help="Comma-separated list of file extensions to scan", required=True, type=str)
    parser.add_argument("-rm", "--remove", help="Delete files listed in the specified file (e.g., path_file.txt)", type=str)
    args = parser.parse_args()

    if not args.directory and not args.remove:
        print("[!] A directory or file to delete must be provided!")
        parser.print_help()
        exit(1)

    keywords_to_search = []
    valid_extensions = []

    if args.wordlist:
        keywords_to_search = load_keywords(args.wordlist)

    if args.extensions:
        valid_extensions = [ext.strip() for ext in args.extensions.split(",")]

    if args.remove:
        if os.path.exists(args.remove):
            with open(args.remove, "r") as f:
                files_to_remove = [line.strip() for line in f.readlines()]
            remove_files_from_list(files_to_remove)
        else:
            print(f"[!] File {args.remove} not found.")
    else:
        if args.directory:
            if os.path.exists(args.directory):
                print("Starting scan...")
                keyword_files = []
                base_dir = os.path.basename(os.path.normpath(args.directory))
                with open("scan_results.txt", "w") as output_scan:
                    keyword_files = scan_directory(args.directory, valid_extensions, keywords_to_search, output_scan)

                with open("path_file.txt", "w") as keyword_file:
                    if keyword_files:
                        for file in keyword_files:
                            relative_path = os.path.relpath(file, args.directory)
                            keyword_file.write(f"/{base_dir}/{relative_path}\n")
                        print(f"\nScan complete. List of files with keywords saved to path_file.txt")
                    else:
                        print("No files with keywords found.")

                print(f"Detailed scan results saved to scan_results.txt")
            else:
                print("Directory not found. Ensure the path provided is correct.")
