#!/usr/bin/env python3
"""Download and unpack the GEO GSE331446 Visium supplemental archive.

The script intentionally keeps downloaded data under data/GSE331446 by default.
That directory is ignored by git because the GEO archive and extracted Space
Ranger outputs are data artifacts, not source code.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import shutil
import tarfile
import xml.etree.ElementTree as ET
import urllib.request
from urllib.parse import urlencode
from pathlib import Path


GEO_SERIES = "GSE331446"
GEO_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE331nnn/GSE331446"
SUPPL_BASE = f"{GEO_BASE}/suppl"
ARCHIVE_NAME = "GSE331446_RAW.tar"
ARCHIVE_SIZE = 180_715_520
SERIES_MATRIX_URL = f"{GEO_BASE}/matrix/GSE331446_series_matrix.txt.gz"
FILELIST_URL = f"{SUPPL_BASE}/filelist.txt"
ARCHIVE_URL = f"{SUPPL_BASE}/{ARCHIVE_NAME}"
SRA_EXPERIMENTS = [
    "SRX33529334",
    "SRX33529335",
    "SRX33529336",
    "SRX33529337",
    "SRX33529338",
    "SRX33529339",
]


def download(url: str, destination: Path, expected_size: int | None = None, force: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        if expected_size is None or destination.stat().st_size == expected_size:
            print(f"Using existing {destination} ({destination.stat().st_size} bytes)")
            return
        print(f"Existing file has unexpected size; re-downloading {destination}")

    tmp = destination.with_suffix(destination.suffix + ".part")
    if tmp.exists():
        tmp.unlink()
    print(f"Downloading {url} -> {destination}")
    with urllib.request.urlopen(url, timeout=120) as response, tmp.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    tmp.rename(destination)

    if expected_size is not None and destination.stat().st_size != expected_size:
        raise RuntimeError(
            f"Downloaded {destination} has {destination.stat().st_size} bytes, "
            f"expected {expected_size}"
        )


def safe_extract(tar_path: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    with tarfile.open(tar_path) as archive:
        members = archive.getmembers()
        root = destination.resolve()
        for member in members:
            target = (destination / member.name).resolve()
            if not str(target).startswith(str(root)):
                raise RuntimeError(f"Unsafe member path in {tar_path}: {member.name}")
        archive.extractall(destination)
        extracted = [member.name for member in members]
    return extracted


def parse_filelist(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open(newline="") as handle:
        reader = csv.DictReader(
            (line for line in handle if not line.startswith("#")),
            delimiter="\t",
            fieldnames=["archive_or_file", "name", "time", "size", "type"],
        )
        for row in reader:
            if row["archive_or_file"] in {"Archive", "File"}:
                rows.append(row)
    return rows


def write_series_matrix_text(raw_path: Path, text_path: Path) -> None:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(raw_path, "rt", encoding="utf-8", errors="replace") as source:
        text_path.write_text(source.read(), encoding="utf-8")


def fetch_sra_runs() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for experiment_accession in SRA_EXPERIMENTS:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urlencode(
            {"db": "sra", "term": experiment_accession, "retmode": "json"}
        )
        with urllib.request.urlopen(search_url, timeout=60) as response:
            ids = json.loads(response.read().decode("utf-8"))["esearchresult"]["idlist"]
        if not ids:
            records.append({"srx": experiment_accession, "error": "not found"})
            continue

        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urlencode(
            {"db": "sra", "id": ids[0], "retmode": "xml"}
        )
        with urllib.request.urlopen(fetch_url, timeout=60) as response:
            root = ET.fromstring(response.read().decode("utf-8"))

        for package in root.findall(".//EXPERIMENT_PACKAGE"):
            experiment = package.find("EXPERIMENT")
            sample = package.find("SAMPLE")
            study = package.find("STUDY")
            for run in package.findall(".//RUN"):
                records.append(
                    {
                        "srx": experiment_accession,
                        "srr": run.attrib.get("accession", ""),
                        "spots": run.attrib.get("total_spots", ""),
                        "bases": run.attrib.get("total_bases", ""),
                        "size_bytes": run.attrib.get("size", ""),
                        "experiment_title": experiment.findtext("TITLE", "") if experiment is not None else "",
                        "sample_accession": sample.attrib.get("accession", "") if sample is not None else "",
                        "study_accession": study.attrib.get("accession", "") if study is not None else "",
                    }
                )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data") / GEO_SERIES)
    parser.add_argument("--force", action="store_true", help="Re-download files even if present.")
    parser.add_argument("--skip-download", action="store_true", help="Only unpack/analyze existing downloads.")
    args = parser.parse_args()

    raw_dir = args.data_dir / "raw"
    extracted_dir = args.data_dir / "extracted"
    metadata_dir = args.data_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    filelist_path = metadata_dir / "filelist.txt"
    series_matrix_gz = metadata_dir / "GSE331446_series_matrix.txt.gz"
    series_matrix_txt = metadata_dir / "GSE331446_series_matrix.txt"
    archive_path = raw_dir / ARCHIVE_NAME

    if not args.skip_download:
        download(FILELIST_URL, filelist_path, force=args.force)
        download(SERIES_MATRIX_URL, series_matrix_gz, force=args.force)
        download(ARCHIVE_URL, archive_path, expected_size=ARCHIVE_SIZE, force=args.force)

    write_series_matrix_text(series_matrix_gz, series_matrix_txt)
    filelist_rows = parse_filelist(filelist_path)

    top_level_members = safe_extract(archive_path, raw_dir)
    sample_manifests: dict[str, list[str]] = {}
    for sample_archive in sorted(raw_dir.glob("GSM*_Sample_*.tar.gz")):
        sample_key = sample_archive.name.removesuffix(".tar.gz")
        sample_destination = extracted_dir / sample_key
        print(f"Extracting {sample_archive.name}")
        sample_manifests[sample_key] = safe_extract(sample_archive, sample_destination)

    manifest = {
        "series": GEO_SERIES,
        "urls": {
            "filelist": FILELIST_URL,
            "series_matrix": SERIES_MATRIX_URL,
            "archive": ARCHIVE_URL,
        },
        "filelist": filelist_rows,
        "top_level_archive_members": top_level_members,
        "sample_archive_manifests": sample_manifests,
        "sra_runs": fetch_sra_runs(),
    }
    (metadata_dir / "download_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote manifest to {metadata_dir / 'download_manifest.json'}")


if __name__ == "__main__":
    main()
