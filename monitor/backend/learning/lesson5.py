from learning.support import read_observation_file
from learning.normalize import normalize_events
from learning.http_rules import select_views, find_following_errors

if __name__ == "__main__":
    rows = normalize_events(read_observation_file()["original_rows"])
    views = select_views(rows)
    errors = find_following_errors(rows, views)
    print(f"조회 {len(views)}행 / 뒤따른 404 {len(errors)}행 / 근거 ID", [e["id"] for e in views + errors])
