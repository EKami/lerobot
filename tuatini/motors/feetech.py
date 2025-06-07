# PROTOCOL_VERSION = 0
# TIMEOUT_MS = 1000
# # High number of retries is needed for feetech compared to dynamixel motors.
# NUM_READ_RETRY = 20
# NUM_WRITE_RETRY = 20
# # The following bounds define the lower and upper joints range (after calibration).
# # For joints in degree (i.e. revolute joints), their nominal range is [-180, 180] degrees
# # which corresponds to a half rotation on the left and half rotation on the right.
# # Some joints might require higher range, so we allow up to [-270, 270] degrees until
# # an error is raised.
# LOWER_BOUND_DEGREE = -270
# UPPER_BOUND_DEGREE = 270
# # For joints in percentage (i.e. joints that move linearly like the prismatic joint of a gripper),
# # their nominal range is [0, 100] %. For instance, for Aloha gripper, 0% is fully
# # closed, and 100% is fully open. To account for slight calibration issue, we allow up to
# # [-10, 110] until an error is raised.
# LOWER_BOUND_LINEAR = -10
# UPPER_BOUND_LINEAR = 110
# HALF_TURN_DEGREE = 180
# # See this link for STS3215 Memory Table:
# # https://docs.google.com/spreadsheets/d/1GVs7W1VS1PqdhA1nW-abeyAHhTUxKUdR/edit?usp=sharing&ouid=116566590112741600240&rtpof=true&sd=true
# # data_name: (address, size_byte)
# STS3215_CONTROL_TABLE = {
#     "Model": (3, 2),
#     "ID": (5, 1),
#     "Baud_Rate": (6, 1),
#     "Return_Delay": (7, 1),
#     "Response_Status_Level": (8, 1),
#     "Min_Angle_Limit": (9, 2),
#     "Max_Angle_Limit": (11, 2),
#     "Max_Temperature_Limit": (13, 1),
#     "Max_Voltage_Limit": (14, 1),
#     "Min_Voltage_Limit": (15, 1),
#     "Max_Torque_Limit": (16, 2),
#     "Phase": (18, 1),
#     "Unloading_Condition": (19, 1),
#     "LED_Alarm_Condition": (20, 1),
#     "P_Coefficient": (21, 1),
#     "D_Coefficient": (22, 1),
#     "I_Coefficient": (23, 1),
#     "Minimum_Startup_Force": (24, 2),
#     "CW_Dead_Zone": (26, 1),
#     "CCW_Dead_Zone": (27, 1),
#     "Protection_Current": (28, 2),
#     "Angular_Resolution": (30, 1),
#     "Offset": (31, 2),
#     "Mode": (33, 1),
#     "Protective_Torque": (34, 1),
#     "Protection_Time": (35, 1),
#     "Overload_Torque": (36, 1),
#     "Speed_closed_loop_P_proportional_coefficient": (37, 1),
#     "Over_Current_Protection_Time": (38, 1),
#     "Velocity_closed_loop_I_integral_coefficient": (39, 1),
#     "Torque_Enable": (40, 1),
#     "Acceleration": (41, 1),
#     "Goal_Position": (42, 2),
#     "Goal_Time": (44, 2),
#     "Goal_Speed": (46, 2),
#     "Torque_Limit": (48, 2),
#     "Lock": (55, 1),
#     "Present_Position": (56, 2),
#     "Present_Speed": (58, 2),
#     "Present_Load": (60, 2),
#     "Present_Voltage": (62, 1),
#     "Present_Temperature": (63, 1),
#     "Status": (65, 1),
#     "Moving": (66, 1),
#     "Present_Current": (69, 2),
#     # Not in the Memory Table
#     "Maximum_Acceleration": (85, 2),
# }
# MODEL_RESOLUTION = 4096
# CALIBRATION_REQUIRED = ["Goal_Position", "Present_Position"]
# CONVERT_UINT32_TO_INT32_REQUIRED = ["Goal_Position", "Present_Position"]
# class OperatingMode(Enum):
#     # position servo mode
#     POSITION = 0
#     # The motor is in constant speed mode, which is controlled by parameter 0x2e, and the highest bit 15 is
#     # the direction bit
#     VELOCITY = 1
#     # PWM open-loop speed regulation mode, with parameter 0x2c running time parameter control, bit11 as
#     # direction bit
#     PWM = 2
#     # In step servo mode, the number of step progress is represented by parameter 0x2a, and the highest bit 15
#     # is the direction bit
#     STEP = 3
# class JointOutOfRangeError(Exception):
#     def __init__(self, message="Joint is out of range"):
#         self.message = message
#         super().__init__(self.message)
# class RobotDeviceNotConnectedError(Exception):
#     """Exception raised when the robot device is not connected."""
#     def __init__(self, message="This robot device is not connected. Try calling `robot_device.connect()` first."):
#         self.message = message
#         super().__init__(self.message)
# class RobotDeviceAlreadyConnectedError(Exception):
#     """Exception raised when the robot device is already connected."""
#     def __init__(
#         self,
#         message="This robot device is already connected. Try not calling `robot_device.connect()` twice.",
#     ):
#         self.message = message
#         super().__init__(self.message)
# # Servos are either in degree or linear mode.
# class CalibrationMode(enum.Enum):
#     # Joints with rotational motions are expressed in degrees in nominal range of [-180, 180]
#     DEGREE = 0
#     # Joints with linear motions are expressed in nominal range of [0, 100]
#     LINEAR = 1
# class FeetechTorqueMode(enum.Enum):
#     ENABLED = 1
#     DISABLED = 0
# class FeetechMotorsBus:
#     """
#     The FeetechMotorsBus class allows to efficiently read and write to the attached motors. It relies on
#     the python [feetech sdk](https://github.com/ftservo/FTServo_Python) available on [Pypi](https://pypi.org/project/ftservo-python-sdk/).
#     A FeetechMotorsBus instance requires a port (e.g. `FeetechMotorsBus(port="/dev/tty.usbmodem575E0031751"`)).
#     """
#     def __init__(self, motors, port):
#         # TODO if ROS was used, we would have a node that would handle the motors bus
#         # and we wouldn't need to pass the port here
#         self.motors = motors
#         self.port = port
#         self.port_handler = None
#         self.packet_handler = None
#         # TODO each Reader and Writer should be a class/struct, one motor should be represented by its own STS3215Servo class
#         self.group_readers = {}
#         self.group_writers = {}
#         self.logs = {}
#         self.is_connected = False
#         self.calibration = None
#         # Motors positions
#         self.track_positions = {}
#     def connect(self):
#         if self.is_connected:
#             raise RobotDeviceAlreadyConnectedError(
#                 f"FeetechMotorsBus({self.port}) is already connected. Do not call `motors_bus.connect()` twice."
#             )
#         self.port_handler = scs.PortHandler(self.port)
#         self.packet_handler = scs.PacketHandler(PROTOCOL_VERSION)
#         if not self.port_handler.openPort():
#             raise OSError(f"Failed to open port '{self.port}'.")
#         # Allow to read and write
#         self.is_connected = True
#         self.port_handler.setPacketTimeoutMillis(TIMEOUT_MS)
#     def __del__(self):
#         if getattr(self, "is_connected", False):
#             self.disconnect()
#     def disconnect(self):
#         if not self.is_connected:
#             raise RobotDeviceNotConnectedError(
#                 f"FeetechMotorsBus({self.port}) is not connected. Try running `motors_bus.connect()` first."
#             )
#         if self.port_handler is not None:
#             self.port_handler.closePort()
#             self.port_handler = None
#         self.packet_handler = None
#         self.group_readers = {}
#         self.group_writers = {}
#         self.is_connected = False
#     def set_calibration(self, calibration: dict[str, list]):
#         self.calibration = calibration
#     @property
#     def motor_names(self) -> list[str]:
#         return list(self.motors.keys())
#     @property
#     def motor_indices(self) -> list[int]:
#         return [idx for idx, _ in self.motors.values()]
#     @staticmethod
#     def get_group_sync_key(data_name, motor_names):
#         group_key = f"{data_name}_" + "_".join(motor_names)
#         return group_key
#     @staticmethod
#     def get_log_name(var_name, fn_name, data_name, motor_names):
#         group_key = FeetechMotorsBus.get_group_sync_key(data_name, motor_names)
#         log_name = f"{var_name}_{fn_name}_{group_key}"
#         return log_name
#     def avoid_rotation_reset(self, values, motor_names, data_name):
#         """Handles position value wrapping for motors that reset their position values after a full rotation.
#         This function tracks motor positions and detects when a full rotation occurs, adjusting the position
#         values to maintain continuous position tracking. It handles two cases:
#         1. When position goes below 0 and resets to 4095
#         2. When position goes above 4095 and resets to 0
#         The function maintains a history of previous positions for each motor to detect these transitions.
#         Args:
#             values (np.ndarray): Array of current position values for the motors
#             motor_names (list[str] | None): List of motor names to process. If None, processes all motors
#             data_name (str): Name of the data being tracked (e.g. "Present_Position")
#         Returns:
#             np.ndarray: Adjusted position values that account for full rotations
#         """
#         if data_name not in self.track_positions:
#             self.track_positions[data_name] = {
#                 "prev": [None] * len(self.motor_names),
#                 # Assume False at initialization
#                 "below_zero": [False] * len(self.motor_names),
#                 "above_max": [False] * len(self.motor_names),
#             }
#         track = self.track_positions[data_name]
#         if motor_names is None:
#             motor_names = self.motor_names
#         for i, name in enumerate(motor_names):
#             idx = self.motor_names.index(name)
#             if track["prev"][idx] is None:
#                 track["prev"][idx] = values[i]
#                 continue
#             # Detect a full rotation occurred
#             if abs(track["prev"][idx] - values[i]) > 2048:
#                 # Position went below 0 and got reset to 4095
#                 if track["prev"][idx] < values[i]:
#                     # So we set negative value by adding a full rotation
#                     values[i] -= 4096
#                 # Position went above 4095 and got reset to 0
#                 elif track["prev"][idx] > values[i]:
#                     # So we add a full rotation
#                     values[i] += 4096
#             track["prev"][idx] = values[i]
#         return values
#     def apply_calibration(self, values: np.ndarray | list, motor_names: list[str] | None):
#         """Convert from unsigned int32 joint position range [0, 2**32[ to the universal float32 nominal degree range ]-180.0, 180.0[ with
#         a "zero position" at 0 degree.
#         Note: We say "nominal degree range" since the motors can take values outside this range. For instance, 190 degrees, if the motor
#         rotate more than a half a turn from the zero position. However, most motors can't rotate more than 180 degrees and will stay in this range.
#         Joints values are original in [0, 2**32[ (unsigned int32). Each motor are expected to complete a full rotation
#         when given a goal position that is + or - their resolution. For instance, feetech xl330-m077 have a resolution of 4096, and
#         at any position in their original range, let's say the position 56734, they complete a full rotation clockwise by moving to 60830,
#         or anticlockwise by moving to 52638. The position in the original range is arbitrary and might change a lot between each motor.
#         To harmonize between motors of the same model, different robots, or even models of different brands, we propose to work
#         in the centered nominal degree range ]-180, 180[.
#         """
#         if motor_names is None:
#             motor_names = self.motor_names
#         # Convert from unsigned int32 original range [0, 2**32] to signed float32 range
#         values = values.astype(np.float32)
#         for i, name in enumerate(motor_names):
#             calib_idx = self.calibration["motor_names"].index(name)
#             calib_mode = self.calibration["calib_mode"][calib_idx]
#             if CalibrationMode[calib_mode] == CalibrationMode.DEGREE:
#                 drive_mode = self.calibration["drive_mode"][calib_idx]
#                 homing_offset = self.calibration["homing_offset"][calib_idx]
#                 # Update direction of rotation of the motor to match between leader and follower.
#                 # In fact, the motor of the leader for a given joint can be assembled in an
#                 # opposite direction in term of rotation than the motor of the follower on the same joint.
#                 if drive_mode:
#                     values[i] *= -1
#                 # Convert from range [-2**31, 2**31[ to
#                 # nominal range ]-resolution, resolution[ (e.g. ]-2048, 2048[)
#                 values[i] += homing_offset
#                 # Convert from range ]-resolution, resolution[ to
#                 # universal float32 centered degree range ]-180, 180[
#                 values[i] = values[i] / (MODEL_RESOLUTION // 2) * HALF_TURN_DEGREE
#                 if (values[i] < LOWER_BOUND_DEGREE) or (values[i] > UPPER_BOUND_DEGREE):
#                     raise JointOutOfRangeError(
#                         f"Wrong motor position range detected for {name}. "
#                         f"Expected to be in nominal range of [-{HALF_TURN_DEGREE}, {HALF_TURN_DEGREE}] degrees (a full rotation), "
#                         f"with a maximum range of [{LOWER_BOUND_DEGREE}, {UPPER_BOUND_DEGREE}] degrees to account for joints that can rotate a bit more, "
#                         f"but present value is {values[i]} degree. "
#                         "This might be due to a cable connection issue creating an artificial 360 degrees jump in motor values. "
#                         "You need to recalibrate by running: `python lerobot/scripts/control_robot.py calibrate`"
#                     )
#             elif CalibrationMode[calib_mode] == CalibrationMode.LINEAR:
#                 start_pos = self.calibration["start_pos"][calib_idx]
#                 end_pos = self.calibration["end_pos"][calib_idx]
#                 # Rescale the present position to a nominal range [0, 100] %,
#                 # useful for joints with linear motions like Aloha gripper
#                 values[i] = (values[i] - start_pos) / (end_pos - start_pos) * 100
#                 if (values[i] < LOWER_BOUND_LINEAR) or (values[i] > UPPER_BOUND_LINEAR):
#                     raise JointOutOfRangeError(
#                         f"Wrong motor position range detected for {name}. "
#                         f"Expected to be in nominal range of [0, 100] % (a full linear translation), "
#                         f"with a maximum range of [{LOWER_BOUND_LINEAR}, {UPPER_BOUND_LINEAR}] % to account for some imprecision during calibration, "
#                         f"but present value is {values[i]} %. "
#                         "This might be due to a cable connection issue creating an artificial jump in motor values. "
#                         "You need to recalibrate by running: `python lerobot/scripts/control_robot.py calibrate`"
#                     )
#         return values
#     def revert_calibration(self, values: np.ndarray | list, motor_names: list[str] | None):
#         """Inverse of `apply_calibration`."""
#         if motor_names is None:
#             motor_names = self.motor_names
#         for i, name in enumerate(motor_names):
#             calib_idx = self.calibration["motor_names"].index(name)
#             calib_mode = self.calibration["calib_mode"][calib_idx]
#             if CalibrationMode[calib_mode] == CalibrationMode.DEGREE:
#                 drive_mode = self.calibration["drive_mode"][calib_idx]
#                 homing_offset = self.calibration["homing_offset"][calib_idx]
#                 # Convert from nominal 0-centered degree range [-180, 180] to
#                 # 0-centered resolution range (e.g. [-2048, 2048] for resolution=4096)
#                 values[i] = values[i] / HALF_TURN_DEGREE * (MODEL_RESOLUTION // 2)
#                 # Subtract the homing offsets to come back to actual motor range of values
#                 # which can be arbitrary.
#                 values[i] -= homing_offset
#                 # Remove drive mode, which is the rotation direction of the motor, to come back to
#                 # actual motor rotation direction which can be arbitrary.
#                 if drive_mode:
#                     values[i] *= -1
#             elif CalibrationMode[calib_mode] == CalibrationMode.LINEAR:
#                 start_pos = self.calibration["start_pos"][calib_idx]
#                 end_pos = self.calibration["end_pos"][calib_idx]
#                 # Convert from nominal lnear range of [0, 100] % to
#                 # actual motor range of values which can be arbitrary.
#                 values[i] = values[i] / 100 * (end_pos - start_pos) + start_pos
#         values = np.round(values).astype(np.int32)
#         return values
#     def autocorrect_calibration(self, values: np.ndarray | list, motor_names: list[str] | None):
#         """This function automatically detects issues with values of motors after calibration, and correct for these issues.
#         Some motors might have values outside of expected maximum bounds after calibration.
#         For instance, for a joint in degree, its value can be outside [-270, 270] degrees, which is totally unexpected given
#         a nominal range of [-180, 180] degrees, which represents half a turn to the left or right starting from zero position.
#         Known issues:
#         #1: Motor value randomly shifts of a full turn, caused by hardware/connection errors.
#         #2: Motor internal homing offset is shifted of a full turn, caused by using default calibration (e.g Aloha).
#         #3: motor internal homing offset is shifted of less or more than a full turn, caused by using default calibration
#             or by human error during manual calibration.
#         Issues #1 and #2 can be solved by shifting the calibration homing offset by a full turn.
#         Issue #3 will be visually detected by user and potentially captured by the safety feature `max_relative_target`,
#         that will slow down the motor, raise an error asking to recalibrate. Manual recalibrating will solve the issue.
#         Note: A full turn corresponds to 360 degrees but also to 4096 steps for a motor resolution of 4096.
#         """
#         if motor_names is None:
#             motor_names = self.motor_names
#         # Convert from unsigned int32 original range [0, 2**32] to signed float32 range
#         values = values.astype(np.float32)
#         for i, name in enumerate(motor_names):
#             calib_idx = self.calibration["motor_names"].index(name)
#             calib_mode = self.calibration["calib_mode"][calib_idx]
#             if CalibrationMode[calib_mode] == CalibrationMode.DEGREE:
#                 drive_mode = self.calibration["drive_mode"][calib_idx]
#                 homing_offset = self.calibration["homing_offset"][calib_idx]
#                 _, model = self.motors[name]
#                 resolution = self.model_resolution[model]
#                 if drive_mode:
#                     values[i] *= -1
#                 # Convert from initial range to range [-180, 180] degrees
#                 calib_val = (values[i] + homing_offset) / (resolution // 2) * HALF_TURN_DEGREE
#                 in_range = (calib_val > LOWER_BOUND_DEGREE) and (calib_val < UPPER_BOUND_DEGREE)
#                 # Solve this inequality to find the factor to shift the range into [-180, 180] degrees
#                 # values[i] = (values[i] + homing_offset + resolution * factor) / (resolution // 2) * HALF_TURN_DEGREE
#                 # - HALF_TURN_DEGREE <= (values[i] + homing_offset + resolution * factor) / (resolution // 2) * HALF_TURN_DEGREE <= HALF_TURN_DEGREE
#                 # (- HALF_TURN_DEGREE / HALF_TURN_DEGREE * (resolution // 2) - values[i] - homing_offset) / resolution <= factor <= (HALF_TURN_DEGREE / 180 * (resolution // 2) - values[i] - homing_offset) / resolution
#                 low_factor = (
#                     -HALF_TURN_DEGREE / HALF_TURN_DEGREE * (resolution // 2) - values[i] - homing_offset
#                 ) / resolution
#                 upp_factor = (
#                     HALF_TURN_DEGREE / HALF_TURN_DEGREE * (resolution // 2) - values[i] - homing_offset
#                 ) / resolution
#             elif CalibrationMode[calib_mode] == CalibrationMode.LINEAR:
#                 start_pos = self.calibration["start_pos"][calib_idx]
#                 end_pos = self.calibration["end_pos"][calib_idx]
#                 # Convert from initial range to range [0, 100] in %
#                 calib_val = (values[i] - start_pos) / (end_pos - start_pos) * 100
#                 in_range = (calib_val > LOWER_BOUND_LINEAR) and (calib_val < UPPER_BOUND_LINEAR)
#                 # Solve this inequality to find the factor to shift the range into [0, 100] %
#                 # values[i] = (values[i] - start_pos + resolution * factor) / (end_pos + resolution * factor - start_pos - resolution * factor) * 100
#                 # values[i] = (values[i] - start_pos + resolution * factor) / (end_pos - start_pos) * 100
#                 # 0 <= (values[i] - start_pos + resolution * factor) / (end_pos - start_pos) * 100 <= 100
#                 # (start_pos - values[i]) / resolution <= factor <= (end_pos - values[i]) / resolution
#                 low_factor = (start_pos - values[i]) / resolution
#                 upp_factor = (end_pos - values[i]) / resolution
#             if not in_range:
#                 # Get first integer between the two bounds
#                 if low_factor < upp_factor:
#                     factor = math.ceil(low_factor)
#                     if factor > upp_factor:
#                         raise ValueError(f"No integer found between bounds [{low_factor=}, {upp_factor=}]")
#                 else:
#                     factor = math.ceil(upp_factor)
#                     if factor > low_factor:
#                         raise ValueError(f"No integer found between bounds [{low_factor=}, {upp_factor=}]")
#                 if CalibrationMode[calib_mode] == CalibrationMode.DEGREE:
#                     out_of_range_str = f"{LOWER_BOUND_DEGREE} < {calib_val} < {UPPER_BOUND_DEGREE} degrees"
#                     in_range_str = f"{LOWER_BOUND_DEGREE} < {calib_val} < {UPPER_BOUND_DEGREE} degrees"
#                 elif CalibrationMode[calib_mode] == CalibrationMode.LINEAR:
#                     out_of_range_str = f"{LOWER_BOUND_LINEAR} < {calib_val} < {UPPER_BOUND_LINEAR} %"
#                     in_range_str = f"{LOWER_BOUND_LINEAR} < {calib_val} < {UPPER_BOUND_LINEAR} %"
#                 logging.warning(
#                     f"Auto-correct calibration of motor '{name}' by shifting value by {abs(factor)} full turns, "
#                     f"from '{out_of_range_str}' to '{in_range_str}'."
#                 )
#                 # A full turn corresponds to 360 degrees but also to 4096 steps for a motor resolution of 4096.
#                 self.calibration["homing_offset"][calib_idx] += resolution * factor
#     def apply_calibration_autocorrect(self, values: np.ndarray | list, motor_names: list[str] | None):
#         """This function apply the calibration, automatically detects out of range errors for motors values and attempt to correct.
#         For more info, see docstring of `apply_calibration` and `autocorrect_calibration`.
#         """
#         try:
#             values = self.apply_calibration(values, motor_names)
#         except JointOutOfRangeError as e:
#             print(e)
#             self.autocorrect_calibration(values, motor_names)
#             values = self.apply_calibration(values, motor_names)
#         return values
#     def convert_to_bytes(self, value, bytes):
#         # Note: No need to convert back into unsigned int, since this byte preprocessing
#         # already handles it for us.
#         if bytes == 1:
#             data = [
#                 scs.SCS_LOBYTE(scs.SCS_LOWORD(value)),
#             ]
#         elif bytes == 2:
#             data = [
#                 scs.SCS_LOBYTE(scs.SCS_LOWORD(value)),
#                 scs.SCS_HIBYTE(scs.SCS_LOWORD(value)),
#             ]
#         elif bytes == 4:
#             data = [
#                 scs.SCS_LOBYTE(scs.SCS_LOWORD(value)),
#                 scs.SCS_HIBYTE(scs.SCS_LOWORD(value)),
#                 scs.SCS_LOBYTE(scs.SCS_HIWORD(value)),
#                 scs.SCS_HIBYTE(scs.SCS_HIWORD(value)),
#             ]
#         else:
#             raise NotImplementedError(
#                 f"Value of the number of bytes to be sent is expected to be in [1, 2, 4], but "
#                 f"{bytes} is provided instead."
#             )
#         return data
#     def read(self, data_name, motor_names: str | list[str] | None = None) -> np.ndarray:
#         if not self.is_connected:
#             raise RobotDeviceNotConnectedError(
#                 f"FeetechMotorsBus({self.port}) is not connected. You need to run `motors_bus.connect()`."
#             )
#         start_time = time.perf_counter()
#         if motor_names is None:
#             motor_names = self.motor_names
#         if isinstance(motor_names, str):
#             motor_names = [motor_names]
#         addr, bytes = STS3215_CONTROL_TABLE[data_name]
#         group_key = self.get_group_sync_key(data_name, motor_names)
#         if data_name not in self.group_readers:
#             # Very Important to flush the buffer!
#             self.port_handler.ser.reset_output_buffer()
#             self.port_handler.ser.reset_input_buffer()
#             # create new group reader
#             self.group_readers[group_key] = scs.GroupSyncRead(self.port_handler, self.packet_handler, addr, bytes)
#             for idx in self.motor_indices:
#                 self.group_readers[group_key].addParam(idx)
#         for _ in range(NUM_READ_RETRY):
#             comm = self.group_readers[group_key].txRxPacket()
#             if comm == scs.COMM_SUCCESS:
#                 break
#         if comm != scs.COMM_SUCCESS:
#             raise ConnectionError(
#                 f"Read failed due to communication error on port {self.port} for group_key {group_key}: "
#                 f"{self.packet_handler.getTxRxResult(comm)}"
#             )
#         values = []
#         for idx in self.motor_indices:
#             value = self.group_readers[group_key].getData(idx, addr, bytes)
#             values.append(value)
#         values = np.array(values)
#         # Convert to signed int to use range [-2048, 2048] for our motor positions.
#         if data_name in CONVERT_UINT32_TO_INT32_REQUIRED:
#             values = values.astype(np.int32)
#         if data_name in CALIBRATION_REQUIRED:
#             values = self.avoid_rotation_reset(values, motor_names, data_name)
#             if self.calibration is not None:
#                 values = self.apply_calibration_autocorrect(values, motor_names)
#         # log the number of seconds it took to read the data from the motors
#         delta_ts_name = FeetechMotorsBus.get_log_name("delta_timestamp_s", "read", data_name, motor_names)
#         self.logs[delta_ts_name] = time.perf_counter() - start_time
#         # log the utc time at which the data was received
#         ts_utc_name = FeetechMotorsBus.get_log_name("timestamp_utc", "read", data_name, motor_names)
#         self.logs[ts_utc_name] = capture_timestamp_utc()
#         return values
#     def write(self, data_name, values: int | float | np.ndarray, motor_names: str | list[str] | None = None):
#         if not self.is_connected:
#             raise RobotDeviceNotConnectedError(
#                 f"FeetechMotorsBus({self.port}) is not connected. You need to run `motors_bus.connect()`."
#             )
#         start_time = time.perf_counter()
#         if motor_names is None:
#             motor_names = self.motor_names
#         if isinstance(motor_names, str):
#             motor_names = [motor_names]
#         if isinstance(values, (int, float, np.integer)):
#             values = [int(values)] * len(motor_names)
#         values = np.array(values)
#         motor_ids = []
#         models = []
#         for name in motor_names:
#             motor_idx, model = self.motors[name]
#             motor_ids.append(motor_idx)
#             models.append(model)
#         if data_name in CALIBRATION_REQUIRED and self.calibration is not None:
#             values = self.revert_calibration(values, motor_names)
#         values = values.tolist()
#         addr, bytes = STS3215_CONTROL_TABLE[data_name]
#         group_key = self.get_group_sync_key(data_name, motor_names)
#         init_group = data_name not in self.group_readers
#         if init_group:
#             self.group_writers[group_key] = scs.GroupSyncWrite(self.port_handler, self.packet_handler, addr, bytes)
#         for idx, value in zip(motor_ids, values, strict=True):
#             data = self.convert_to_bytes(value, bytes)
#             if init_group:
#                 self.group_writers[group_key].addParam(idx, data)
#             else:
#                 self.group_writers[group_key].changeParam(idx, data)
#         comm = self.group_writers[group_key].txPacket()
#         if comm != scs.COMM_SUCCESS:
#             raise ConnectionError(
#                 f"Write failed due to communication error on port {self.port} for group_key {group_key}: "
#                 f"{self.packet_handler.getTxRxResult(comm)}"
#             )
#         # log the number of seconds it took to write the data to the motors
#         delta_ts_name = FeetechMotorsBus.get_log_name("delta_timestamp_s", "write", data_name, motor_names)
#         self.logs[delta_ts_name] = time.perf_counter() - start_time
#         # TODO(rcadene): should we log the time before sending the write command?
#         # log the utc time when the write has been completed
#         ts_utc_name = FeetechMotorsBus.get_log_name("timestamp_utc", "write", data_name, motor_names)
#         self.logs[ts_utc_name] = capture_timestamp_utc()
import logging
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pprint import pformat
from typing import TypeAlias

