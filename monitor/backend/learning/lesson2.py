from learning.support import read_observation_file
from learning.normalize import normalize_events

if __name__ == "__main__":
    data = read_observation_file()
    normalized = normalize_events(data["original_rows"])
    print(f"원본 {len(data['original_rows'])}행 / 정규화 {len(normalized)}행")
    for item in normalized:
        print(item["id"], item["source"], item["kind"], item["received_at"])
