# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2022
from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser


def parse_live_coin_watch_row(data_row, parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Date'])
    data_row.parsed = True

    if row_dict['Fee']:
        fee_quantity = row_dict['Fee']
    else:
        fee_quantity = None

    fee_asset = row_dict['Base'] if row_dict['Fee Currency'] == 'base' else row_dict['Quote']

    if row_dict['Trade'] in ("buy",):
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                                 data_row.timestamp,
                                                 buy_quantity=row_dict['Base Quantity'],
                                                 buy_asset=row_dict['Base'],
                                                 sell_quantity=row_dict['Quote Quantity'],
                                                 sell_asset=row_dict['Quote'],
                                                 fee_quantity=fee_quantity,
                                                 fee_asset=fee_asset,
                                                 note=row_dict['Notes'])
    elif row_dict['Trade'] == "deposit":
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                                 data_row.timestamp,
                                                 buy_quantity=row_dict['Base Quantity'],
                                                 buy_asset=row_dict['Base'],
                                                 note=row_dict['Notes'])

    elif row_dict['Trade'] in ("reward",):
        if 'stak' in row_dict.get('Notes', '').lower():
            data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_STAKING,
                                                     data_row.timestamp,
                                                     buy_quantity=row_dict['Base Quantity'],
                                                     buy_asset=row_dict['Base'],
                                                     fee_quantity=fee_quantity,
                                                     fee_asset=fee_asset,
                                                     note=row_dict['Notes'])
        else:
            data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_INCOME,
                                                     data_row.timestamp,
                                                     buy_quantity=row_dict['Base Quantity'],
                                                     buy_asset=row_dict['Base'],
                                                     fee_quantity=fee_quantity,
                                                     fee_asset=fee_asset,
                                                     note=row_dict['Notes'])


DataParser(DataParser.TYPE_SHARES,
           "Live Coin Watch",
           ['Date', 'Trade', 'Base', 'Quote', 'Base Quantity', 'Quote Quantity',
            'Fee', 'Fee Currency', 'Fee Type', 'Price (GBP)',
            'Since Trade (%)', 'Notes'],
           worksheet_name="Sheet 1",
           row_handler=parse_live_coin_watch_row)
