from .interfaces import IdentityDataPointInterface


class Configurables:
    class Data:
        required_data_points = [
            IdentityDataPointInterface(
                name="first_name",
                pretty_name="First Name",
                type="text",
            ),
            IdentityDataPointInterface(
                name="last_name",
                pretty_name="Last Name",
                type="text"
            )
        ]

    class Web:
        secret_key = "DEFAULT-KEY-CHANGE-ME-BEFORE-PRODUCTION"
