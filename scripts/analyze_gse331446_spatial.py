#!/usr/bin/env python3
"""Summarize GSE331446 Visium files and marker-level spatial results.

This analysis is deliberately conservative: Visium spots are not single cells,
so the cell categories below are marker-score proxies for spatial spots rather
than definitive cell calls.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

try:
    import h5py
except ImportError:  # pragma: no cover - handled at runtime
    h5py = None


GEO_SAMPLE_METADATA = {
    "Sample_8A": {"geo_accession": "GSM9746005", "library": "Spatial_8A", "batch": "Batch1"},
    "Sample_8C": {"geo_accession": "GSM9746006", "library": "Spatial_8C", "batch": "Batch1"},
    "Sample_9A": {"geo_accession": "GSM9746007", "library": "Spatial_9A", "batch": "Batch2"},
    "Sample_9B": {"geo_accession": "GSM9746008", "library": "Spatial_9B", "batch": "Batch2"},
    "Sample_9C": {"geo_accession": "GSM9746009", "library": "Spatial_9C", "batch": "Batch2"},
    "Sample_9D": {"geo_accession": "GSM9746010", "library": "Spatial_9D", "batch": "Batch2"},
}

MARKER_SETS = {
    "cardiomyocyte": [
        "TTN",
        "MYH6",
        "MYH7",
        "TNNT2",
        "TNNI3",
        "ACTC1",
        "MYL2",
        "MYL7",
        "MYBPC3",
        "NPPA",
        "NPPB",
    ],
    "pacemaker_autonomic": [
        "HCN4",
        "SHOX2",
        "TBX3",
        "TBX18",
        "ISL1",
        "CACNA1D",
        "CACNA1G",
        "RYR2",
        "GJA5",
        "TBX5",
    ],
    "macrophage_anxa4": [
        "ANXA4",
        "CD68",
        "LYZ",
        "C1QA",
        "C1QB",
        "C1QC",
        "CD14",
        "FCGR3A",
        "MSR1",
        "MARCO",
        "CD163",
        "MRC1",
        "IL1B",
        "CCL2",
    ],
}

REQUIRED_SPACE_RANGER_FILES = [
    "filtered_feature_bc_matrix/barcodes.tsv.gz",
    "filtered_feature_bc_matrix/features.tsv.gz",
    "filtered_feature_bc_matrix/matrix.mtx.gz",
    "filtered_feature_bc_matrix.h5",
    "spatial/tissue_positions.csv",
    "spatial/scalefactors_json.json",
    "spatial/tissue_hires_image.png",
    "spatial/tissue_lowres_image.png",
    "spatial/aligned_fiducials.jpg",
    "spatial/detected_tissue_image.jpg",
    "spatial/spatial_enrichment.csv",
    "metrics_summary.csv",
    "web_summary.html",
]


def decode(value: bytes | str) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("rt", encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str] | None = None) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_metrics(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        return next(reader, {})


def read_tissue_positions(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        return {row["barcode"]: row for row in reader}


def read_features(path: Path) -> list[str]:
    genes: list[str] = []
    with open_text(path) as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                genes.append(parts[1])
            elif parts:
                genes.append(parts[0])
    return genes


def read_barcodes(path: Path) -> list[str]:
    with open_text(path) as handle:
        return [line.strip() for line in handle if line.strip()]


def selected_gene_map(genes: list[str]) -> dict[int, str]:
    selected = set().union(*[set(markers) for markers in MARKER_SETS.values()])
    return {idx: gene for idx, gene in enumerate(genes) if gene in selected}


def percentile(values: list[float], q: float) -> float:
    clean = sorted(v for v in values if not math.isnan(v))
    if not clean:
        return math.nan
    if len(clean) == 1:
        return clean[0]
    pos = (len(clean) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return clean[lo]
    return clean[lo] + (clean[hi] - clean[lo]) * (pos - lo)


def initialize_marker_arrays(barcodes: list[str]) -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    gene_counts = {
        gene: [0.0] * len(barcodes)
        for gene in sorted(set().union(*[set(markers) for markers in MARKER_SETS.values()]))
    }
    set_counts = {name: [0.0] * len(barcodes) for name in MARKER_SETS}
    return gene_counts, set_counts


def read_mtx_counts(sample_dir: Path) -> dict:
    matrix_dir = sample_dir / "filtered_feature_bc_matrix"
    features_path = matrix_dir / "features.tsv.gz"
    barcodes_path = matrix_dir / "barcodes.tsv.gz"
    matrix_path = matrix_dir / "matrix.mtx.gz"
    if not (features_path.exists() and barcodes_path.exists() and matrix_path.exists()):
        raise FileNotFoundError("complete Matrix Market files are not present")

    genes = read_features(features_path)
    barcodes = read_barcodes(barcodes_path)
    gene_by_idx = selected_gene_map(genes)
    gene_counts, set_counts = initialize_marker_arrays(barcodes)
    total_by_spot = [0.0] * len(barcodes)
    total_umis = 0.0
    shape = None
    nnz = None

    gene_to_sets: dict[str, list[str]] = defaultdict(list)
    for set_name, markers in MARKER_SETS.items():
        for marker in markers:
            gene_to_sets[marker].append(set_name)

    with gzip.open(matrix_path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("%"):
                continue
            parts = line.strip().split()
            if not parts:
                continue
            if shape is None:
                shape = tuple(int(part) for part in parts[:3])
                nnz = shape[2]
                continue
            gene_idx = int(parts[0]) - 1
            spot_idx = int(parts[1]) - 1
            count = float(parts[2])
            total_umis += count
            total_by_spot[spot_idx] += count
            gene = gene_by_idx.get(gene_idx)
            if gene:
                gene_counts[gene][spot_idx] += count
                for set_name in gene_to_sets[gene]:
                    set_counts[set_name][spot_idx] += count

    return {
        "source": "matrix_market",
        "genes": genes,
        "barcodes": barcodes,
        "shape": shape,
        "nnz": nnz,
        "total_umis": total_umis,
        "total_by_spot": total_by_spot,
        "gene_counts": gene_counts,
        "set_counts": set_counts,
    }


def read_h5_counts(sample_dir: Path) -> dict:
    if h5py is None:
        raise RuntimeError("h5py is required to read filtered_feature_bc_matrix.h5")
    h5_path = sample_dir / "filtered_feature_bc_matrix.h5"
    if not h5_path.exists():
        raise FileNotFoundError("filtered_feature_bc_matrix.h5 is not present")

    with h5py.File(h5_path, "r") as handle:
        matrix = handle["matrix"]
        barcodes = [decode(value) for value in matrix["barcodes"][:]]
        genes = [decode(value) for value in matrix["features"]["name"][:]]
        data = matrix["data"][:]
        indices = matrix["indices"][:]
        indptr = matrix["indptr"][:]
        shape = tuple(int(value) for value in matrix["shape"][:])

    gene_by_idx = selected_gene_map(genes)
    gene_counts, set_counts = initialize_marker_arrays(barcodes)
    total_by_spot = [0.0] * len(barcodes)
    total_umis = 0.0

    gene_to_sets: dict[str, list[str]] = defaultdict(list)
    for set_name, markers in MARKER_SETS.items():
        for marker in markers:
            gene_to_sets[marker].append(set_name)

    for spot_idx in range(len(barcodes)):
        start = int(indptr[spot_idx])
        end = int(indptr[spot_idx + 1])
        counts = data[start:end]
        feature_indices = indices[start:end]
        spot_total = float(counts.sum())
        total_by_spot[spot_idx] = spot_total
        total_umis += spot_total
        for feature_idx, count in zip(feature_indices, counts, strict=False):
            gene = gene_by_idx.get(int(feature_idx))
            if not gene:
                continue
            value = float(count)
            gene_counts[gene][spot_idx] += value
            for set_name in gene_to_sets[gene]:
                set_counts[set_name][spot_idx] += value

    return {
        "source": "h5",
        "genes": genes,
        "barcodes": barcodes,
        "shape": shape,
        "nnz": int(len(data)),
        "total_umis": total_umis,
        "total_by_spot": total_by_spot,
        "gene_counts": gene_counts,
        "set_counts": set_counts,
    }


def normalized(values: list[float], totals: list[float], scale: float = 10_000.0) -> list[float]:
    out: list[float] = []
    for value, total in zip(values, totals, strict=False):
        out.append((value / total * scale) if total > 0 else 0.0)
    return out


def summarize_counts(sample: str, counts: dict) -> tuple[list[dict], list[dict], dict]:
    totals = counts["total_by_spot"]
    gene_rows: list[dict] = []
    for gene, values in counts["gene_counts"].items():
        total = sum(values)
        gene_rows.append(
            {
                "sample": sample,
                "gene": gene,
                "total_counts": total,
                "spots_detected": sum(1 for value in values if value > 0),
                "mean_count_per_spot": total / len(values) if values else 0,
                "mean_cpm10k_per_spot": sum(normalized(values, totals)) / len(values) if values else 0,
            }
        )

    set_norm = {name: normalized(values, totals) for name, values in counts["set_counts"].items()}
    marker_rows: list[dict] = []
    for set_name, scores in set_norm.items():
        marker_rows.append(
            {
                "sample": sample,
                "marker_set": set_name,
                "markers_requested": ";".join(MARKER_SETS[set_name]),
                "markers_present": ";".join(gene for gene in MARKER_SETS[set_name] if gene in counts["genes"]),
                "mean_cpm10k_score": sum(scores) / len(scores) if scores else 0,
                "median_cpm10k_score": percentile(scores, 0.5),
                "q75_cpm10k_score": percentile(scores, 0.75),
                "spots_with_signal": sum(1 for score in scores if score > 0),
            }
        )

    dominant = defaultdict(int)
    for i in range(len(counts["barcodes"])):
        spot_scores = {name: scores[i] for name, scores in set_norm.items()}
        best_name, best_score = max(spot_scores.items(), key=lambda item: item[1])
        dominant[best_name if best_score > 0 else "no_marker_signal"] += 1

    anxa4_scores = normalized(counts["gene_counts"].get("ANXA4", [0.0] * len(totals)), totals)
    macrophage_scores = set_norm["macrophage_anxa4"]
    anxa4_q75 = percentile([score for score in anxa4_scores if score > 0], 0.75)
    macrophage_q75 = percentile([score for score in macrophage_scores if score > 0], 0.75)
    if math.isnan(anxa4_q75):
        anxa4_q75 = math.inf
    if math.isnan(macrophage_q75):
        macrophage_q75 = math.inf
    high_anxa4_macrophage = sum(
        1
        for anxa4_score, macrophage_score in zip(anxa4_scores, macrophage_scores, strict=False)
        if anxa4_score >= anxa4_q75 and macrophage_score >= macrophage_q75
    )
    proxy_summary = {
        "sample": sample,
        "total_filtered_spots": len(counts["barcodes"]),
        "dominant_cardiomyocyte_spots": dominant["cardiomyocyte"],
        "dominant_pacemaker_autonomic_spots": dominant["pacemaker_autonomic"],
        "dominant_macrophage_anxa4_spots": dominant["macrophage_anxa4"],
        "no_marker_signal_spots": dominant["no_marker_signal"],
        "anxa4_positive_spots": sum(1 for score in anxa4_scores if score > 0),
        "anxa4_q75_cpm10k_positive_spots": anxa4_q75 if anxa4_q75 != math.inf else "",
        "macrophage_q75_cpm10k_positive_spots": macrophage_q75 if macrophage_q75 != math.inf else "",
        "anxa4_high_macrophage_proxy_spots": high_anxa4_macrophage,
    }
    return gene_rows, marker_rows, proxy_summary


def read_spatial_enrichment(sample: str, path: Path, marker_genes: set[str], top_n: int) -> tuple[list[dict], list[dict]]:
    if not path.exists():
        return [], []
    marker_rows: list[dict] = []
    top_rows: list[dict] = []
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    rows_sorted = sorted(rows, key=lambda row: float(row.get("I", "nan")), reverse=True)
    for rank, row in enumerate(rows_sorted[:top_n], start=1):
        top_rows.append({"sample": sample, "rank_by_morans_i": rank, **row})
    for row in rows:
        if row.get("Feature Name") in marker_genes:
            marker_rows.append({"sample": sample, **row})
    return marker_rows, top_rows


def inventory_sample(sample_dir: Path) -> dict:
    sample = sample_dir.name
    metadata = GEO_SAMPLE_METADATA.get(sample, {})
    row = {
        "sample": sample,
        "geo_accession": metadata.get("geo_accession", ""),
        "library": metadata.get("library", ""),
        "batch": metadata.get("batch", ""),
        "source_name": "right atrial appendage",
        "technology": "10x Genomics Visium Spatial Gene Expression FFPE",
    }
    missing: list[str] = []
    for relative in REQUIRED_SPACE_RANGER_FILES:
        exists = (sample_dir / relative).exists()
        row[relative] = "yes" if exists else "no"
        if not exists:
            missing.append(relative)
    row["missing_files"] = ";".join(missing)
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data") / "GSE331446")
    parser.add_argument("--out-dir", type=Path, default=Path("analysis") / "GSE331446")
    parser.add_argument("--top-se", type=int, default=20, help="Top spatial_enrichment rows per sample.")
    args = parser.parse_args()

    extracted = args.data_dir / "extracted"
    args.out_dir.mkdir(parents=True, exist_ok=True)
    sample_dirs = sorted(path for path in extracted.glob("GSM*/Sample_*") if path.is_dir())
    if not sample_dirs:
        raise SystemExit(f"No sample directories found under {extracted}")

    marker_genes = set().union(*[set(markers) for markers in MARKER_SETS.values()])
    inventory_rows: list[dict] = []
    qc_rows: list[dict] = []
    gene_rows: list[dict] = []
    marker_rows: list[dict] = []
    proxy_rows: list[dict] = []
    se_marker_rows: list[dict] = []
    se_top_rows: list[dict] = []

    for sample_dir in sample_dirs:
        sample = sample_dir.name
        print(f"Analyzing {sample}")
        inventory_rows.append(inventory_sample(sample_dir))
        metrics = read_metrics(sample_dir / "metrics_summary.csv")
        positions = read_tissue_positions(sample_dir / "spatial" / "tissue_positions.csv")

        counts = None
        count_error = ""
        for reader in (read_mtx_counts, read_h5_counts):
            try:
                counts = reader(sample_dir)
                break
            except Exception as exc:  # noqa: BLE001 - keep fallback reason in output
                count_error = str(exc)
        if counts is None:
            print(f"Skipping counts for {sample}: {count_error}")
        else:
            sample_gene_rows, sample_marker_rows, sample_proxy = summarize_counts(sample, counts)
            gene_rows.extend(sample_gene_rows)
            marker_rows.extend(sample_marker_rows)
            proxy_rows.append(sample_proxy)

        qc = {
            "sample": sample,
            "geo_accession": GEO_SAMPLE_METADATA.get(sample, {}).get("geo_accession", ""),
            "batch": GEO_SAMPLE_METADATA.get(sample, {}).get("batch", ""),
            "matrix_source": counts["source"] if counts else "",
            "matrix_rows_genes": counts["shape"][0] if counts and counts["shape"] else "",
            "matrix_columns_spots": counts["shape"][1] if counts and counts["shape"] else "",
            "matrix_nnz": counts["nnz"] if counts else "",
            "matrix_total_umis": counts["total_umis"] if counts else "",
            "positions_rows": len(positions),
            "positions_in_tissue_rows": sum(1 for row in positions.values() if row.get("in_tissue") == "1"),
            "count_read_error": "" if counts else count_error,
        }
        qc.update(metrics)
        qc_rows.append(qc)

        marker_se, top_se = read_spatial_enrichment(
            sample,
            sample_dir / "spatial" / "spatial_enrichment.csv",
            marker_genes,
            args.top_se,
        )
        se_marker_rows.extend(marker_se)
        se_top_rows.extend(top_se)

    write_csv(args.out_dir / "file_inventory.csv", inventory_rows)
    write_csv(args.out_dir / "space_ranger_qc_summary.csv", qc_rows)
    write_csv(args.out_dir / "marker_gene_counts.csv", gene_rows)
    write_csv(args.out_dir / "marker_score_summary.csv", marker_rows)
    write_csv(args.out_dir / "spot_marker_proxy_summary.csv", proxy_rows)
    write_csv(args.out_dir / "spatial_enrichment_marker_comparison.csv", se_marker_rows)
    write_csv(args.out_dir / "spatial_enrichment_top_features.csv", se_top_rows)

    metadata = {
        "series": "GSE331446",
        "source": "NCBI GEO",
        "tissue_constraint": "All six GEO samples are human right atrial appendage/right atrial FFPE sections.",
        "comparison_scope": "Within right atrial appendage Visium sections only.",
        "temporal_analysis": (
            "No explicit time point, AF/SR group, or ordered disease-stage metadata is provided in the "
            "GEO series matrix; sample identifiers 8A/8C/9A/9B/9C/9D should not be treated as time."
        ),
        "marker_sets": MARKER_SETS,
    }
    (args.out_dir / "metadata_and_scope.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote outputs to {args.out_dir}")


if __name__ == "__main__":
    main()