import scservo_sdk as scs
import serial

from tuatini.motors.feetech_table import (
    FIRMWARE_MAJOR_VERSION,
    FIRMWARE_MINOR_VERSION,
    MODEL_BAUDRATE_TABLE,
    MODEL_CONTROL_TABLE,
    MODEL_ENCODING_TABLE,
    MODEL_NUMBER,
    MODEL_NUMBER_TABLE,
    MODEL_PROTOCOL,
    MODEL_RESOLUTION,
    SCAN_BAUDRATES,
)
from tuatini.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError

DEFAULT_PROTOCOL_VERSION = 0
DEFAULT_BAUDRATE = 1_000_000
DEFAULT_TIMEOUT_MS = 1000

NORMALIZED_DATA = ["Goal_Position", "Present_Position"]

NameOrID: TypeAlias = str | int
Value: TypeAlias = int | float


class DriveMode(Enum):
    NON_INVERTED = 0
    INVERTED = 1


class TorqueMode(Enum):
    ENABLED = 1
    DISABLED = 0


class OperatingMode(Enum):
    # position servo mode
    POSITION = 0
    # The motor is in constant speed mode, which is controlled by parameter 0x2e, and the highest bit 15 is
    # the direction bit
    VELOCITY = 1
    # PWM open-loop speed regulation mode, with parameter 0x2c running time parameter control, bit11 as
    # direction bit
    PWM = 2
    # In step servo mode, the number of step progress is represented by parameter 0x2a, and the highest bit 15
    # is the direction bit
    STEP = 3


