# GSE331446右心房空间转录组数据追踪与补充分析

## 结论摘要

1. **比较部位**：GSE331446的6个GEO样本均为`right atrial appendage`（右心耳/右心房附属组织）FFPE Visium切片，因此本次补充分析限定在同一心肌部位内比较。
2. **SE比较**：这里将SE按GEO补充文件中的`spatial_enrichment.csv`理解，即Space Ranger输出的空间富集/Moran's I结果。本次已对心肌、自律/起搏、ANXA4/巨噬细胞标记基因做SE比较，输出见`analysis/GSE331446/spatial_enrichment_marker_comparison.csv`。
3. **细胞/spot区分**：Visium不是单细胞数据，不能直接把spot等同为细胞。本次用marker score区分三类空间spot代理：心肌细胞样、起搏/自律细胞样、ANXA4高表达巨噬细胞样，输出见`analysis/GSE331446/marker_score_summary.csv`和`analysis/GSE331446/spot_marker_proxy_summary.csv`。
4. **时序分析**：GEO series matrix没有时间点、AF/SR分组或有序疾病阶段字段；样本名`8A/8C/9A/9B/9C/9D`不能当作时间顺序。因此当前不能做严格时序分析，只能做横断面右心房空间比较。若后续获得独立阶段/时间元数据，脚本可在样本元数据层面扩展。
5. **现有`immune`脚本追踪**：现有脚本已包含MR/共定位、单细胞整合、SR/AF巨噬细胞差异、ANXA4表达和ANXA4高低组CellChat，但未见明确右心房限定、GSE331446空间数据导入、spatial enrichment比较或拟时序/时序分析。

## GEO/NCBI元数据核对

- Series: `GSE331446`
- Title: `Epicardial fat drives macrophage response in atrial cardiomyopathy`
- Organism: `Homo sapiens`
- 技术：10x Genomics Visium Spatial Gene Expression FFPE workflow
- 参考基因组：GRCh38
- 组织：全部为`right atrial appendage`
- 样本：

| GEO样本 | library | batch | 组织 |
|---|---:|---|---|
| GSM9746005 | Spatial_8A | Batch1 | right atrial appendage |
| GSM9746006 | Spatial_8C | Batch1 | right atrial appendage |
| GSM9746007 | Spatial_9A | Batch2 | right atrial appendage |
| GSM9746008 | Spatial_9B | Batch2 | right atrial appendage |
| GSM9746009 | Spatial_9C | Batch2 | right atrial appendage |
| GSM9746010 | Spatial_9D | Batch2 | right atrial appendage |

## 原始与处理数据下载

已下载并解包GEO补充处理文件：

- `GSE331446_RAW.tar`：180,715,520 bytes
- 内含6个样本tar包：
  - `GSM9746005_Sample_8A.tar.gz`：21,842,185 bytes
  - `GSM9746006_Sample_8C.tar.gz`：17,151,368 bytes
  - `GSM9746007_Sample_9A.tar.gz`：48,062,793 bytes
  - `GSM9746008_Sample_9B.tar.gz`：28,940,446 bytes
  - `GSM9746009_Sample_9C.tar.gz`：40,024,985 bytes
  - `GSM9746010_Sample_9D.tar.gz`：24,686,223 bytes

SRA原始reads也已核对，但未提交到仓库，因单个SRR约10-17 GB：

| SRX | SRR | SRA size bytes |
|---|---|---:|
| SRX33529334 | SRR38746338 | 10,329,541,502 |
| SRX33529335 | SRR38746337 | 13,382,142,733 |
| SRX33529336 | SRR38746336 | 15,611,641,303 |
| SRX33529337 | SRR38746335 | 13,354,436,995 |
| SRX33529338 | SRR38746334 | 16,827,116,661 |
| SRX33529339 | SRR38746333 | 14,306,224,440 |

复现处理文件下载和分析：

```bash
pip3 install --user -r requirements-gse331446.txt
python3 scripts/download_gse331446.py --data-dir data/GSE331446
python3 scripts/analyze_gse331446_spatial.py --data-dir data/GSE331446 --out-dir analysis/GSE331446
```

如需下载SRA原始reads，可用SRA Toolkit按SRR逐个执行，例如：

```bash
prefetch SRR38746338
fasterq-dump --split-files SRR38746338
```

## 补充文件格式和内容核对

实测文件完整性见`analysis/GSE331446/file_inventory.csv`。主要发现：

- `Sample_9A`包含完整的标准Space Ranger处理文件。
- `Sample_8A`可通过`filtered_feature_bc_matrix.h5`读取表达矩阵，但缺少标准`barcodes.tsv.gz/features.tsv.gz/matrix.mtx.gz`以及`tissue_positions.csv`，因此不能做坐标级定位。
- `Sample_8C`缺少`filtered_feature_bc_matrix.h5`、fiducial/detected tissue图和`web_summary.html`，但有完整mtx、坐标、scalefactors和SE文件，可分析表达与坐标。
- `Sample_9B`缺少`scalefactors_json.json`。
- `Sample_9C`缺少`tissue_lowres_image.png`。
- `Sample_9D`缺少`detected_tissue_image.jpg`。

