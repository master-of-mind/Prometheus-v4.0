# elrec.py

def elrec_match(elema, template, tolerance=0):
    """
    Matches if elema values meet or exceed the template values within a tolerance.
    """
    for k, required in template.items():
        actual = elema.get(k)
        if actual < required - tolerance:
            return False
    return True

def elrec_strength(elema):
    """
    Returns the total summed strength of all sigils in the elema.
    """
    return sum(elema.values.values())

def elrec_dominant(elema):
    """
    Returns the sigil with the strongest pulse in the elema.
    """
    strongest = max(elema.values.items(), key=lambda x: x[1])
    return strongest[0] if strongest[1] > 0 else None

def elrec_synchronized(elema_list, required_sigil, threshold=3):
    """
    Checks for synchronized pulses on a single sigil across multiple elema objects.
    """
    count = 0
    for e in elema_list:
        if e.get(required_sigil) > 0:
            count += 1
    return count >= threshold