@dataclass
class MotorCalibration:
    id: int
    drive_mode: int
    homing_offset: int
    range_min: int
    range_max: int


class MotorNormMode(str, Enum):
    RANGE_0_100 = "range_0_100"
    RANGE_M100_100 = "range_m100_100"
    DEGREES = "degrees"


@dataclass
class Motor:
    id: int
    model: str
    norm_mode: MotorNormMode


def scs_lobyte(w):
    return w & 0xFF


def scs_hibyte(w):
    return (w >> 8) & 0xFF


def scs_loword(l):
    return l & 0xFFFF


def scs_hiword(l):
    return (l >> 16) & 0xFFFF


def _split_into_byte_chunks(value: int, length: int) -> list[int]:
    if length == 1:
        data = [value]
    elif length == 2:
        data = [scs_lobyte(value), scs_lobyte(value)]
    elif length == 4:
        data = [
            scs_lobyte(scs_loword(value)),
            scs_hibyte(scs_loword(value)),
            scs_lobyte(scs_hiword(value)),
            scs_hibyte(scs_hiword(value)),
        ]
    return data


def encode_sign_magnitude(value: int, sign_bit_index: int):
    """
    https://en.wikipedia.org/wiki/Signed_number_representations#Sign%E2%80%93magnitude
    """
    max_magnitude = (1 << sign_bit_index) - 1
    magnitude = abs(value)
    if magnitude > max_magnitude:
        raise ValueError(f"Magnitude {magnitude} exceeds {max_magnitude} (max for {sign_bit_index=})")

    direction_bit = 1 if value < 0 else 0
    return (direction_bit << sign_bit_index) | magnitude


