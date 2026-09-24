import csv
import io
import math
from signals.models import Signal
from traces.models import Trace


def parse_csv_data(dataset):

    dataset.file.seek(0)
    decoded_file = dataset.file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    rows = []
    for row in reader:
        converted_row = {}
        for k, v in row.items():
            clean_key = k.strip()
            try:
                converted_row[clean_key] = float(v.strip())
            except (ValueError, TypeError):
                converted_row[clean_key] = v.strip()
        rows.append(converted_row)
    dataset.file.seek(0)
    return rows


def calculate_pearson_correlation(x_vals, y_vals):

    n = len(x_vals)
    if n != len(y_vals) or n < 2:
        return 0.0

    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n

    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    denom_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_vals))
    denom_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_vals))

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return round(numerator / (denom_x * denom_y), 2)


def analyze_dataset_file(dataset):

    rows = parse_csv_data(dataset)
    if not rows:
        return {}

    all_keys = list(rows[0].keys())
    numerical_cols = []
    categorical_cols = []

    for key in all_keys:
        if isinstance(rows[0].get(key), (int, float)):
            numerical_cols.append(key)
        else:
            categorical_cols.append(key)

    metrics_summary = {}
    for col in numerical_cols:
        vals = [r[col] for r in rows if isinstance(r.get(col), (int, float))]
        if vals:
            count = len(vals)
            avg = sum(vals) / count
            variance = sum((x - avg) ** 2 for x in vals) / (count - 1) if count > 1 else 0
            std_dev = math.sqrt(variance)

            metrics_summary[col] = {
                "mean": round(avg, 2),
                "std": round(std_dev, 2),
                "min": round(min(vals), 2),
                "max": round(max(vals), 2),
                "count": count
            }

    dataset.rows = len(rows)
    dataset.columns = len(all_keys)
    dataset.summary_stats = {
        "total_rows": dataset.rows,
        "total_columns": dataset.columns,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "metrics_summary": metrics_summary,
    }
    dataset.save()
    return dataset.summary_stats


def auto_detect_signals_from_dataset(dataset):

    rows = parse_csv_data(dataset)
    if not rows:
        return []

    numerical_cols = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
    created_signals = []

    baselines = {
        "attendance": 80.0,
        "assignment_completion": 75.0,
        "final_score": 70.0,
        "study_hours": 5.0,
    }

    for col in numerical_cols:
        col_lower = col.lower()
        baseline_val = None
        for base_key, b_val in baselines.items():
            if base_key in col_lower:
                baseline_val = b_val
                break

        if baseline_val:
            vals = [r[col] for r in rows if isinstance(r.get(col), (int, float))]
            if not vals:
                continue

            current_avg = round(sum(vals) / len(vals), 2)
            diff_pct = round(((current_avg - baseline_val) / baseline_val) * 100, 2)

            if diff_pct <= -5.0:
                severity = 'CRITICAL' if abs(diff_pct) >= 25 else ('HIGH' if abs(diff_pct) >= 15 else 'MEDIUM')
                signal = Signal.objects.create(
                    project=dataset.project,
                    dataset=dataset,
                    metric=f"Low Average {col.replace('_', ' ').title()}",
                    previous_value=baseline_val,
                    current_value=current_avg,
                    severity=severity,
                    status='ACTIVE'
                )

                other_cols = [c for c in numerical_cols if c != col]
                correlations = []
                for other in other_cols:
                    other_vals = [r[other] for r in rows if isinstance(r.get(other), (int, float))]
                    r_score = calculate_pearson_correlation(vals, other_vals)
                    correlations.append((other, r_score, abs(r_score)))

                # Pick top 3 correlated factors
                correlations.sort(key=lambda item: item[2], reverse=True)
                for factor_col, raw_corr, abs_score in correlations[:3]:
                    direction = "positively associated" if raw_corr > 0 else "negatively associated"
                    Trace.objects.create(
                        signal=signal,
                        factor=factor_col.replace('_', ' ').title(),
                        importance_score=abs_score,
                        explanation=f"{factor_col} is strongly {direction} (r = {raw_corr}) with {col}."
                    )

                created_signals.append({
                    "signal_id": signal.id,
                    "metric": signal.metric,
                    "baseline": signal.previous_value,
                    "dataset_average": signal.current_value,
                    "change_percentage": signal.change_percentage,
                    "severity": signal.severity,
                    "root_causes_discovered": signal.traces.count()
                })

    return created_signals