#!/usr/bin/env python3
"""Create YYMMDD output folders and archive daily image/copy without overwrites."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SERIES_FOLDERS = {
    "core-signal": "每日核心信号",
    "one-line-judgment": "今日一句话判断",
}


def parse_date(value: str | None) -> str:
    if value is None:
        return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%y%m%d")
    for fmt in ("%y%m%d", "%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%y%m%d")
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("日期必须为 YYMMDD、YYYYMMDD 或 YYYY-MM-DD")


def versioned_path(folder: Path, filename: str) -> Path:
    candidate = folder / filename
    if not candidate.exists():
        return candidate
    stem, suffix = candidate.stem, candidate.suffix
    version = 2
    while True:
        candidate = folder / f"{stem}-v{version}{suffix}"
        if not candidate.exists():
            return candidate
        version += 1


def archive_file(source: str | None, folder: Path, filename: str) -> str | None:
    if not source:
        return None
    source_path = Path(source).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"找不到待归档文件：{source_path}")
    destination = versioned_path(folder, filename)
    shutil.copy2(source_path, destination)
    return str(destination)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="建立每日核心信号/今日一句话判断的六位日期目录并归档成品。"
    )
    parser.add_argument("--root", default=".", help="项目主目录，默认当前目录")
    parser.add_argument(
        "--series",
        choices=("both", *SERIES_FOLDERS),
        default="both",
        help="栏目；归档文件时必须选择单个栏目",
    )
    parser.add_argument("--date", help="可选：YYMMDD、YYYYMMDD 或 YYYY-MM-DD")
    parser.add_argument("--image", help="待归档图片路径")
    parser.add_argument("--content-file", help="待归档 UTF-8 文案文件路径")
    args = parser.parse_args()

    if args.series == "both" and (args.image or args.content_file):
        parser.error("归档图片或文案时，--series 必须选择单个栏目")

    root = Path(args.root).expanduser().resolve()
    date_code = parse_date(args.date)
    selected = SERIES_FOLDERS if args.series == "both" else {
        args.series: SERIES_FOLDERS[args.series]
    }

    result: dict[str, object] = {
        "root": str(root),
        "date": date_code,
        "folders": {},
        "archived": {},
    }
    for key, folder_name in selected.items():
        folder = root / folder_name / date_code
        folder.mkdir(parents=True, exist_ok=True)
        result["folders"][key] = str(folder)
        if args.series != "both":
            archived = {
                "image": archive_file(args.image, folder, "cover.png"),
                "content": archive_file(args.content_file, folder, "content.txt"),
            }
            result["archived"][key] = {k: v for k, v in archived.items() if v}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
