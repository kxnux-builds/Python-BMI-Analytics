def generate_stats(history_data: list) -> dict:
    if not history_data:
        return {"total": 0, "avg_bmi": 0.0, "min_bmi": 0.0, "max_bmi": 0.0, "trend": "N/A"}

    bmis = [row[4] for row in history_data]
    total = len(bmis)
    avg_bmi = round(sum(bmis) / total, 1)

    if total > 1:
        diff = round(bmis[-1] - bmis[0], 1)
        if diff > 0: trend = f"↗ Increasing (+{diff})"
        elif diff < 0: trend = f"↘ Decreasing ({diff})"
        else: trend = "→ Stable"
    else:
        trend = "Need more data"

    return {"total": total, "avg_bmi": avg_bmi, "min_bmi": min(bmis), "max_bmi": max(bmis), "trend": trend}