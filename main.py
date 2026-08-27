# ==================================================
# OPTICAL FIBER LINK BUDGET ANALYZER
# ==================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ==================================================
# RESULTS DIRECTORY
# ==================================================

RESULTS_DIR = (
    Path(__file__).resolve().parent.parent / "results"
)

RESULTS_DIR.mkdir(exist_ok=True)


# ==================================================
# USER INPUT FUNCTION
# ==================================================

def get_float_input(message, default_value):
    """
    Get a numerical input from the user.
    Press Enter to use the default value.
    """

    user_input = input(
        f"{message} [{default_value}]: "
    ).strip()

    if user_input == "":
        return float(default_value)

    try:
        return float(user_input)

    except ValueError:
        print(
            f"Invalid input. Using default value: "
            f"{default_value}"
        )

        return float(default_value)


# ==================================================
# GET LINK PARAMETERS
# ==================================================

def get_link_parameters():

    print("\n" + "=" * 55)
    print("OPTICAL FIBER LINK BUDGET ANALYZER")
    print("=" * 55)

    print("\nEnter optical link parameters.")
    print("Press Enter to use the default value.\n")

    parameters = {}

    parameters["P_tx_dbm"] = get_float_input(
        "Transmitter Power (dBm)",
        0.0
    )

    parameters["fiber_length_km"] = get_float_input(
        "Fiber Length (km)",
        50.0
    )

    parameters["fiber_attenuation_db_per_km"] = (
        get_float_input(
            "Fiber Attenuation (dB/km)",
            0.2
        )
    )

    parameters["num_connectors"] = int(
        get_float_input(
            "Number of Connectors",
            4
        )
    )

    parameters["connector_loss_db"] = get_float_input(
        "Loss per Connector (dB)",
        0.5
    )

    parameters["num_splices"] = int(
        get_float_input(
            "Number of Splices",
            10
        )
    )

    parameters["splice_loss_db"] = get_float_input(
        "Loss per Splice (dB)",
        0.1
    )

    parameters["amplifier_gain_db"] = get_float_input(
        "Optical Amplifier Gain (dB)",
        0.0
    )

    parameters["receiver_sensitivity_dbm"] = (
        get_float_input(
            "Receiver Sensitivity (dBm)",
            -20.0
        )
    )

    parameters["system_margin_db"] = get_float_input(
        "Required System Margin (dB)",
        3.0
    )

    return parameters


# ==================================================
# CALCULATE LINK LOSSES
# ==================================================

def calculate_losses(parameters):

    fiber_loss_db = (
        parameters["fiber_length_km"]
        * parameters["fiber_attenuation_db_per_km"]
    )

    connector_loss_total_db = (
        parameters["num_connectors"]
        * parameters["connector_loss_db"]
    )

    splice_loss_total_db = (
        parameters["num_splices"]
        * parameters["splice_loss_db"]
    )

    total_link_loss_db = (
        fiber_loss_db
        + connector_loss_total_db
        + splice_loss_total_db
    )

    return {
        "fiber_loss_db": fiber_loss_db,
        "connector_loss_total_db": (
            connector_loss_total_db
        ),
        "splice_loss_total_db": (
            splice_loss_total_db
        ),
        "total_link_loss_db": total_link_loss_db
    }


# ==================================================
# CALCULATE RECEIVED POWER
# ==================================================

def calculate_received_power(
    parameters,
    losses
):

    P_rx_dbm = (
        parameters["P_tx_dbm"]
        - losses["total_link_loss_db"]
        + parameters["amplifier_gain_db"]
    )

    return P_rx_dbm


# ==================================================
# CALCULATE REQUIRED RECEIVER POWER
# ==================================================

def calculate_required_receiver_power(parameters):

    return (
        parameters["receiver_sensitivity_dbm"]
        + parameters["system_margin_db"]
    )


# ==================================================
# CALCULATE AVAILABLE POWER MARGIN
# ==================================================

def calculate_power_margin(
    P_rx_dbm,
    required_receiver_power_dbm
):

    return (
        P_rx_dbm
        - required_receiver_power_dbm
    )


