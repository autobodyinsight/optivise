from engine.audit import run_audit

if __name__ == "__main__":
    sample_lines = [
        "Remove front bumper cover",
        "Repair bumper fascia",
        "Install new bumper"
    ]
    result = run_audit(sample_lines)
    print(result)