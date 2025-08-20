from rules.bumper import evaluate_bumper

def test_bumper_replace():
    lines = ["Remove front bumper cover"]
    result = evaluate_bumper(lines)
    assert "Consider replacing the front bumper if damage is extensive." in result

def test_bumper_repair():
    lines = ["Repair bumper fascia"]
    result = evaluate_bumper(lines)
    assert "Repair may be sufficient for minor bumper damage." in result

def test_deduplication():
    lines = ["Remove bumper", "Install bumper"]
    result = evaluate_bumper(lines)
    assert len(result) == 1