import struct
import csv
import argparse
import os

# === User Configuration ===

STRUCT_FORMATS = {
    "adcs": "<" + "LB" + 6 * "f" + "B" + 3 * "f" + 9 * "H" + 6 * "B" + 4 * "f",
    "cdh": "<" + "LbLbbbbb",
    "cmd_logs": "<" + "LBB",
    "comms": "<" + "Lf",
    "eps": "<" + "Lbhhhhb" + "h" * 4 + "L" * 2 + "h" * 30 + "b",
    "gps": "<" + "LBBBHLllllHHHHHllllll",
    "hal": "<" + "L" + "b" * 43,
    "eps_warning": "<" + "L" + "b" * 10
}


# ===========================

FIELDS = {
    "adcs" : [
        "TIME_ADCS",
        "MODE",
        "GYRO_X",
        "GYRO_Y",
        "GYRO_Z",
        "MAG_X",
        "MAG_Y",
        "MAG_Z",
        "SUN_STATUS",
        "SUN_VEC_X",
        "SUN_VEC_Y",
        "SUN_VEC_Z",
        "LIGHT_SENSOR_XP",
        "LIGHT_SENSOR_XM",
        "LIGHT_SENSOR_YP",
        "LIGHT_SENSOR_YM",
        "LIGHT_SENSOR_ZP1",
        "LIGHT_SENSOR_ZP2",
        "LIGHT_SENSOR_ZP3",
        "LIGHT_SENSOR_ZP4",
        "LIGHT_SENSOR_ZM",
        "XP_COIL_STATUS",
        "XM_COIL_STATUS",
        "YP_COIL_STATUS",
        "YM_COIL_STATUS",
        "ZP_COIL_STATUS",
        "ZM_COIL_STATUS",
        "COARSE_ATTITUDE_QW",
        "COARSE_ATTITUDE_QX",
        "COARSE_ATTITUDE_QY",
        "COARSE_ATTITUDE_QZ",
    ],
    "cmd_logs" : ["TIME", 
                  "CMD_ID", 
                  "STATUS"],
    "cdh" : ["TIME", 
             "SC_STATE", 
             "SD_USAGE", 
             "CURRENT_RAM_USAGE",
             "REBOOT_COUNT",
             "WATCHDOG_TIMER",
             "HAL_BITFLAGS",
             "DETUMBLING_ERROR_FLAG"],
    "comms" : ["TIME", "RSSI"],
    "eps" : ["TIME",
        "EPS_POWER_FLAG",
        "MAINBOARD_TEMPERATURE",
        "MAINBOARD_VOLTAGE",
        "MAINBOARD_CURRENT",
        "BATTERY_PACK_TEMPERATURE",
        "BATTERY_PACK_REPORTED_SOC",
        "BATTERY_PACK_REPORTED_CAPACITY",
        "BATTERY_PACK_CURRENT",
        "BATTERY_PACK_VOLTAGE",
        "BATTERY_PACK_MIDPOINT_VOLTAGE",
        "BATTERY_PACK_TTE",
        "BATTERY_PACK_TTF",
        "XP_COIL_VOLTAGE",
        "XP_COIL_CURRENT",
        "XM_COIL_VOLTAGE",
        "XM_COIL_CURRENT",
        "YP_COIL_VOLTAGE",
        "YP_COIL_CURRENT",
        "YM_COIL_VOLTAGE",
        "YM_COIL_CURRENT",
        "ZP_COIL_VOLTAGE",
        "ZP_COIL_CURRENT",
        "ZM_COIL_VOLTAGE",
        "ZM_COIL_CURRENT",
        "JETSON_INPUT_VOLTAGE",
        "JETSON_INPUT_CURRENT",
        "RF_LDO_OUTPUT_VOLTAGE",
        "RF_LDO_OUTPUT_CURRENT",
        "GPS_VOLTAGE",
        "GPS_CURRENT",
        "XP_SOLAR_CHARGE_VOLTAGE",
        "XP_SOLAR_CHARGE_CURRENT",
        "XM_SOLAR_CHARGE_VOLTAGE",
        "XM_SOLAR_CHARGE_CURRENT",
        "YP_SOLAR_CHARGE_VOLTAGE",
        "YP_SOLAR_CHARGE_CURRENT",
        "YM_SOLAR_CHARGE_VOLTAGE",
        "YM_SOLAR_CHARGE_CURRENT",
        "ZP_SOLAR_CHARGE_VOLTAGE",
        "ZP_SOLAR_CHARGE_CURRENT",
        "ZM_SOLAR_CHARGE_VOLTAGE",
        "ZM_SOLAR_CHARGE_CURRENT",
        "BATTERY_HEATERS_ENABLED"],
    "eps_warning": [
        "TIME_EPS_WARNING",
        "MAINBOARD_POWER_ALERT",
        "PERIPH_POWER_ALERT",
        "RADIO_POWER_ALERT",
        "JETSON_POWER_ALERT",
        "XP_COIL_POWER_ALERT",
        "XM_COIL_POWER_ALERT",
        "YP_COIL_POWER_ALERT",
        "YM_COIL_POWER_ALERT",
        "ZP_COIL_POWER_ALERT",
        "ZM_COIL_POWER_ALERT"
    ],
    "gps" : ["TIME",
            "GPS_MESSAGE_ID",
            "GPS_FIX_MODE",
            "GPS_NUMBER_OF_SV",
            "GPS_GNSS_WEEK",
            "GPS_GNSS_TOW",
            "GPS_LATITUDE",
            "GPS_LONGITUDE",
            "GPS_ELLIPSOID_ALT",
            "GPS_MEAN_SEA_LVL_ALT",
            "GPS_GDOP",
            "GPS_PDOP",
            "GPS_HDOP",
            "GPS_VDOP",
            "GPS_TDOP",
            "GPS_ECEF_X",
            "GPS_ECEF_Y",
            "GPS_ECEF_Z",
            "GPS_ECEF_VX",
            "GPS_ECEF_VY",
            "GPS_ECEF_VZ"],
    "hal": ["TIME_HAL",
            "SDCARD_ERROR",
            "SDCARD_ERROR_COUNT",
            "SDCARD_DEAD",
            "RTC_ERROR",
            "RTC_ERROR_COUNT",
            "RTC_DEAD",
            "GPS_ERROR",
            "GPS_ERROR_COUNT",
            "GPS_DEAD",
            "RADIO_ERROR",
            "RADIO_ERROR_COUNT",
            "RADIO_DEAD",
            "IMU_ERROR",
            "IMU_ERROR_COUNT",
            "IMU_DEAD",
            "FUEL_GAUGE_ERROR",
            "FUEL_GAUGE_ERROR_COUNT",
            "FUEL_GAUGE_DEAD",
            "BATT_HEATERS_ERROR",
            "BATT_HEATERS_ERROR_COUNT",
            "BATT_HEATERS_DEAD",
            "WATCHDOG_ERROR",
            "WATCHDOG_ERROR_COUNT",
            "WATCHDOG_DEAD",
            "BURN_WIRES_ERROR",
            "BURN_WIRES_ERROR_COUNT",
            "BURN_WIRES_DEAD",
            "BOARD_PWR_ERROR",
            "BOARD_PWR_ERROR_COUNT",
            "BOARD_PWR_DEAD",
            "RADIO_PWR_ERROR",
            "RADIO_PWR_ERROR_COUNT",
            "RADIO_PWR_DEAD",
            "GPS_PWR_ERROR",
            "GPS_PWR_ERROR_COUNT",
            "GPS_PWR_DEAD",
            "JETSON_PWR_ERROR",
            "JETSON_PWR_ERROR_COUNT",
            "JETSON_PWR_DEAD",
            "XP_PWR_ERROR",
            "XP_PWR_ERROR_COUNT",
            "XP_PWR_DEAD",
            "XM_PWR_ERROR",
            "XM_PWR_ERROR_COUNT",
            "XM_PWR_DEAD",
            "YP_PWR_ERROR",
            "YP_PWR_ERROR_COUNT",
            "YP_PWR_DEAD",
            "YM_PWR_ERROR",
            "YM_PWR_ERROR_COUNT",
            "YM_PWR_DEAD",
            "ZP_PWR_ERROR",
            "ZP_PWR_ERROR_COUNT",
            "ZP_PWR_DEAD",
            "TORQUE_XP_ERROR",
            "TORQUE_XP_ERROR_COUNT",
            "TORQUE_XP_DEAD",
            "TORQUE_XM_ERROR",
            "TORQUE_XM_ERROR_COUNT",
            "TORQUE_XM_DEAD",
            "TORQUE_YP_ERROR",
            "TORQUE_YP_ERROR_COUNT",
            "TORQUE_YP_DEAD",
            "TORQUE_YM_ERROR",
            "TORQUE_YM_ERROR_COUNT",
            "TORQUE_YM_DEAD",
            "TORQUE_ZP_ERROR",
            "TORQUE_ZP_ERROR_COUNT",
            "TORQUE_ZP_DEAD",
            "TORQUE_ZM_ERROR",
            "TORQUE_ZM_ERROR_COUNT",
            "TORQUE_ZM_DEAD",
            "LIGHT_XP_ERROR",
            "LIGHT_XP_ERROR_COUNT",
            "LIGHT_XP_DEAD",
            "LIGHT_XM_ERROR",
            "LIGHT_XM_ERROR_COUNT",
            "LIGHT_XM_DEAD",
            "LIGHT_YP_ERROR",
            "LIGHT_YP_ERROR_COUNT",
            "LIGHT_YP_DEAD",
            "LIGHT_YM_ERROR",
            "LIGHT_YM_ERROR_COUNT",
            "LIGHT_YM_DEAD",
            "LIGHT_ZM_ERROR",
            "LIGHT_ZM_ERROR_COUNT",
            "LIGHT_ZM_DEAD",
            "LIGHT_ZP_1_ERROR",
            "LIGHT_ZP_1_ERROR_COUNT",
            "LIGHT_ZP_1_DEAD",
            "LIGHT_ZP_2_ERROR",
            "LIGHT_ZP_2_ERROR_COUNT",
            "LIGHT_ZP_2_DEAD",
            "LIGHT_ZP_3_ERROR",
            "LIGHT_ZP_3_ERROR_COUNT",
            "LIGHT_ZP_3_DEAD",
            "LIGHT_ZP_4_ERROR",
            "LIGHT_ZP_4_ERROR_COUNT",
            "LIGHT_ZP_4_DEAD",
            "NEOPIXEL_ERROR",
            "NEOPIXEL_ERROR_COUNT",
            "NEOPIXEL_DEAD"]
}