# ==================================================
# CHECK LINK STATUS
# ==================================================

def check_link_status(power_margin_db):

    if power_margin_db >= 0:
        return "PASS"

    return "FAIL"


# ==================================================
# CALCULATE MAXIMUM FIBER DISTANCE
# ==================================================

def calculate_maximum_distance(
    parameters,
    losses
):

    required_receiver_power_dbm = (
        calculate_required_receiver_power(
            parameters
        )
    )

    fixed_losses_db = (
        losses["connector_loss_total_db"]
        + losses["splice_loss_total_db"]
    )

    numerator = (
        parameters["P_tx_dbm"]
        + parameters["amplifier_gain_db"]
        - fixed_losses_db
        - required_receiver_power_dbm
    )

    maximum_distance_km = (
        numerator
        / parameters["fiber_attenuation_db_per_km"]
    )

    return maximum_distance_km


# ==================================================
# PRINT RESULTS
# ==================================================

def print_results(
    parameters,
    losses,
    P_rx_dbm,
    required_receiver_power_dbm,
    power_margin_db,
    maximum_distance_km,
    link_status
):

    print("\n" + "=" * 55)
    print("OPTICAL LINK ANALYSIS RESULTS")
    print("=" * 55)

    print("\n--- INPUT PARAMETERS ---")

    print(
        f"Transmitter Power: "
        f"{parameters['P_tx_dbm']:.2f} dBm"
    )

    print(
        f"Fiber Length: "
        f"{parameters['fiber_length_km']:.2f} km"
    )

    print(
        f"Fiber Attenuation: "
        f"{parameters['fiber_attenuation_db_per_km']:.2f} dB/km"
    )

    print(
        f"Number of Connectors: "
        f"{parameters['num_connectors']}"
    )

    print(
        f"Number of Splices: "
        f"{parameters['num_splices']}"
    )

    print(
        f"Amplifier Gain: "
        f"{parameters['amplifier_gain_db']:.2f} dB"
    )

    print(
        f"Receiver Sensitivity: "
        f"{parameters['receiver_sensitivity_dbm']:.2f} dBm"
    )

    print(
        f"Required System Margin: "
        f"{parameters['system_margin_db']:.2f} dB"
    )


    print("\n--- LOSS CALCULATION ---")

    print(
        f"Fiber Loss: "
        f"{losses['fiber_loss_db']:.2f} dB"
    )

    print(
        f"Connector Loss: "
        f"{losses['connector_loss_total_db']:.2f} dB"
    )

    print(
        f"Splice Loss: "
        f"{losses['splice_loss_total_db']:.2f} dB"
    )

    print(
        f"Total Link Loss: "
        f"{losses['total_link_loss_db']:.2f} dB"
    )


    print("\n--- RECEIVER ANALYSIS ---")

    print(
        f"Received Power: "
        f"{P_rx_dbm:.2f} dBm"
    )

    print(
        f"Required Receiver Power: "
        f"{required_receiver_power_dbm:.2f} dBm"
    )

    print(
        f"Available Power Margin: "
        f"{power_margin_db:.2f} dB"
    )


    print("\n--- MAXIMUM LINK DISTANCE ---")

    print(
        f"Maximum Fiber Length: "
        f"{maximum_distance_km:.2f} km"
    )


    print("\n--- LINK STATUS ---")

    print(
        f"STATUS: {link_status}"
    )

    print("=" * 55)


# ==================================================
# PLOT RECEIVED POWER
# ==================================================