GEO描述中的“processed files include filtered_feature_bc_matrix, filtered_feature_bc_matrix.h5, tissue images, spatial coordinates and Space Ranger outputs”在逐样本层面并非完全一致，因此分析脚本对mtx与h5做了回退读取。

## Space Ranger QC概览

输出：`analysis/GSE331446/space_ranger_qc_summary.csv`

| sample | matrix source | filtered spots | median genes/spot | genes detected |
|---|---|---:|---:|---:|
| Sample_8A | h5 | 2,873 | 808 | 14,967 |
| Sample_8C | matrix_market | 2,153 | 1,231 | 15,817 |
| Sample_9A | matrix_market | 3,383 | 2,062 | 17,612 |
| Sample_9B | matrix_market | 1,990 | 1,540 | 16,915 |
| Sample_9C | matrix_market | 2,956 | 1,917 | 15,785 |
| Sample_9D | matrix_market | 2,133 | 1,167 | 15,094 |

## SE（spatial enrichment）比较

输出：

- `analysis/GSE331446/spatial_enrichment_marker_comparison.csv`
- `analysis/GSE331446/spatial_enrichment_top_features.csv`

心肌标记（如`NPPA`, `MYH6`, `TNNI3`, `ACTC1`, `TNNT2`）在各样本的Moran's I整体较高，提示右心房切片中强空间结构化的心肌区域信号。例：

- `NPPA` Moran's I：8A 0.456、8C 0.783、9A 0.584、9B 0.710、9C 0.703、9D 0.590。

ANXA4和巨噬细胞标记：

- `ANXA4`空间富集在9C和9D达到显著：9C I=0.0292, adjusted p=1.05e-5；9D I=0.0228, adjusted p=0.0141。
- `ANXA4`在8A/8C/9A/9B的Moran's I不显著或接近零，提示ANXA4表达可检测但空间聚集性有限。
- 巨噬细胞补体标记`C1QB/C1QC`在8C、9A、9B、9C、9D更明显，尤其9C中`C1QB` I=0.139、`C1QC` I=0.123。

自律/起搏标记：

- `HCN4`在8C、9A、9B、9C有一定空间富集信号，但整体低于心肌结构标记。
- `SHOX2/TBX3`信号总体较弱，Visium spot层面只能作为代理提示，不能直接证明起搏细胞群。

## 心肌、自律、ANXA4高巨噬细胞样spot代理

输出：

- `analysis/GSE331446/marker_score_summary.csv`
- `analysis/GSE331446/spot_marker_proxy_summary.csv`
- `analysis/GSE331446/marker_gene_counts.csv`

使用的marker集合：

- 心肌细胞样：`TTN, MYH6, MYH7, TNNT2, TNNI3, ACTC1, MYL2, MYL7, MYBPC3, NPPA, NPPB`
- 自律/起搏样：`HCN4, SHOX2, TBX3, TBX18, ISL1, CACNA1D, CACNA1G, RYR2, GJA5, TBX5`
- ANXA4/巨噬细胞样：`ANXA4, CD68, LYZ, C1QA, C1QB, C1QC, CD14, FCGR3A, MSR1, MARCO, CD163, MRC1, IL1B, CCL2`

ANXA4高表达巨噬细胞样spot代理定义：同一样本内ANXA4 normalized score位于阳性spot的上四分位，同时巨噬细胞marker score位于阳性spot的上四分位。

| sample | ANXA4+ spots | ANXA4-high macrophage proxy spots |
|---|---:|---:|
| Sample_8A | 110 | 15 |
| Sample_8C | 255 | 39 |
| Sample_9A | 586 | 94 |
| Sample_9B | 217 | 33 |
| Sample_9C | 537 | 83 |
| Sample_9D | 248 | 45 |

解释限制：多数spot的最高marker score仍是心肌细胞样，这是右心房心肌切片和Visium多细胞spot的预期结果。巨噬细胞/ANXA4结果应作为空间区域富集代理，后续最好与单核RNA-seq或组织免疫染色联合验证。

## 时序分析判断

GSE331446元数据只有样本、batch、组织、技术等字段，没有明确时间点、SR/AF分组、病程阶段或有序纤维脂肪重塑分级。当前分析不执行真实时序/拟时序，避免把样本编号误作生物时间。

如后续获得：

- 每个样本的AF/SR或ACM阶段；
- 脂肪浸润/纤维化定量；
- 与单核RNA-seq匹配的细胞状态连续谱；

可在现有脚本基础上增加分组差异、空间邻域变化或以外部阶段变量排序的趋势分析。
