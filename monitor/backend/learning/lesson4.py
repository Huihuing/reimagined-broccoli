from learning.support import read_observation_file
from learning.normalize import normalize_events
from learning.http_rules import select_views, evaluate

if __name__ == "__main__":
    views = select_views(normalize_events(read_observation_file()["original_rows"]))
    for threshold in (10, 20):
        print(f"기준 {threshold}, 관찰 {len(views)}, 검토 후보: {evaluate(views, threshold)}")
