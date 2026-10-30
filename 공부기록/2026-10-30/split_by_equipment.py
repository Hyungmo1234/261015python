"""data.csv를 장비별로 나눠, 정상(검정) + 이상(유형별 색) 센서 그래프를 그립니다.

- 주요 센서(SENSOR_COLUMNS)에 결측이 있는 행은 산점도에서 제외
- sensor_malfunction 이상 건은 제외
- operating_mode != normal 구간은 센서 그래프 배경색으로 표시
"""

from pathlib import Path
import csv
from collections import defaultdict, Counter
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# 원본 데이터 / 그래프 저장 경로
INPUT_FILE = Path("data.csv")
OUTPUT_DIR = Path("anomaly_plots")

# 시계열로 볼 주요 센서 컬럼
SENSOR_COLUMNS = [
    "temperature_c",
    "vibration_mm_s",
    "pressure_kpa",
    "motor_rpm",
    "power_consumption_kw",
]

# operating_mode 배경색 (normal은 배경 없음)
MODE_COLORS = {
    "high_load": "#ffcccc",  # 연한 빨강
    "idle": "#d9d9d9",  # 회색
    "cooldown": "#cce5ff",  # 연한 파랑
    "startup": "#fff2cc",  # 연한 노랑
}
MODE_BG_ALPHA = 0.45

# 그래프에서 제외할 이상 유형
EXCLUDED_ANOMALY_TYPES = {"sensor_malfunction"}


def _to_float(value: str | None) -> float | None:
    """문자열 → float. 결측/변환 실패 시 None."""
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_time(row: dict) -> datetime:
    try:
        return datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
    except (KeyError, ValueError):
        return datetime.min


def _has_missing_sensors(row: dict) -> bool:
    """주요 센서 컬럼 중 하나라도 결측이면 True."""
    return any(_to_float(row.get(col)) is None for col in SENSOR_COLUMNS)


def _mode_segments(
    timeline: list[tuple[datetime, str]],
) -> list[tuple[datetime, datetime, str]]:
    """(시간, mode) 시계열 → 연속 구간 [start, end) 리스트."""
    if not timeline:
        return []
    timeline = sorted(timeline, key=lambda x: x[0])
    segments: list[tuple[datetime, datetime, str]] = []
    start_t, prev_mode = timeline[0]
    for t, mode in timeline[1:]:
        if mode != prev_mode:
            segments.append((start_t, t, prev_mode))
            start_t, prev_mode = t, mode
    # 마지막 구간: 마지막 샘플 + 1분까지
    end_t = timeline[-1][0] + timedelta(minutes=1)
    segments.append((start_t, end_t, prev_mode))
    return segments


def load_by_equipment(
    input_file: Path = INPUT_FILE,
) -> tuple[
    dict[str, list[dict]],
    dict[str, list[dict]],
    dict[str, list[tuple[datetime, datetime, str]]],
    int,
]:
    """장비별 정상/이상 행 + operating_mode 구간을 반환. 센서 결측 행은 산점도에서 제외."""
    normals: dict[str, list[dict]] = defaultdict(list)
    anomalies: dict[str, list[dict]] = defaultdict(list)
    mode_timelines: dict[str, list[tuple[datetime, str]]] = defaultdict(list)
    dropped = 0

    with input_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "is_anomaly" not in reader.fieldnames:
            raise ValueError("CSV에 is_anomaly 컬럼이 없습니다.")

        for row in reader:
            eq_id = row["equipment_id"]
            mode = (row.get("operating_mode") or "unknown").strip() or "unknown"
            mode_timelines[eq_id].append((_parse_time(row), mode))

            if _has_missing_sensors(row):
                dropped += 1
                continue
            if row.get("is_anomaly", "").strip() == "1":
                atype = (row.get("anomaly_type") or "").strip()
                if atype in EXCLUDED_ANOMALY_TYPES:
                    continue  # 센서 고장 등은 그래프에서 제외
                anomalies[eq_id].append(row)
            else:
                normals[eq_id].append(row)

    for groups in (normals, anomalies):
        for rows in groups.values():
            rows.sort(key=lambda r: r.get("timestamp", ""))

    mode_segs = {
        eq_id: _mode_segments(tl) for eq_id, tl in sorted(mode_timelines.items())
    }
    eq_ids = sorted(set(normals) | set(anomalies) | set(mode_segs))
    return (
        {k: normals[k] for k in eq_ids},
        {k: anomalies[k] for k in eq_ids},
        {k: mode_segs.get(k, []) for k in eq_ids},
        dropped,
    )


def _scatter_series(
    ax,
    rows: list[dict],
    col: str,
    *,
    color,
    s: float,
    alpha: float,
    zorder: int,
) -> None:
    xs, ys = [], []
    for r in rows:
        y = _to_float(r.get(col))
        if y is None:
            continue
        xs.append(_parse_time(r))
        ys.append(y)
    if xs:
        ax.scatter(xs, ys, c=color, s=s, alpha=alpha, zorder=zorder, linewidths=0)


