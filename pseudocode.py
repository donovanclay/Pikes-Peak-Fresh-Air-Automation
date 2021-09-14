INPUTS = [
    input1,
    input2,
    input3
]

WEIGHTS = [
    weight1,
    weight2,
    weight3
]

OUTPUTS = [
    out1,
    out2,
    out3
]

def poll() {
    main()
}

def main() {
    # int for CFM value
    CFM_required = 0

    # Update input values
    fetch_statuses()

    CFM_required = get_CFM()

    set_CFM(CFM_required)
}

def fetch_statuses() {
    # Get all new input values
    ## Do *NOT* rely on this code, the f-string for the for-loop probably won't work.
    for fan in INPUTS:
        fan = self.isy.cmd(f'nodes/FAN{fan}LEVEL/query')
}

def get_CFM() {
    total_CFM = 0
    for fan_level in INPUTS:
        total_CFM += weight * fan_level * constant                  # ...or something like that
}

def set_CFM(CFM_required) {
    for output in OUTPUTS:
        # Insteon switch level, assuming out of 100 (?)
        output = CFM_required / num(OUTPUTS) / weight * constant    # ...or something like that
}