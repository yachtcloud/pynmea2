from decimal import Decimal

import pytest
import pynmea2
from pynmea2.types.proprietary.anz import ANZRSI
from pynmea2.types.talker import ALC, HTD, POS


def test_HTD_parses_typed_heading_and_track_fields():
    sentence = '$AGHTD,V,0.3,R,M,N,35.0,30.0,0.5,30.0,,0.000,,T,A,A,A,14.5*4E'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, HTD)
    assert msg.talker == 'AG'
    assert msg.sentence_type == 'HTD'
    assert msg.override == 'V'
    assert msg.commanded_rudder_angle == Decimal('0.3')
    assert msg.commanded_rudder_direction == 'R'
    assert msg.selected_steering_mode == 'M'
    assert msg.turn_mode == 'N'
    assert msg.commanded_rudder_limit == Decimal('35.0')
    assert msg.commanded_off_heading_limit == Decimal('30.0')
    assert msg.commanded_radius_of_turn == Decimal('0.5')
    assert msg.commanded_rate_of_turn == Decimal('30.0')
    assert msg.commanded_heading_to_steer is None
    assert msg.commanded_off_track_limit == Decimal('0.000')
    assert msg.commanded_track is None
    assert msg.heading_reference_in_use == 'T'
    assert msg.rudder_status == 'A'
    assert msg.off_heading_status == 'A'
    assert msg.off_track_status == 'A'
    assert msg.vessel_heading == Decimal('14.5')
    assert msg.render() == sentence


def test_POS_keeps_raw_fields_and_empty_positions():
    sentence = '$VDPOS,VD,01,A,0.0,0.0,,V,,,R*08'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, POS)
    assert msg.field_1 == 'VD'
    assert msg.field_6 == ''
    assert msg.field_7 == 'V'
    assert msg.field_10 == 'R'
    assert len(POS.fields) == 11
    assert msg.render() == sentence


@pytest.mark.parametrize('talker', ['VD', 'AI'])
def test_ALC_supports_both_talkers_and_retains_alert_group_fields(talker):
    sentence = '${}ALC,01,02,59,0,group,condition'.format(talker)

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, ALC)
    assert msg.sentence_type == 'ALC'
    assert msg.field_1 == '01'
    assert msg.field_4 == '0'
    assert msg.data[4:] == ['group', 'condition']
    assert msg.render(checksum=False) == sentence


def test_ANZRSI_maps_named_fields_and_keeps_sentence_identifier():
    sentence = '$PANZRSI,65,0.0,6.7,S,0'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, ANZRSI)
    assert msg.sentence_id == 'RSI'
    assert msg.source_id == '65'
    assert msg.rudder_order == '0.0'
    assert msg.rudder_actual == '6.7'
    assert msg.status == 'S'
    assert msg.steering_position == '0'
    assert msg.render(checksum=False) == sentence


def test_ANZ_dispatches_using_first_nonempty_sentence_identifier():
    sentence = '$PANZ,,RSI,65,0.0,6.7,S,0'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, ANZRSI)
    assert msg.manufacturer == 'ANZ'
    assert msg.data == ['', '', 'RSI', '65', '0.0', '6.7', 'S', '0']
    assert msg.render(checksum=False) == sentence