def _paint_mode_background(
    ax,
    segments: list[tuple[datetime, datetime, str]],
) -> None:
    """non-normal operating_mode 구간에 배경색을 칠한다."""
    for start, end, mode in segments:
        color = MODE_COLORS.get(mode)
        if color is None:
            continue  # normal 등은 배경 없음
        ax.axvspan(start, end, facecolor=color, alpha=MODE_BG_ALPHA, zorder=0, lw=0)


def plot_equipment(
    eq_id: str,
    normal_rows: list[dict],
    anomaly_rows: list[dict],
    mode_segments: list[tuple[datetime, datetime, str]],
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """한 장비의 정상/이상 산점도 + operating_mode 배경을 PNG로 저장한다."""
    output_dir.mkdir(parents=True, exist_ok=True)

    type_counts = Counter(r.get("anomaly_type", "unknown") for r in anomaly_rows)
    type_list = sorted(type_counts.keys())
    color_map = {t: f"C{i}" for i, t in enumerate(type_list)}

    used_modes = sorted(
        {m for _, _, m in mode_segments if m in MODE_COLORS},
        key=lambda m: list(MODE_COLORS).index(m) if m in MODE_COLORS else 99,
    )

    n_sensors = len(SENSOR_COLUMNS)
    fig, axes = plt.subplots(
        n_sensors + 1,
        1,
        figsize=(12, 2.4 * (n_sensors + 1)),
        constrained_layout=True,
    )
    fig.suptitle(
        f"{eq_id}  |  normal={len(normal_rows):,}  anomaly={len(anomaly_rows):,}",
        fontsize=14,
    )

    # 1) 이상 유형 막대
    ax0 = axes[0]
    if type_list:
        labels = list(type_counts.keys())
        values = [type_counts[k] for k in labels]
        bars = ax0.bar(labels, values, color=[color_map[k] for k in labels])
        for bar, v in zip(bars, values):
            ax0.text(
                bar.get_x() + bar.get_width() / 2,
                v,
                str(v),
                ha="center",
                va="bottom",
                fontsize=9,
            )
    ax0.set_ylabel("count")
    ax0.set_title("anomaly_type counts")
    ax0.tick_params(axis="x", rotation=15)

    # 2) 센서별 시계열
    anomalies_by_type: dict[str, list[dict]] = defaultdict(list)
    for r in anomaly_rows:
        anomalies_by_type[r.get("anomaly_type", "unknown")].append(r)

    for ax, col in zip(axes[1:], SENSOR_COLUMNS):
        _paint_mode_background(ax, mode_segments)
        _scatter_series(
            ax, normal_rows, col, color="black", s=6, alpha=0.25, zorder=1
        )
        for t in type_list:
            _scatter_series(
                ax,
                anomalies_by_type[t],
                col,
                color=color_map[t],
                s=14,
                alpha=0.85,
                zorder=2,
            )
        ax.set_ylabel(col)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("timestamp")

    point_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="black",
            markersize=7,
            label="normal (is_anomaly=0)",
        )
    ] + [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color_map[t],
            markersize=8,
            label=t,
        )
        for t in type_list
    ]
    leg1 = axes[1].legend(
        handles=point_handles, loc="upper right", fontsize=8, title="point"
    )
    axes[1].add_artist(leg1)

    if used_modes:
        mode_handles = [
            Patch(facecolor=MODE_COLORS[m], alpha=MODE_BG_ALPHA, label=m)
            for m in used_modes
        ]
        axes[2].legend(
            handles=mode_handles,
            loc="upper right",
            fontsize=8,
            title="operating_mode",
        )

    out_path = output_dir / f"{eq_id}_anomalies.png"
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    return out_path


def plot_all(
    normals: dict[str, list[dict]],
    anomalies: dict[str, list[dict]],
    mode_segments: dict[str, list[tuple[datetime, datetime, str]]],
) -> list[Path]:
    """모든 장비에 대해 그래프를 생성한다."""
    paths = []
    for eq_id in sorted(set(normals) | set(anomalies) | set(mode_segments)):
        path = plot_equipment(
            eq_id,
            normals.get(eq_id, []),
            anomalies.get(eq_id, []),
            mode_segments.get(eq_id, []),
        )
        paths.append(path)
    return paths


if __name__ == "__main__":
    normals, anomalies, mode_segments, dropped = load_by_equipment()

    print(f"결측 행 제외: {dropped:,}건")
    print("장비별 건수 (normal / anomaly)")
    for eq_id in sorted(set(normals) | set(anomalies)):
        n = len(normals.get(eq_id, []))
        a = len(anomalies.get(eq_id, []))
        modes = Counter(m for _, _, m in mode_segments.get(eq_id, []))
        non_normal = {k: v for k, v in modes.items() if k != "normal"}
        print(f"  {eq_id}: {n:,} / {a:,}  | mode구간={dict(non_normal)}")

    paths = plot_all(normals, anomalies, mode_segments)
    print(f"\n그래프 저장 위치: {OUTPUT_DIR.resolve()}")
    for p in paths:
        print(f"  {p.name}")
