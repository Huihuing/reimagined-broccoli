"""Optional OFFLINE educational PCAP: not captured from the real web board.

Creates a minimal PCAP with invented packet timestamps and sizes, then compares
the first five seconds against the first one second. No packets are transmitted.
"""
import argparse
import struct
from pathlib import Path

MAGIC = 0xA1B2C3D4
# Synthetic local demonstration frames, not actual Ethernet traffic.
FRAMES = [(0, 60), (0, 74), (1, 62), (2, 82), (3, 66), (4, 90), (5, 70)]


def create_demo_pcap(path: Path):
    with path.open("wb") as handle:
        handle.write(struct.pack("<IHHIIII", MAGIC, 2, 4, 0, 0, 65535, 1))
        for second, size in FRAMES:
            # Link-layer bytes are intentionally artificial and never interpreted
            # as real site traffic or evidence of an attacker.
            packet = b"\x00" * size
            handle.write(struct.pack("<IIII", 0 + second, 0, size, size))
            handle.write(packet)


def read_packet_rows(path: Path):
    result = []
    with path.open("rb") as handle:
        header = handle.read(24)
        if len(header) != 24 or struct.unpack("<I", header[:4])[0] != MAGIC:
            raise ValueError("Expected a little-endian pcap global header")
        while True:
            record = handle.read(16)
            if not record:
                break
            if len(record) != 16:
                raise ValueError("Truncated pcap record")
            ts_sec, ts_usec, included, original = struct.unpack("<IIII", record)
            if included > 65535 or len(handle.read(included)) != included:
                raise ValueError("Truncated packet")
            result.append({"time": ts_sec + ts_usec / 1_000_000, "bytes": original})
    return result


def summarize(rows, seconds):
    return {"window_seconds": seconds,
            "packet_count": sum(1 for row in rows if 0 <= row["time"] < seconds),
            "byte_sum": sum(row["bytes"] for row in rows if 0 <= row["time"] < seconds)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/day3-educational.pcap")
    args = parser.parse_args()
    path = Path(args.output)
    create_demo_pcap(path)
    packets = read_packet_rows(path)
    for seconds in (5, 1):
        print(summarize(packets, seconds))
    print("교육용 생성 PCAP이며 게시판 실제 네트워크 캡처가 아닙니다.")