def plot_received_power(
    parameters,
    losses,
    required_receiver_power_dbm,
    maximum_distance_km
):

    distance_values = np.linspace(
        0,
        maximum_distance_km * 1.3,
        500
    )

    received_power_values = (
        parameters["P_tx_dbm"]
        - (
            distance_values
            * parameters["fiber_attenuation_db_per_km"]
        )
        - losses["connector_loss_total_db"]
        - losses["splice_loss_total_db"]
        + parameters["amplifier_gain_db"]
    )

    plt.figure(figsize=(9, 5))

    plt.plot(
        distance_values,
        received_power_values,
        linewidth=2,
        label="Received Optical Power"
    )

    plt.axhline(
        required_receiver_power_dbm,
        linestyle="--",
        linewidth=2,
        label="Required Receiver Power"
    )

    plt.axvline(
        maximum_distance_km,
        linestyle="--",
        linewidth=2,
        label=(
            f"Maximum Distance = "
            f"{maximum_distance_km:.1f} km"
        )
    )

    plt.axvline(
        parameters["fiber_length_km"],
        linestyle=":",
        linewidth=2,
        label=(
            f"Current Distance = "
            f"{parameters['fiber_length_km']:.1f} km"
        )
    )

    plt.title(
        "Received Optical Power vs Fiber Length"
    )

    plt.xlabel("Fiber Length (km)")
    plt.ylabel("Received Optical Power (dBm)")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_file = (
        RESULTS_DIR
        / "received_power_vs_fiber_length.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==================================================
# PLOT POWER MARGIN
# ==================================================

def plot_power_margin(
    parameters,
    losses,
    required_receiver_power_dbm,
    maximum_distance_km
):

    distance_values = np.linspace(
        0,
        maximum_distance_km * 1.3,
        500
    )

    received_power_values = (
        parameters["P_tx_dbm"]
        - (
            distance_values
            * parameters["fiber_attenuation_db_per_km"]
        )
        - losses["connector_loss_total_db"]
        - losses["splice_loss_total_db"]
        + parameters["amplifier_gain_db"]
    )

    power_margin_values = (
        received_power_values
        - required_receiver_power_dbm
    )

    plt.figure(figsize=(9, 5))

    plt.plot(
        distance_values,
        power_margin_values,
        linewidth=2,
        label="Available Power Margin"
    )

    plt.axhline(
        0,
        linestyle="--",
        linewidth=2,
        label="Link Limit (0 dB Margin)"
    )

    plt.axvline(
        maximum_distance_km,
        linestyle="--",
        linewidth=2,
        label=(
            f"Maximum Distance = "
            f"{maximum_distance_km:.1f} km"
        )
    )

    plt.axvline(
        parameters["fiber_length_km"],
        linestyle=":",
        linewidth=2,
        label=(
            f"Current Distance = "
            f"{parameters['fiber_length_km']:.1f} km"
        )
    )

    plt.title(
        "Power Margin vs Fiber Length"
    )

    plt.xlabel("Fiber Length (km)")
    plt.ylabel("Available Power Margin (dB)")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_file = (
        RESULTS_DIR
        / "power_margin_vs_fiber_length.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==================================================
# PLOT AMPLIFIER ANALYSIS
# ==================================================

def plot_amplifier_analysis(
    parameters,
    losses,
    required_receiver_power_dbm,
    maximum_distance_km
):

    amplifier_gain_values = np.linspace(
        0,
        20,
        100
    )

    maximum_distance_values = (
        parameters["P_tx_dbm"]
        + amplifier_gain_values
        - losses["connector_loss_total_db"]
        - losses["splice_loss_total_db"]
        - required_receiver_power_dbm
    ) / parameters["fiber_attenuation_db_per_km"]

    plt.figure(figsize=(9, 5))

    plt.plot(
        amplifier_gain_values,
        maximum_distance_values,
        linewidth=2,
        label="Maximum Fiber Length"
    )

    plt.axvline(
        parameters["amplifier_gain_db"],
        linestyle="--",
        linewidth=2,
        label=(
            f"Current Gain = "
            f"{parameters['amplifier_gain_db']:.1f} dB"
        )
    )

    plt.axhline(
        maximum_distance_km,
        linestyle=":",
        linewidth=2,
        label=(
            f"Current Maximum Distance = "
            f"{maximum_distance_km:.1f} km"
        )
    )

    plt.title(
        "Maximum Fiber Length vs Amplifier Gain"
    )

    plt.xlabel(
        "Optical Amplifier Gain (dB)"
    )

    plt.ylabel(
        "Maximum Fiber Length (km)"
    )

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_file = (
        RESULTS_DIR
        / "maximum_distance_vs_amplifier_gain.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==================================================
# PLOT LOSS BREAKDOWN
# ==================================================

def plot_loss_breakdown(losses):

    loss_components = [
        "Fiber Loss",
        "Connector Loss",
        "Splice Loss"
    ]

    loss_values = [
        losses["fiber_loss_db"],
        losses["connector_loss_total_db"],
        losses["splice_loss_total_db"]
    ]

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        loss_components,
        loss_values
    )

    for bar, loss in zip(
        bars,
        loss_values
    ):

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            f"{loss:.1f} dB",
            ha="center",
            va="bottom"
        )

    plt.title(
        "Optical Link Loss Breakdown"
    )

    plt.xlabel("Loss Component")
    plt.ylabel("Optical Loss (dB)")

    plt.grid(
        True,
        axis="y"
    )

    plt.tight_layout()

    output_file = (
        RESULTS_DIR
        / "optical_link_loss_breakdown.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==================================================
# PLOT ATTENUATION ANALYSIS
# ==================================================

def plot_attenuation_analysis(
    parameters,
    losses,
    required_receiver_power_dbm,
    maximum_distance_km
):

    attenuation_values = np.linspace(
        0.1,
        0.5,
        200
    )

    maximum_distance_values = (
        parameters["P_tx_dbm"]
        + parameters["amplifier_gain_db"]
        - losses["connector_loss_total_db"]
        - losses["splice_loss_total_db"]
        - required_receiver_power_dbm
    ) / attenuation_values

    plt.figure(figsize=(9, 5))

    plt.plot(
        attenuation_values,
        maximum_distance_values,
        linewidth=2,
        label="Maximum Fiber Length"
    )

    plt.axvline(
        parameters["fiber_attenuation_db_per_km"],
        linestyle="--",
        linewidth=2,
        label=(
            f"Current Attenuation = "
            f"{parameters['fiber_attenuation_db_per_km']:.2f} dB/km"
        )
    )

    plt.axhline(
        maximum_distance_km,
        linestyle=":",
        linewidth=2,
        label=(
            f"Current Maximum Distance = "
            f"{maximum_distance_km:.1f} km"
        )
    )

    plt.scatter(
        parameters["fiber_attenuation_db_per_km"],
        maximum_distance_km,
        s=60,
        label="Current Operating Point"
    )

    plt.title(
        "Maximum Fiber Length vs Fiber Attenuation"
    )

    plt.xlabel(
        "Fiber Attenuation (dB/km)"
    )

    plt.ylabel(
        "Maximum Fiber Length (km)"
    )

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_file = (
        RESULTS_DIR
        / "maximum_distance_vs_fiber_attenuation.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    parameters = get_link_parameters()

    losses = calculate_losses(
        parameters
    )

    P_rx_dbm = calculate_received_power(
        parameters,
        losses
    )

    required_receiver_power_dbm = (
        calculate_required_receiver_power(
            parameters
        )
    )

    power_margin_db = calculate_power_margin(
        P_rx_dbm,
        required_receiver_power_dbm
    )

    link_status = check_link_status(
        power_margin_db
    )

    maximum_distance_km = (
        calculate_maximum_distance(
            parameters,
            losses
        )
    )

    print_results(
        parameters,
        losses,
        P_rx_dbm,
        required_receiver_power_dbm,
        power_margin_db,
        maximum_distance_km,
        link_status
    )

    plot_received_power(
        parameters,
        losses,
        required_receiver_power_dbm,
        maximum_distance_km
    )

    plot_power_margin(
        parameters,
        losses,
        required_receiver_power_dbm,
        maximum_distance_km
    )

    plot_amplifier_analysis(
        parameters,
        losses,
        required_receiver_power_dbm,
        maximum_distance_km
    )

    plot_loss_breakdown(
        losses
    )

    plot_attenuation_analysis(
        parameters,
        losses,
        required_receiver_power_dbm,
        maximum_distance_km
    )


# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    main()