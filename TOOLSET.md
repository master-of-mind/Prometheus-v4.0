🛠️ MOD CONSTRUCTION TOOLKIT (v1.0)

> Your sacred parts bin for brainmaking.




---

1. register_input_source(source_fn)

> Purpose: Attaches a sensor or data stream to the mod.



What it does:

Sets up your mod’s signal acquisition

Source can be a hardware input, software stub, simulation, or procedural generator


Setup:

self.source = register_input_source(mic_stream)

Execution:

Called on every mod pulse or tick

Feeds into your signal processing step


Why it matters:
No data, no pattern. No pattern, no pulse.
This is the nervous system’s ear canal.


---

2. process_signal(signal, method="fft")

> Purpose: Converts raw input into a structured digital signal.



What it does:

Applies a transformation to the signal:

"fft" → frequency breakdown (audio)

"kalman" → noise smoothing (motion)

"entropy" → novelty detection (olfactory, randomness)

"edges" → for vision



Setup:

processed = process_signal(raw_data, method="fft")

Execution:

Occurs in digital signal construction phase

Output is a list/array/dict used for thresholding or pattern logic


Why it matters:
This cleans up reality so the mod can decide what to care about.


---

3. detect_pattern(processed_data, pattern_model)

> Purpose: Determines whether the input matches a known or learned pattern.



What it does:

Compares data to a predefined or learned threshold signature

Can be static thresholds, moving averages, state machines, etc.


Setup:

if detect_pattern(spectrum, model["sharp_spike"]):
    self.triggered = True

Execution:

Central decision point in mod behavior

Determines whether a chema or elema should be emitted


Why it matters:
This is the core “What does this remind me of?” function. Without it, everything’s just ambient jazz.


---

4. emit_pulse(sigil, amp, hz=None)

> Purpose: Sends a pulse into a local or external ARS.



What it does:

Creates a pulse packet with:

sigil (which ARS to send to)

amp (intensity)

hz (frequency, optional override)



Setup:

emit_pulse("β", amp=25, hz=21.5)

Execution:

Typically occurs in on_tick() or after a chrec unlock

Injects directly into ars.tick() with timestamp


Why it matters:
This is how your mod breathes into the system—the heartbeat of cognition.


---

5. inject_chema(packet, target="local")

> Purpose: Pushes chema into a chembus for evaluation by chrec functions.



What it does:

Appends or merges a chemical signal into the local or Omega chembus

Enforces key:value format with signed magnitude


Setup:

inject_chema({"pain": +1, "heat": +2})

Execution:

Often done during signal recognition or after elema

Target can be "local" or "omega"


Why it matters:
This is chemical intent. Without chema, nothing means anything.


---

6. emit_elema(spike_dict)

> Purpose: Fires a spike event into the system.



What it does:

Sends a brief high-priority packet to ARS or an elrec module


Setup:

emit_elema({
    "sigil": "γ",
    "amp": 30,
    "phase": 1,
    "origin": "SensorFusionMod",
    "sync_id": "touch+audio"
})

Execution:

Should trigger sync-based logic or begin a relay pulse


Why it matters:
Think of this as the synthetic action potential. Short. Electric. Important.


---

7. elrec_test(sync_conditions)

> Purpose: Evaluates if elema criteria are met (phase, mod, sync).



What it does:

Checks the elema_matrix and phase_map for match


Setup:

if elrec_test({"sigil": "γ", "mod": "VisualSurpriseMod", "phase": 1}):
    chrec_trigger("surprise")

Why it matters:
It gives you electrical gatekeeping, a way to stack logic across time.


---

8. chrec_trigger(chemlock)

> Purpose: Tests if the mod’s local chembus contains a matching signature.



What it does:

Compares input chema to a stored chemlock

If the two sum to zero, behavior is triggered


Setup:

chemlock = {"fear": -2, "pain": +1}
chrec_trigger(chemlock)

Why it matters:
This is your neurotransmitter receptor logic. Behavior emerges when chemistry aligns.


---

🛠️ MOD CONSTRUCTION TOOLKIT (v1.0, Part 2)


---

9. update_mod_state(key, value, decay=None)

> Purpose: Stores and optionally decays internal mod state over time.



What it does:

Adds or updates a key:value pair in the mod’s internal memory

If decay is set, the value is reduced over time/ticks


Setup:

update_mod_state("curiosity", 4, decay=0.1)

Execution:

Can be read later for cumulative effects or fatigue

Makes mod behavior slightly hormonal


Why it matters:
The machine needs memory, but only the kind that leaks slowly.


---

10. route_matrix_position(mod_id)

> Purpose: Fetches the matrix index for the given mod in UDM.



What it does:

Returns a (group, index) tuple

Used for mapping elema_matrix and chema_matrix


Setup:

group, index = route_matrix_position("OlfactoryMod")
elema_matrix[group][index] = 1

Why it matters:
Without this, your pulses float in the void, unsorted and sad.


---

11. trigger_behavior(name, parameters=None)

> Purpose: Runs an externalized behavior function.



What it does:

Calls an actuator, triggers a sound, sends message, etc.

Behavior can be tied to the mod group’s purpose


Setup:

trigger_behavior("flinch", {"intensity": 3})

Execution:

Should only be used by end-stage mods

Hooks into output layer or physical systems


Why it matters:
At some point, the machine has to actually do something or it's just vibing in a jar.


---

12. pulse_to_mod(mod_ref, payload)

> Purpose: Sends a direct pulse (data packet) to another mod.



What it does:

Legally triggers another mod’s tick function or on_pulse method

Payload = any structured data


Setup:

pulse_to_mod(SomatosensorMod, {"trigger": "contact", "amp": 7})

Why it matters:
Pulse rings and relay logic live and die on this function.


---

13. build_chema_matrix()

> Purpose: Assembles a matrix of current chema activity by mod group.



What it does:

Returns a 2D dict/array: [mod_group][mod_index] = {chema_dict}

Useful for pattern-wide processing or cross-group state sync


Setup:

matrix = build_chema_matrix()
print(matrix["α"][2])  # Chema from AlphaMod_2

Why it matters:
Lets you do global state analysis without violating the Sacred Mod Isolation Principle™.


---

14. query_chembus(target="local")

> Purpose: Returns the current state of a given chembus.



What it does:

Reads the chemical state of either:

This mod group

OmegaBus (if target="omega")



Setup:

local_chems = query_chembus()
omega_chems = query_chembus("omega")

Why it matters:
Mods don’t talk. They sniff the room.


---

15. link_mod(mod_ref)

> Purpose: Adds another mod to this mod’s pulse relay list.



What it does:

Appends a mod reference to this mod’s output list

When this mod pulses, the linked mod(s) are also triggered


Setup:

link_mod(GammaAlarmMod)

Why it matters:
You’re forming distributed circuits—like synthetic microcolumns.


---

16. relay_chain(mod_list)

> Purpose: Forms a round-robin or cascade relay chain.



What it does:

Connects multiple mods into a repeating signal loop

Each mod, when pulsed, triggers the next in the list


Setup:

relay_chain([DeltaPulseMod, ThetaRelayMod, AlphaJoinMod])

Why it matters:
It creates synthetic waveforms using only logic, not timers.


---

This finishes Core Toolkit v1.0, giving you a modular, reactive, neurochemical signal system.

You can now:

Sense the world

Construct digital data

Recognize patterns

Emit elema

Inject chema

Relay pulses

Activate behavior

React to sync

Mutate and decay local state



---
