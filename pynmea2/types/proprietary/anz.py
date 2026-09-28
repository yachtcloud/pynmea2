"""Support for YachtCloud's proprietary ANZ messages."""

from ... import nmea


class ANZ(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        identifier_index = next(
            (index for index, value in enumerate(data) if value not in (None, '')),
            None,
        )
        sentence_id = data[identifier_index] if identifier_index is not None else None
        name = manufacturer + sentence_id if sentence_id else manufacturer
        message_class = _cls.sentence_types.get(name, _cls)
        return super(ANZ, message_class).__new__(message_class)


class ANZRSI(ANZ):
    """Rudder and steering information."""

    fields = (
        ('Sentence identifier', 'sentence_id'),
        ('Source CAN Unit ID', 'source_id'),
        ('Order rudder', 'rudder_order'),
        ('Actual rudder', 'rudder_actual'),
        ('Status', 'status'),
        ('Position of steering', 'steering_position'),
    )
