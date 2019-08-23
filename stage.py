import serial
import argparse
import logging

logger = logging.getLogger("ThorlabsLL9K")


def get_position(address):
    with serial.Serial(address) as s:
        s.write(b"0gs")
        status = s.readline().decode("ascii").rstrip()
        if status != "0GS00":
            raise IOError("Stage GetStatus returned {}.".format(status))
        s.write(b"0gp")
        position = s.readline().decode("ascii").rstrip()
        if position.startswith("0PO"):
            print("Current stage position is: {}, which is {}mm and "
                  "slot {}".format(position, int(position[3:], 16), int(position[3:], 16) // 31))


def move_stage(pos, address):
    with serial.Serial(address) as s:
        logger.info("Move to Position: {}.".format(pos))
        s.write(b"0gs")

        status = s.readline().decode("ascii").rstrip()
        if status != "0GS00":
            logger.error("Stage GetStatus returned {}. No move will be executed.".format(status))
            raise IOError("Stage GetStatus returned {}. No move will be executed.".format(status))
        # requested position in absolute units of stage:
        req = pos * 31

        if pos == 0:
            # for position 0 we home the stage for repeatability.
            s.write(b"0ho0")
        else:
            # convert absolute position to HEX
            req_hex = "%08X" % req
            s.write("0ma{}".format(req_hex).encode("ascii"))
        answer = s.readline().decode("ascii").rstrip()
        if answer.startswith("0PO"):
            # check that reported position is nearby requested position
            actual_position = int(answer[3:], 16)
            if abs(actual_position - req) < 2:
                print("OK")
            else:
                logger.error("Final position was {}, but requested was {}.".format(actual_position, req))
                raise IOError("Final position was {}, but requested was {}.".format(actual_position, req))
        else:
            logger.error("Could not move stage to pos {}".format(pos))
            raise IOError("Could not move stage to pos {}".format(pos))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Control for Thorlabs LL9K linear stage. '
                                                 'If position argument is not set, the current position will be '
                                                 'returned.')
    parser.add_argument('position', type=int, choices=[0, 1, 2, 3], nargs="?",
                        help='sets position of stage to slot 0, 1, 2 or 3. Slot 0 is the slot in home position. '
                             'If not set, current stage position is returned.')
    parser.add_argument('-d', '--device', type=str, default='/dev/ttyUSB0', help='address of linear stage.')
    args = parser.parse_args()
    if args.position is not None:
        move_stage(args.position, args.device)
    else:
        get_position(args.device)