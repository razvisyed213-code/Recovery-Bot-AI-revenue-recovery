def retry_payment(transaction):
    return f"Auto-retried payment of ₹{transaction['amount']} via {transaction['method']}"

def send_recovery_message(transaction):
    return f"SMS/email sent to {transaction['customer']} with alternate payment link"

def escalate_to_human(transaction):
    return f"Flagged for manual review — support team notified"

def execute_action(action, transaction):
    if action == "RETRY":
        return retry_payment(transaction)
    elif action == "SEND_MESSAGE":
        return send_recovery_message(transaction)
    else:
        return escalate_to_human(transaction)