def decode_sign_magnitude(encoded_value: int, sign_bit_index: int):
    """
    https://en.wikipedia.org/wiki/Signed_number_representations#Sign%E2%80%93magnitude
    """
    direction_bit = (encoded_value >> sign_bit_index) & 1
    magnitude_mask = (1 << sign_bit_index) - 1
    magnitude = encoded_value & magnitude_mask
    return -magnitude if direction_bit else magnitude


def get_ctrl_table(model_ctrl_table: dict[str, dict], model: str) -> dict[str, tuple[int, int]]:
    ctrl_table = model_ctrl_table.get(model)
    if ctrl_table is None:
        raise KeyError(f"Control table for {model=} not found.")
    return ctrl_table


def get_address(model_ctrl_table: dict[str, dict], model: str, data_name: str) -> tuple[int, int]:
    ctrl_table = get_ctrl_table(model_ctrl_table, model)
    addr_bytes = ctrl_table.get(data_name)
    if addr_bytes is None:
        raise KeyError(f"Address for '{data_name}' not found in {model} control table.")
    return addr_bytes


class FeetechMotorsBus:
    """
    TODO if ROS was used, we would have a node that would handle the motors bus
    https://github.com/brukg/SO-100-arm?tab=readme-ov-file

    The FeetechMotorsBus class allows to efficiently read and write to the attached motors. It relies on the
    python feetech sdk to communicate with the motors, which is itself based on the dynamixel sdk.
    """

    apply_drive_mode = True
    available_baudrates = deepcopy(SCAN_BAUDRATES)
    default_baudrate = DEFAULT_BAUDRATE
    default_timeout = DEFAULT_TIMEOUT_MS
    model_baudrate_table = deepcopy(MODEL_BAUDRATE_TABLE)
    model_ctrl_table = deepcopy(MODEL_CONTROL_TABLE)
    model_encoding_table = deepcopy(MODEL_ENCODING_TABLE)
    model_number_table = deepcopy(MODEL_NUMBER_TABLE)
    model_resolution_table = deepcopy(MODEL_RESOLUTION)
    normalized_data = deepcopy(NORMALIZED_DATA)

    def __init__(
        self,
        port: str,
        motors: dict[str, Motor],
        calibration: dict[str, MotorCalibration] | None = None,
        protocol_version: int = DEFAULT_PROTOCOL_VERSION,
    ):
        self.port = port
        self.motors = motors
        self.calibration = calibration if calibration else {}
        self.protocol_version = protocol_version
        self._assert_same_protocol()

        self.port_handler = scs.PortHandler(self.port)
        self.packet_handler = scs.protocol_packet_handler(self.port_handler, protocol_version)
        self.sync_reader = scs.GroupSyncRead(self.packet_handler, 0, 0)
        self.sync_writer = scs.GroupSyncWrite(self.packet_handler, 0, 0)
        self._comm_success = scs.COMM_SUCCESS
        self._no_error = 0x00

        if any(MODEL_PROTOCOL[model] != self.protocol_version for model in self.models):
            raise ValueError(f"Some motors are incompatible with protocol_version={self.protocol_version}")

        self._id_to_model_dict = {m.id: m.model for m in self.motors.values()}

    def _assert_same_protocol(self) -> None:
        if any(MODEL_PROTOCOL[model] != self.protocol_version for model in self.models):
            raise RuntimeError("Some motors use an incompatible protocol.")

    @property
    def is_connected(self) -> bool:
        """bool: `True` if the underlying serial port is open."""
        return self.port_handler.is_open

    def _connect(self, handshake: bool = True) -> None:
        try:
            if not self.port_handler.openPort():
                raise OSError(f"Failed to open port '{self.port}'.")
            elif handshake:
                self._handshake()
        except (FileNotFoundError, OSError, serial.SerialException) as e:
            raise ConnectionError(
                f"\nCould not connect on port '{self.port}'. Make sure you are using the correct port."
                "\nTry running `python lerobot/find_port.py`\n"
            ) from e

    def set_timeout(self, timeout_ms: int | None = None):
        """Change the packet timeout used by the SDK.

        Args:
            timeout_ms (int | None, optional): Timeout in *milliseconds*. If `None` (default) the method falls
                back to :pyattr:`default_timeout`.
        """
        timeout_ms = timeout_ms if timeout_ms is not None else self.default_timeout
        self.port_handler.setPacketTimeoutMillis(timeout_ms)

    def connect(self, handshake: bool = True) -> None:
        """Open the serial port and initialise communication.

        Args:
            handshake (bool, optional): Pings every expected motor and performs additional
                integrity checks specific to the implementation. Defaults to `True`.

        Raises:
            DeviceAlreadyConnectedError: The port is already open.
            ConnectionError: The underlying SDK failed to open the port or the handshake did not succeed.
        """
        if self.is_connected:
            raise DeviceAlreadyConnectedError(
                f"{self.__class__.__name__}('{self.port}') is already connected. Do not call `{self.__class__.__name__}.connect()` twice."
            )

        self._connect(handshake)
        self.set_timeout()
        logging.debug(f"{self.__class__.__name__} connected.")

    @contextmanager
    def torque_disabled(self):
        """Context-manager that guarantees torque is re-enabled.

        This helper is useful to temporarily disable torque when configuring motors.

        Examples:
            >>> with bus.torque_disabled():
            ...     # Safe operations here
            ...     pass
        """
        self.disable_torque()
        try:
            yield
        finally:
            self.enable_torque()

    @cached_property
    def models(self) -> list[str]:
        return [m.model for m in self.motors.values()]

    def _assert_protocol_is_compatible(self, instruction_name: str) -> None:
        if instruction_name == "sync_read" and self.protocol_version == 1:
            raise NotImplementedError(
                "'Sync Read' is not available with Feetech motors using Protocol 1. Use 'Read' sequentially instead."
            )
        if instruction_name == "broadcast_ping" and self.protocol_version == 1:
            raise NotImplementedError(
                "'Broadcast Ping' is not available with Feetech motors using Protocol 1. Use 'Ping' sequentially instead."
            )

    def _assert_same_firmware(self) -> None:
        firmware_versions = self._read_firmware_version(self.ids, raise_on_error=True)
        if len(set(firmware_versions.values())) != 1:
            raise RuntimeError(
                "Some Motors use different firmware versions:"
                f"\n{pformat(firmware_versions)}\n"
                "Update their firmware first using Feetech's software. "
                "Visit https://www.feetechrc.com/software."
            )

    @cached_property
    def ids(self) -> list[int]:
        return [m.id for m in self.motors.values()]

    def _get_motor_id(self, motor: NameOrID) -> int:
        if isinstance(motor, str):
            return self.motors[motor].id
        elif isinstance(motor, int):
            return motor
        else:
            raise TypeError(f"'{motor}' should be int, str.")

    def _is_comm_success(self, comm: int) -> bool:
        return comm == self._comm_success

    def _is_error(self, error: int) -> bool:
        return error != self._no_error

    def ping(self, motor: NameOrID, num_retry: int = 0, raise_on_error: bool = False) -> int | None:
        """Ping a single motor and return its model number.

        Args:
            motor (NameOrID): Target motor (name or ID).
            num_retry (int, optional): Extra attempts before giving up. Defaults to `0`.
            raise_on_error (bool, optional): If `True` communication errors raise exceptions instead of
                returning `None`. Defaults to `False`.

        Returns:
            int | None: Motor model number or `None` on failure.
        """
        id_ = self._get_motor_id(motor)
        for n_try in range(1 + num_retry):
            model_number, comm, error = self.packet_handler.ping(id_)
            if self._is_comm_success(comm):
                break
            logging.debug(f"ping failed for {id_=}: {n_try=} got {comm=} {error=}")

        if not self._is_comm_success(comm):
            if raise_on_error:
                raise ConnectionError(self.packet_handler.getTxRxResult(comm))
            else:
                return
        if self._is_error(error):
            if raise_on_error:
                raise RuntimeError(self.packet_handler.getRxPacketError(error))
            else:
                return

        return model_number

    def _assert_motors_exist(self) -> None:
        expected_models = {m.id: self.model_number_table[m.model] for m in self.motors.values()}

        found_models = {}
        for id_ in self.ids:
            model_nb = self.ping(id_)
            if model_nb is not None:
                found_models[id_] = model_nb

        missing_ids = [id_ for id_ in self.ids if id_ not in found_models]
        wrong_models = {
            id_: (expected_models[id_], found_models[id_])
            for id_ in found_models
            if expected_models.get(id_) != found_models[id_]
        }

        if missing_ids or wrong_models:
            error_lines = [f"{self.__class__.__name__} motor check failed on port '{self.port}':"]

            if missing_ids:
                error_lines.append("\nMissing motor IDs:")
                error_lines.extend(f"  - {id_} (expected model: {expected_models[id_]})" for id_ in missing_ids)

            if wrong_models:
                error_lines.append("\nMotors with incorrect model numbers:")
                error_lines.extend(
                    f"  - {id_} ({self._id_to_name(id_)}): expected {expected}, found {found}"
                    for id_, (expected, found) in wrong_models.items()
                )

            error_lines.append("\nFull expected motor list (id: model_number):")
            error_lines.append(pformat(expected_models, indent=4, sort_dicts=False))
            error_lines.append("\nFull found motor list (id: model_number):")
            error_lines.append(pformat(found_models, indent=4, sort_dicts=False))

            raise RuntimeError("\n".join(error_lines))

    def _handshake(self) -> None:
        self._assert_motors_exist()
        self._assert_same_firmware()

    def _find_single_motor(self, motor: str, initial_baudrate: int | None = None) -> tuple[int, int]:
        if self.protocol_version == 0:
            return self._find_single_motor_p0(motor, initial_baudrate)
        else:
            return self._find_single_motor_p1(motor, initial_baudrate)

    def _find_single_motor_p0(self, motor: str, initial_baudrate: int | None = None) -> tuple[int, int]:
        model = self.motors[motor].model
        search_baudrates = [initial_baudrate] if initial_baudrate is not None else self.model_baudrate_table[model]
        expected_model_nb = self.model_number_table[model]

        for baudrate in search_baudrates:
            self.set_baudrate(baudrate)
            id_model = self.broadcast_ping()
            if id_model:
                found_id, found_model = next(iter(id_model.items()))
                if found_model != expected_model_nb:
                    raise RuntimeError(
                        f"Found one motor on {baudrate=} with id={found_id} but it has a "
                        f"model number '{found_model}' different than the one expected: '{expected_model_nb}'. "
                        f"Make sure you are connected only connected to the '{motor}' motor (model '{model}')."
                    )
                return baudrate, found_id

        raise RuntimeError(f"Motor '{motor}' (model '{model}') was not found. Make sure it is connected.")

    def _find_single_motor_p1(self, motor: str, initial_baudrate: int | None = None) -> tuple[int, int]:
        model = self.motors[motor].model
        search_baudrates = [initial_baudrate] if initial_baudrate is not None else self.model_baudrate_table[model]
        expected_model_nb = self.model_number_table[model]

        for baudrate in search_baudrates:
            self.set_baudrate(baudrate)
            for id_ in range(scs.MAX_ID + 1):
                found_model = self.ping(id_)
                if found_model is not None:
                    if found_model != expected_model_nb:
                        raise RuntimeError(
                            f"Found one motor on {baudrate=} with id={id_} but it has a "
                            f"model number '{found_model}' different than the one expected: '{expected_model_nb}'. "
                            f"Make sure you are connected only connected to the '{motor}' motor (model '{model}')."
                        )
                    return baudrate, id_

        raise RuntimeError(f"Motor '{motor}' (model '{model}') was not found. Make sure it is connected.")

    def configure_motors(self) -> None:
        for motor in self.motors:
            # By default, Feetech motors have a 500µs delay response time (corresponding to a value of 250 on
            # the 'Return_Delay_Time' address). We ensure this is reduced to the minimum of 2µs (value of 0).
            self.write_register("Return_Delay_Time", motor, 0)
            # Set 'Maximum_Acceleration' to 254 to speedup acceleration and deceleration of the motors.
            # Note: this address is not in the official STS3215 Memory Table
            self.write_register("Maximum_Acceleration", motor, 254)
            self.write_register("Acceleration", motor, 254)

    @property
    def is_calibrated(self) -> bool:
        motors_calibration = self.read_calibration()
        if set(motors_calibration) != set(self.calibration):
            return False

        same_ranges = all(
            self.calibration[motor].range_min == cal.range_min and self.calibration[motor].range_max == cal.range_max
            for motor, cal in motors_calibration.items()
        )
        if self.protocol_version == 1:
            return same_ranges

        same_offsets = all(
            self.calibration[motor].homing_offset == cal.homing_offset for motor, cal in motors_calibration.items()
        )
        return same_ranges and same_offsets

    def read_calibration(self) -> dict[str, MotorCalibration]:
        offsets, mins, maxes = {}, {}, {}
        for motor in self.motors:
            mins[motor] = self.read_register("Min_Position_Limit", motor, normalize=False)
            maxes[motor] = self.read_register("Max_Position_Limit", motor, normalize=False)
            offsets[motor] = (
                self.read_register("Homing_Offset", motor, normalize=False) if self.protocol_version == 0 else 0
            )

        calibration = {}
        for motor, m in self.motors.items():
            calibration[motor] = MotorCalibration(
                id=m.id,
                drive_mode=0,
                homing_offset=offsets[motor],
                range_min=mins[motor],
                range_max=maxes[motor],
            )

        return calibration

    def write_calibration(self, calibration_dict: dict[str, MotorCalibration]) -> None:
        for motor, calibration in calibration_dict.items():
            if self.protocol_version == 0:
                self.write("Homing_Offset", motor, calibration.homing_offset)
            self.write("Min_Position_Limit", motor, calibration.range_min)
            self.write("Max_Position_Limit", motor, calibration.range_max)

        self.calibration = calibration_dict

    def _get_half_turn_homings(self, positions: dict[NameOrID, Value]) -> dict[NameOrID, Value]:
        """
        On Feetech Motors:
        Present_Position = Actual_Position - Homing_Offset
        """
        half_turn_homings = {}
        for motor, pos in positions.items():
            model = self._get_motor_model(motor)
            max_res = self.model_resolution_table[model] - 1
            half_turn_homings[motor] = pos - int(max_res / 2)

        return half_turn_homings

    def _get_motors_list(self, motors: str | list[str] | None) -> list[str]:
        if motors is None:
            return list(self.motors)
        elif isinstance(motors, str):
            return [motors]
        elif isinstance(motors, list):
            return motors.copy()
        else:
            raise TypeError(motors)

    def _disable_torque(self, motor_id: int, model: str, num_retry: int = 0) -> None:
        addr, length = get_address(self.model_ctrl_table, model, "Torque_Enable")
        self._write(addr, length, motor_id, TorqueMode.DISABLED.value, num_retry=num_retry)
        addr, length = get_address(self.model_ctrl_table, model, "Lock")
        self._write(addr, length, motor_id, 0, num_retry=num_retry)

    def _encode_sign(self, data_name: str, ids_values: dict[int, int]) -> dict[int, int]:
        for id_ in ids_values:
            model = self._id_to_model(id_)
            encoding_table = self.model_encoding_table.get(model)
            if encoding_table and data_name in encoding_table:
                sign_bit = encoding_table[data_name]
                ids_values[id_] = encode_sign_magnitude(ids_values[id_], sign_bit)

        return ids_values

    def _id_to_model(self, motor_id: int) -> str:
        return self._id_to_model_dict[motor_id]

    def _decode_sign(self, data_name: str, ids_values: dict[int, int]) -> dict[int, int]:
        for id_ in ids_values:
            model = self._id_to_model(id_)
            encoding_table = self.model_encoding_table.get(model)
            if encoding_table and data_name in encoding_table:
                sign_bit = encoding_table[data_name]
                ids_values[id_] = decode_sign_magnitude(ids_values[id_], sign_bit)

        return ids_values

    def _split_into_byte_chunks(self, value: int, length: int) -> list[int]:
        return _split_into_byte_chunks(value, length)

    def _broadcast_ping(self) -> tuple[dict[int, int], int]:
        data_list = {}

        status_length = 6

        rx_length = 0
        wait_length = status_length * scs.MAX_ID

        txpacket = [0] * 6

        tx_time_per_byte = (1000.0 / self.port_handler.getBaudRate()) * 10.0

        txpacket[scs.PKT_ID] = scs.BROADCAST_ID
        txpacket[scs.PKT_LENGTH] = 2
        txpacket[scs.PKT_INSTRUCTION] = scs.INST_PING

        result = self.packet_handler.txPacket(self.port_handler, txpacket)
        if result != scs.COMM_SUCCESS:
            self.port_handler.is_using = False
            return data_list, result

        # set rx timeout
        self.port_handler.setPacketTimeoutMillis((wait_length * tx_time_per_byte) + (3.0 * scs.MAX_ID) + 16.0)

        rxpacket = []
        while not self.port_handler.isPacketTimeout() and rx_length < wait_length:
            rxpacket += self.port_handler.readPort(wait_length - rx_length)
            rx_length = len(rxpacket)

        self.port_handler.is_using = False

        if rx_length == 0:
            return data_list, scs.COMM_RX_TIMEOUT

        while True:
            if rx_length < status_length:
                return data_list, scs.COMM_RX_CORRUPT

            # find packet header
            for idx in range(0, (rx_length - 1)):
                if (rxpacket[idx] == 0xFF) and (rxpacket[idx + 1] == 0xFF):
                    break

            if idx == 0:  # found at the beginning of the packet
                # calculate checksum
                checksum = 0
                for idx in range(2, status_length - 1):  # except header & checksum
                    checksum += rxpacket[idx]

                checksum = ~checksum & 0xFF
                if rxpacket[status_length - 1] == checksum:
                    result = scs.COMM_SUCCESS
                    data_list[rxpacket[scs.PKT_ID]] = rxpacket[scs.PKT_ERROR]

                    del rxpacket[0:status_length]
                    rx_length = rx_length - status_length

                    if rx_length == 0:
                        return data_list, result
                else:
                    result = scs.COMM_RX_CORRUPT
                    # remove header (0xFF 0xFF)
                    del rxpacket[0:2]
                    rx_length = rx_length - 2
            else:
                # remove unnecessary packets
                del rxpacket[0:idx]
                rx_length = rx_length - idx

    def _get_motor_model(self, motor: NameOrID) -> int:
        if isinstance(motor, str):
            return self.motors[motor].model
        elif isinstance(motor, int):
            return self._id_to_model_dict[motor]
        else:
            raise TypeError(f"'{motor}' should be int, str.")

    def _serialize_data(self, value: int, length: int) -> list[int]:
        """
        Converts an unsigned integer value into a list of byte-sized integers to be sent via a communication
        protocol. Depending on the protocol, split values can be in big-endian or little-endian order.

        Supported data length for both Feetech and Dynamixel:
            - 1 (for values 0 to 255)
            - 2 (for values 0 to 65,535)
            - 4 (for values 0 to 4,294,967,295)
        """
        if value < 0:
            raise ValueError(f"Negative values are not allowed: {value}")

        max_value = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF}.get(length)
        if max_value is None:
            raise NotImplementedError(f"Unsupported byte size: {length}. Expected [1, 2, 4].")

        if value > max_value:
            raise ValueError(f"Value {value} exceeds the maximum for {length} bytes ({max_value}).")

        return self._split_into_byte_chunks(value, length)

    def broadcast_ping(self, num_retry: int = 0, raise_on_error: bool = False) -> dict[int, int] | None:
        self._assert_protocol_is_compatible("broadcast_ping")
        for n_try in range(1 + num_retry):
            ids_status, comm = self._broadcast_ping()
            if self._is_comm_success(comm):
                break
            logging.debug(f"Broadcast ping failed on port '{self.port}' ({n_try=})")
            logging.debug(self.packet_handler.getTxRxResult(comm))

        if not self._is_comm_success(comm):
            if raise_on_error:
                raise ConnectionError(self.packet_handler.getTxRxResult(comm))
            return

        ids_errors = {id_: status for id_, status in ids_status.items() if self._is_error(status)}
        if ids_errors:
            display_dict = {id_: self.packet_handler.getRxPacketError(err) for id_, err in ids_errors.items()}
            logging.error(f"Some motors found returned an error status:\n{pformat(display_dict, indent=4)}")

        return self._read_model_number(list(ids_status), raise_on_error)

    def enable_torque(self, motors: str | list[str] | None = None, num_retry: int = 0) -> None:
        for motor in self._get_motors_list(motors):
            self.write_register("Torque_Enable", motor, TorqueMode.ENABLED.value, num_retry=num_retry)
            self.write_register("Lock", motor, 1, num_retry=num_retry)

    def disable_torque(self, motors: str | list[str] | None = None, num_retry: int = 0) -> None:
        for motor in self._get_motors_list(motors):
            self.write_register("Torque_Enable", motor, TorqueMode.DISABLED.value, num_retry=num_retry)
            self.write_register("Lock", motor, 0, num_retry=num_retry)

    def reset_calibration(self, motors: NameOrID | list[NameOrID] | None = None) -> None:
        """Restore factory calibration for the selected motors.

        Homing offset is set to ``0`` and min/max position limits are set to the full usable range.
        The in-memory :pyattr:`calibration` is cleared.

        Args:
            motors (NameOrID | list[NameOrID] | None, optional): Selection of motors. `None` (default)
                resets every motor.
        """
        if motors is None:
            motors = list(self.motors)
        elif isinstance(motors, (str, int)):
            motors = [motors]
        elif not isinstance(motors, list):
            raise TypeError(motors)

        for motor in motors:
            model = self._get_motor_model(motor)
            max_res = self.model_resolution_table[model] - 1
            self.write_register("Homing_Offset", motor, 0, normalize=False)
            self.write_register("Min_Position_Limit", motor, 0, normalize=False)
            self.write_register("Max_Position_Limit", motor, max_res, normalize=False)

        self.calibration = {}

    def set_half_turn_homings(self, motors: NameOrID | list[NameOrID] | None = None) -> dict[NameOrID, Value]:
        """Centre each motor range around its current position.

        The function computes and writes a homing offset such that the present position becomes exactly one
        half-turn (e.g. `2047` on a 12-bit encoder).

        Args:
            motors (NameOrID | list[NameOrID] | None, optional): Motors to adjust. Defaults to all motors (`None`).

        Returns:
            dict[NameOrID, Value]: Mapping *motor → written homing offset*.
        """
        if motors is None:
            motors = list(self.motors)
        elif isinstance(motors, (str, int)):
            motors = [motors]
        elif not isinstance(motors, list):
            raise TypeError(motors)

        self.reset_calibration(motors)
        actual_positions = self.sync_read("Present_Position", motors, normalize=False)
        homing_offsets = self._get_half_turn_homings(actual_positions)
        for motor, offset in homing_offsets.items():
            self.write("Homing_Offset", motor, offset)

        return homing_offsets

    def _read(
        self,
        address: int,
        length: int,
        motor_id: int,
        *,
        num_retry: int = 0,
        raise_on_error: bool = True,
        err_msg: str = "",
    ) -> tuple[int, int]:
        if length == 1:
            read_fn = self.packet_handler.read1ByteTxRx
        elif length == 2:
            read_fn = self.packet_handler.read2ByteTxRx
        elif length == 4:
            read_fn = self.packet_handler.read4ByteTxRx
        else:
            raise ValueError(length)

        for n_try in range(1 + num_retry):
            value, comm, error = read_fn(motor_id, address)
            if self._is_comm_success(comm):
                break
            logging.debug(
                f"Failed to read @{address=} ({length=}) on {motor_id=} ({n_try=}): "
                + self.packet_handler.getTxRxResult(comm)
            )

        if not self._is_comm_success(comm) and raise_on_error:
            raise ConnectionError(f"{err_msg} {self.packet_handler.getTxRxResult(comm)}")
        elif self._is_error(error) and raise_on_error:
            raise RuntimeError(f"{err_msg} {self.packet_handler.getRxPacketError(error)}")

        return value, comm, error

    def read_register(
        self,
        data_name: str,
        motor: str,
        *,
        normalize: bool = True,
        num_retry: int = 0,
    ) -> Value:
        """Read a register from a motor.

        Args:
            data_name (str): Control-table key (e.g. `"Present_Position"`).
            motor (str): Motor name.
            normalize (bool, optional): When `True` (default) scale the value to a user-friendly range as
                defined by the calibration.
            num_retry (int, optional): Retry attempts.  Defaults to `0`.

        Returns:
            Value: Raw or normalised value depending on *normalize*.
        """
        if not self.is_connected:
            raise DeviceNotConnectedError(
                f"{self.__class__.__name__}('{self.port}') is not connected. You need to run `{self.__class__.__name__}.connect()`."
            )

        id_ = self.motors[motor].id
        model = self.motors[motor].model
        addr, length = get_address(self.model_ctrl_table, model, data_name)

        err_msg = f"Failed to read '{data_name}' on {id_=} after {num_retry + 1} tries."
        value, _, _ = self._read(addr, length, id_, num_retry=num_retry, raise_on_error=True, err_msg=err_msg)

        id_value = self._decode_sign(data_name, {id_: value})

        if normalize and data_name in self.normalized_data:
            id_value = self._normalize(id_value)

        return id_value[id_]

    def _write(
        self,
        addr: int,
        length: int,
        motor_id: int,
        value: int,
        *,
        num_retry: int = 0,
        raise_on_error: bool = True,
        err_msg: str = "",
    ) -> tuple[int, int]:
        data = self._serialize_data(value, length)
        for n_try in range(1 + num_retry):
            comm, error = self.packet_handler.writeTxRx(motor_id, addr, length, data)
            if self._is_comm_success(comm):
                break
            logging.debug(
                f"Failed to sync write @{addr=} ({length=}) on id={motor_id} with {value=} ({n_try=}): "
                + self.packet_handler.getTxRxResult(comm)
            )

        if not self._is_comm_success(comm) and raise_on_error:
            raise ConnectionError(f"{err_msg} {self.packet_handler.getTxRxResult(comm)}")
        elif self._is_error(error) and raise_on_error:
            raise RuntimeError(f"{err_msg} {self.packet_handler.getRxPacketError(error)}")

        return comm, error

    def write_register(
        self, data_name: str, motor: str, value: Value, *, normalize: bool = True, num_retry: int = 0
    ) -> None:
        """Write a value to a single motor's register.

        Contrary to :pymeth:`sync_write`, this expects a response status packet emitted by the motor, which
        provides a guarantee that the value was written to the register successfully. In consequence, it is
        slower than :pymeth:`sync_write` but it is more reliable. It should typically be used when configuring
        motors.

        Args:
            data_name (str): Register name.
            motor (str): Motor name.
            value (Value): Value to write.  If *normalize* is `True` the value is first converted to raw
                units.
            normalize (bool, optional): Enable or disable normalisation. Defaults to `True`.
            num_retry (int, optional): Retry attempts.  Defaults to `0`.
        """
        if not self.is_connected:
            raise DeviceNotConnectedError(
                f"{self.__class__.__name__}('{self.port}') is not connected. You need to run `{self.__class__.__name__}.connect()`."
            )

        id_ = self.motors[motor].id
        model = self.motors[motor].model
        addr, length = get_address(self.model_ctrl_table, model, data_name)

        if normalize and data_name in self.normalized_data:
            value = self._unnormalize({id_: value})[id_]

        value = self._encode_sign(data_name, {id_: value})[id_]

        err_msg = f"Failed to write '{data_name}' on {id_=} with '{value}' after {num_retry + 1} tries."
        self._write(addr, length, id_, value, num_retry=num_retry, raise_on_error=True, err_msg=err_msg)

    def _read_firmware_version(self, motor_ids: list[int], raise_on_error: bool = False) -> dict[int, str]:
        firmware_versions = {}
        for id_ in motor_ids:
            firm_ver_major, comm, error = self._read(*FIRMWARE_MAJOR_VERSION, id_, raise_on_error=raise_on_error)
            if not self._is_comm_success(comm) or self._is_error(error):
                continue

            firm_ver_minor, comm, error = self._read(*FIRMWARE_MINOR_VERSION, id_, raise_on_error=raise_on_error)
            if not self._is_comm_success(comm) or self._is_error(error):
                continue

            firmware_versions[id_] = f"{firm_ver_major}.{firm_ver_minor}"

        return firmware_versions

    def _read_model_number(self, motor_ids: list[int], raise_on_error: bool = False) -> dict[int, int]:
        model_numbers = {}
        for id_ in motor_ids:
            model_nb, comm, error = self._read(*MODEL_NUMBER, id_, raise_on_error=raise_on_error)
            if not self._is_comm_success(comm) or self._is_error(error):
                continue

            model_numbers[id_] = model_nb

        return model_numbers