def read_and_unpack_bin_file(struct_format, input_file):
    record_size = struct.calcsize(struct_format)
    data = []

    with open(input_file, 'rb') as f:
        while True:
            bytes_read = f.read(record_size)
            if len(bytes_read) < record_size:
                break
            try:
                record = struct.unpack(struct_format, bytes_read)
                data.append(record)
            except struct.error as e:
                print(f"Unpacking error in file {input_file}: {e}")
                break

    return data

def write_to_csv(data, field_names, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(field_names)
        writer.writerows(data)

def process_all_bin_files(input_root, output_root):
    for root, dirs, files in os.walk(input_root):
        relative_path = os.path.relpath(root, input_root)
        subsystem = os.path.basename(root)

        if subsystem not in STRUCT_FORMATS:
            continue  # Skip folders not matching known subsystems

        struct_format = STRUCT_FORMATS[subsystem]
        field_names = FIELDS[subsystem]

        for file in files:
            if file.endswith('.bin'):
                bin_path = os.path.join(root, file)

                # Mirror folder structure under output_root
                output_folder = os.path.join(output_root, relative_path)
                csv_filename = file.replace('.bin', '.csv')
                csv_path = os.path.join(output_folder, csv_filename)

                print(f"Processing: {bin_path}")
                data = read_and_unpack_bin_file(struct_format, bin_path)

                if any(len(record) != len(field_names) for record in data):
                    print(f"❌ Field count mismatch in file {bin_path}")
                    continue

                write_to_csv(data, field_names, csv_path)
                print(f"✅ Converted to {csv_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert CubeSat binary logs to CSV.")
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Path to top-level input log directory containing subsystem folders"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Path to output directory where CSV files should be written"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(f"❌ Input path is not a directory: {args.input}")
        return

    process_all_bin_files(args.input, args.output)

if __name__ == '__main__':
    main()
