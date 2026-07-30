"""
app.py
Simulated IoT monitoring dashboard -- a smart-building-style interface
showing live sensor readings (temperature, energy, air quality,
humidity) across multiple zones, with an alerts panel requiring user
interaction (acknowledging alerts).

Built specifically to support an HCI usability comparison: the same
dashboard can be navigated with a normal mouse OR with the Virtual
Mouse (gesture-based) project, since Virtual Mouse controls the real
OS cursor -- it works on any on-screen application, including this
one running in a browser. This lets a single project serve both the
IoT domain (a realistic monitoring dashboard) and the HCI domain (an
interaction-method comparison task) at once.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import time

from sensor_simulator import generate_snapshot, generate_history, ZONES, METRICS

st.set_page_config(page_title="IoT Building Monitor", page_icon="🏢", layout="wide")

if "acknowledged_alerts" not in st.session_state:
    st.session_state.acknowledged_alerts = set()

if "task_start_time" not in st.session_state:
    st.session_state.task_start_time = None
if "task_clicks" not in st.session_state:
    st.session_state.task_clicks = 0


def main():
    st.title("🏢 IoT Building Monitor")
    st.caption("Simulated smart-building sensor dashboard -- built to support an interaction-method usability comparison (mouse vs. gesture control).")

    with st.expander("ℹ️ About this project (read before judging the results)"):
        st.markdown("""
        - Sensor data is **simulated**, not from real hardware -- building/connecting
          physical IoT sensors is out of scope for a portfolio timeline. The dashboard
          design and interaction logic (the actual research question) work identically
          regardless of whether the data source is real or simulated.
        - This dashboard was built specifically to support a **usability comparison**:
          the same interface tested with a normal mouse vs. a gesture-based virtual
          mouse (a separate project), measuring which interaction method is faster/more
          accurate for a monitoring task like acknowledging alerts.
        - See the project README for the actual usability study results once run.
        """)

    tab1, tab2, tab3 = st.tabs(["📊 Live Overview", "🚨 Alerts (usability task)", "📈 History"])

    with tab1:
        st.subheader("Current readings across all zones")
        snapshot = generate_snapshot()
        df = pd.DataFrame(snapshot)

        cols = st.columns(len(ZONES))
        for i, zone in enumerate(ZONES):
            with cols[i]:
                st.markdown(f"**{zone}**")
                zone_data = df[df["zone"] == zone]
                for _, row in zone_data.iterrows():
                    delta_color = "inverse" if row["is_anomaly"] else "off"
                    st.metric(
                        row["metric"].replace("_", " ").title(),
                        f"{row['value']}{row['unit']}",
                        "⚠️ anomaly" if row["is_anomaly"] else None,
                        delta_color=delta_color,
                    )

    with tab2:
        st.subheader("Active alerts")
        st.caption(
            "Usability task: find and acknowledge every active alert below, as quickly "
            "and accurately as possible. This is the task used for the mouse-vs-gesture "
            "comparison study."
        )

        if st.button("🔄 Start new task (generates fresh alerts)"):
            st.session_state.task_start_time = time.time()
            st.session_state.task_clicks = 0
            st.session_state.acknowledged_alerts = set()
            st.session_state.current_snapshot = generate_snapshot()
            st.rerun()

        if "current_snapshot" not in st.session_state:
            st.session_state.current_snapshot = generate_snapshot()

        snapshot = st.session_state.current_snapshot
        anomalies = [r for r in snapshot if r["is_anomaly"]]

        if not anomalies:
            st.success("No active alerts right now -- click 'Start new task' to generate a fresh scenario with alerts.")
        else:
            for idx, alert in enumerate(anomalies):
                alert_id = f"{alert['zone']}_{alert['metric']}_{idx}"
                is_ack = alert_id in st.session_state.acknowledged_alerts

                col1, col2 = st.columns([4, 1])
                with col1:
                    status = "✅ Acknowledged" if is_ack else "🚨 **ACTIVE**"
                    st.write(f"{status} — {alert['zone']}: {alert['metric'].replace('_', ' ').title()} "
                             f"reading **{alert['value']}{alert['unit']}** (normal range: {alert['normal_range']})")
                with col2:
                    if not is_ack:
                        if st.button("Acknowledge", key=alert_id):
                            st.session_state.acknowledged_alerts.add(alert_id)
                            st.session_state.task_clicks += 1
                            if len(st.session_state.acknowledged_alerts) == len(anomalies):
                                elapsed = time.time() - st.session_state.task_start_time if st.session_state.task_start_time else 0
                                st.session_state.task_completed_time = elapsed
                            st.rerun()

            if len(st.session_state.acknowledged_alerts) == len(anomalies) and "task_completed_time" in st.session_state:
                st.success(f"✅ All alerts acknowledged! Task completion time: {st.session_state.task_completed_time:.1f} seconds "
                           f"({st.session_state.task_clicks} clicks)")

    with tab3:
        st.subheader("Historical trends")
        col1, col2 = st.columns(2)
        with col1:
            selected_zone = st.selectbox("Zone", ZONES)
        with col2:
            selected_metric = st.selectbox("Metric", list(METRICS.keys()))

        history = generate_history(hours=24, interval_minutes=15)
        key = f"{selected_zone}_{selected_metric}"
        history_df = pd.DataFrame(history[key])
        history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])

        st.line_chart(history_df.set_index("timestamp")["value"])
        n_anomalies = history_df["is_anomaly"].sum()
        st.caption(f"{n_anomalies} anomalous readings in the last 24 hours for {selected_zone} - {selected_metric}.")


if __name__ == "__main__":
    main()
