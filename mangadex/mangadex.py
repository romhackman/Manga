import argparse
from mangadex import search, chapters, pages
from downloader import download_chapter

parser = argparse.ArgumentParser(description="MangaDex Downloader CLI")
sub = parser.add_subparsers(dest="cmd")

# Recherche manga
s = sub.add_parser("search")
s.add_argument("title")

# Liste des chapitres
c = sub.add_parser("chapters")
c.add_argument("manga_id")

# Télécharger chapitre
d = sub.add_parser("download")
d.add_argument("chapter_id")
d.add_argument("-o", "--out", default="downloads")
d.add_argument("--cbz", action="store_true")

args = parser.parse_args()

if args.cmd == "search":
    res = search(args.title)
    for m in res:
        t = m["attributes"]["title"].get("en", "N/A")
        print(f"{t} | ID: {m['id']}")

elif args.cmd == "chapters":
    chs = chapters(args.manga_id)
    for ch in chs:
        num = ch["attributes"]["chapter"] or "N/A"
        title = ch["attributes"]["title"] or ""
        print(f"Chap {num} {title} | ID: {ch['id']}")

elif args.cmd == "download":
    data = pages(args.chapter_id)
    download_chapter(data, args.out, args.cbz)

else:
    parser.print_help()
