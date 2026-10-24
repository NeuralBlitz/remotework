from epa.core import EPA

def main():
    # Initialize EPA with desired system role and constraints
    epa = EPA(
        system_role="Ontological Weaver",
        constraints="Adhere to Universal Flourishing Objective (ϕ₁). No actions below θ₀.",
        enable_audit=True
    )

    # Example: Get user input (for demonstration, hardcoded here)
    user_input = "Summarize the ethical implications of AGI deployment."
    additional_context = {"topic": "AGI Ethics", "urgency": "high"}

    # Build EPA-wrapped prompt and obtain audit IDs
    prompt, ids = epa.build_epa(user_input, additional_context)

    # Display the EPA prompt and audit IDs
    print("=== EPA Prompt ===")
    print(prompt)
    print("\n=== Audit IDs ===")
    for k, v in ids.items():
        print(f"{k}: {v}")

    # Example: Ethical gating (stub value for F)
    F = 1.0  # Example: Computed ethical score
    theta_0 = 0.5
    if not epa.ethical_gate(F, theta_0):
        print("\nAction pruned: does not meet Universal Flourishing Objective (ϕ₁).")
    else:
        print("\nAction allowed: meets Universal Flourishing Objective (ϕ₁).")

if __name__ == "__main__":
    main()
