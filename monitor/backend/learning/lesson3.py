from learning.support import read_observation_file
from learning.normalize import normalize_events
from learning.http_rules import select_views

if __name__ == "__main__":
    rows = normalize_events(read_observation_file()["original_rows"])
    selected = select_views(rows)
    print(f"조회 {len(selected)}행 / ID:", [e["id"] for e in selected])
