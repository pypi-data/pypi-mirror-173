import mbsim.core.server as mb

_fx = {"d": 2, "i": 4, "h": 3, "c": 1}  # Map to some modbus functions
context = mb.genContext()  # Gen a shared context with all Vals set to 0


@mb.Task(1, args=(context,))
def watchdog(context):
    """
    A Simple watch dog that will toggle the val in the first Holding register.
    The one in the decorator is the number of secs to wait till next execution.

    :param context: context that the modbus server will use
    """
    if context[0].getValues(_fx["h"], 1)[0] == 0:
        context[0].setValues(_fx["h"], 1, [1])
    else:
        context[0].setValues(_fx["h"], 1, [0])


@mb.Task(1, args=(context,))
def add(context):
    """
    A Simple function that will add 1 to the val in the Second Holding register
    The one in the decorator is the number of secs to wait till next execution.

    :param context: context that the modbus server will use
    """
    x = context[0].getValues(_fx["h"], 2)[0]
    x += 1
    context[0].setValues(_fx["h"], 2, [x])


mb.start("tcp", context=context, address=("", 5020))  # Starts the modbus server
