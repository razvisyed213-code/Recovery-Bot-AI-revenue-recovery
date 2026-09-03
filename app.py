import streamlit as st
import pandas as pd
import time
from mock_data import transactions
from agent import decide_action
from actions import execute_action

st.set_page_config(page_title="RecoveryBot", layout="wide")
st.title("🔁 RecoveryBot — AI Revenue Recovery Agent")

if "results_df" not in st.session_state:
    st.session_state.results_df = None
    st.session_state.total_recovered = 0
    st.session_state.total_escalated_amount = 0
    st.session_state.recovered_count = 0
    st.session_state.escalated_count = 0
    st.session_state.total_txns = 0

if st.button("▶ Run Agent on Failed Transactions"):
    total_recovered = 0
    total_escalated_amount = 0
    recovered_count = 0
    escalated_count = 0
    rows = []
    demo_transactions = transactions[:15]

    with st.spinner("Agent analyzing failed transactions..."):
        for txn in demo_transactions:
            action, reason = decide_action(txn)
            result = execute_action(action, txn)

            if action in ["RETRY", "SEND_MESSAGE"]:
                total_recovered += txn["amount"]
                recovered_count += 1
            else:
                total_escalated_amount += txn["amount"]
                escalated_count += 1

            rows.append({
                "Transaction": txn["id"],
                "Customer": txn["customer"],
                "Amount": f"₹{txn['amount']}",
                "AmountValue": txn["amount"],
                "Method": txn["method"],
                "Failure Reason": txn["reason"],
                "Agent Decision": action,
                "Reasoning": reason,
                "Action Taken": result
            })
            time.sleep(2)

    st.session_state.results_df = pd.DataFrame(rows)
    st.session_state.total_recovered = total_recovered
    st.session_state.total_escalated_amount = total_escalated_amount
    st.session_state.recovered_count = recovered_count
    st.session_state.escalated_count = escalated_count
    st.session_state.total_txns = len(demo_transactions)

# ---------- DISPLAY RESULTS (persists across reruns) ----------
if st.session_state.results_df is not None:
    df = st.session_state.results_df
    total_txns = st.session_state.total_txns
    recovery_rate = (st.session_state.recovered_count / total_txns) * 100 if total_txns else 0

    st.subheader("📊 Recovery Rate Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", total_txns)
    col2.metric("Recovery Rate", f"{recovery_rate:.1f}%")
    col3.metric("💰 Total Recovered", f"₹{st.session_state.total_recovered:,}")
    col4.metric("🚩 Escalated", f"{st.session_state.escalated_count} (₹{st.session_state.total_escalated_amount:,})")

    st.progress(recovery_rate / 100)
    st.caption(f"{st.session_state.recovered_count} of {total_txns} transactions successfully recovered")

    st.subheader("📈 Failure Reason Breakdown")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.caption("Count of transactions by failure reason")
        reason_counts = df.groupby("Failure Reason").size()
        st.bar_chart(reason_counts)

    with chart_col2:
        st.caption("Recovered amount (₹) by payment method")
        recovered_df = df[df["Agent Decision"].isin(["RETRY", "SEND_MESSAGE"])]
        method_amounts = recovered_df.groupby("Method")["AmountValue"].sum()
        st.bar_chart(method_amounts)

    st.subheader("📋 Transaction Details")
    display_df = df.drop(columns=["AmountValue", "Method"])

    def highlight_failed(row):
        if row["Agent Decision"] == "ESCALATE":
            return ["color: red; font-weight: bold;"] * len(row)
        return ["color: green;"] * len(row)

    styled_df = display_df.style.apply(highlight_failed, axis=1)
    st.dataframe(styled_df, use_container_width=True)

    st.subheader("🔍 View Single Transaction")
    selected_id = st.selectbox("Select a Transaction ID", display_df["Transaction"].tolist())
    txn_detail = display_df[display_df["Transaction"] == selected_id].iloc[0]

    if txn_detail["Agent Decision"] == "ESCALATE":
        st.error(f"🚩 {selected_id} — Escalated to Human Review")
    else:
        st.success(f"✅ {selected_id} — Successfully Recovered")

    d1, d2 = st.columns(2)
    with d1:
        st.write(f"**Customer:** {txn_detail['Customer']}")
        st.write(f"**Amount:** {txn_detail['Amount']}")
        st.write(f"**Failure Reason:** {txn_detail['Failure Reason']}")
    with d2:
        st.write(f"**Agent Decision:** {txn_detail['Agent Decision']}")
        st.write(f"**Action Taken:** {txn_detail['Action Taken']}")

    st.write(f"**Full AI Reasoning:** {txn_detail['Reasoning']}")