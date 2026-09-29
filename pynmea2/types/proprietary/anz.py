"""Support for proprietary ANZ messages."""

from ... import nmea


def _leading_empty_fields(data):
    count = 0
    for value in data:
        if value not in (None, ''):
            break
        count += 1
    return count


class ANZ(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        leading = _leading_empty_fields(data)
        sentence_id = data[leading] if leading < len(data) else None
        name = manufacturer + sentence_id if sentence_id else manufacturer
        message_class = _cls.sentence_types.get(name, _cls)
        return super(ANZ, message_class).__new__(message_class)

    def __init__(self, manufacturer, data):
        # '$PANZ,,RSI,...' carries empty fields before the sentence identifier.
        # Drop them so data lines up with fields, and keep them in identifier()
        # so render() reproduces the original sentence.
        leading = _leading_empty_fields(data)
        if leading == len(data):
            leading = 0
        self.leading_empty_fields = leading
        super(ANZ, self).__init__(manufacturer, data[leading:])

    def identifier(self):
        return 'P%s%s' % (self.manufacturer, ',' * self.leading_empty_fields)


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
