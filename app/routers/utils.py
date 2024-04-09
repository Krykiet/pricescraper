from typing import Type

from app.models.models import RDN


def convert_properties_to_str(obj: Type[RDN]):
    return {'id': obj.id,
            'date': str(obj.date_scraped),
            'f1_price': str(obj.f1_price),
            'f1_volume': str(obj.f1_volume),
            'f2_price': str(obj.f2_price),
            'f2_volume': str(obj.f2_volume),
            'cont_price': str(obj.cont_price),
            'cont_volume': str(obj.cont_volume)}