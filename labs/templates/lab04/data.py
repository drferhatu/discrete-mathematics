"""
The social network for Lab 4. These are FICTIONAL people.

FOLLOWS maps each person to the set of people they follow:
    FOLLOWS["Bora"] == {"Ada", "Can"}     means Bora follows Ada and Can.

Nobody follows themselves. Do not change this file: the tests also use other, hidden networks.
"""

FOLLOWS = {
    "Ada":   {"Bora"},
    "Bora":  {"Ada", "Can"},
    "Can":   {"Ada"},
    "Defne": {"Ada", "Emir"},
    "Emir":  {"Ada", "Defne"},
    "Funda": {"Ada", "Gökay"},
    "Gökay": {"Ada"},
    "Hira":  {"Ada"},
}
